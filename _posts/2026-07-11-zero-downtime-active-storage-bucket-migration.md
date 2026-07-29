---
layout: post
title: "Moving Active Storage Between Buckets Without 404s"
date: 2026-07-11
description: "A small fallback service and rclone made it possible to move Active Storage files to a new S3 bucket without downtime."
og_image:
  canvas:
    background_image: "/assets/images/og-backgrounds/bg-4190.png"
---

I recently had to move the user uploads of a live Rails application to a new S3 bucket. There were several million objects totaling more than a terabyte, and users kept uploading images, PDFs, and other files throughout the move.

Copying the bucket and switching the configuration wasn't quite enough. During the final sync, some recent uploads would still exist only in the old bucket. Switching reads to the new one at that point would temporarily turn those files into 404s.

I solved this with a small Active Storage service: new files go to the new bucket, while reads try the new bucket first and fall back to the old one on a miss.

```ruby
# lib/active_storage/service/s3_fallback_service.rb
require "active_storage/service"

class ActiveStorage::Service::S3FallbackService < ActiveStorage::Service
  attr_reader :primary, :fallback

  def self.build(primary:, fallback:, name:, configurator:, **)
    new(
      primary: configurator.build(primary),
      fallback: configurator.build(fallback)
    ).tap { |service| service.name = name }
  end

  def initialize(primary:, fallback:)
    @primary = primary
    @fallback = fallback
  end

  delegate :upload, :update_metadata, :compose,
           :url_for_direct_upload, :headers_for_direct_upload, to: :primary

  def download(key, &block)
    primary.download(key, &block)
  rescue ActiveStorage::FileNotFoundError
    fallback.download(key, &block)
  end

  def download_chunk(key, range)
    primary.download_chunk(key, range)
  rescue ActiveStorage::FileNotFoundError
    fallback.download_chunk(key, range)
  end

  def exist?(key)
    primary.exist?(key) || fallback.exist?(key)
  end

  def url(key, **options)
    (primary.exist?(key) ? primary : fallback).url(key, **options)
  end

  def delete(key)
    primary.delete(key)
    fallback.delete(key)
  end

  def delete_prefixed(prefix)
    primary.delete_prefixed(prefix)
    fallback.delete_prefixed(prefix)
  end
end
```

The important detail here is to rescue `ActiveStorage::FileNotFoundError`, not the S3 provider's error. The standard `S3Service` has already wrapped it by this point.

We use Active Storage in proxy mode, so the fallback happens inside Rails and is invisible to the client. The `url` method provides the same behavior in redirect mode, at the cost of an extra HEAD request whenever a file is served during the migration.

The configuration looked like this:

```yaml
production:
  service: S3Fallback
  primary: s3_new
  fallback: s3_old

s3_new:
  service: S3
  # credentials, bucket, endpoint

s3_old:
  service: S3
  # credentials, bucket, endpoint
```

The wrapper has to use the existing service name—`production` in my case. Active Storage stores that name in `active_storage_blobs.service_name` for every blob. Give the wrapper a new name and existing blobs will continue to use the old service directly.

The migration itself was straightforward:

1. Copy most of the files to the new bucket in advance, if possible.
2. Deploy the fallback service. From this point on, new files go to the new bucket and the old one is only needed for reads.
3. Run `rclone copy` from the old bucket to the new one.
4. Verify the result with `rclone check`.
5. Once there are no differences, remove the wrapper and point the regular S3 service at the new bucket.

`rclone copy` is safe to restart. I ran it from a small VM close to the buckets. With several million objects, each pass took about 35 minutes almost regardless of the size of the delta.

Two more details that are easy to forget:

- If you use direct uploads, copy the CORS configuration to the new bucket before switching.
- Don't delete the old bucket immediately. Keep it around briefly as a rollback source.

Active Storage's built-in `Mirror` service wasn't quite enough for this. It writes to multiple services but reads only from the primary, so the migration still ends with a hard switch that requires the new bucket to be complete. The fallback service let me switch writes first, finish copying at leisure, and remove the wrapper only after verifying the result.

In the end, several million files moved without downtime or broken images. All it took was a small Ruby class and two rclone commands: `copy` and `check`.
