---
layout: post
title: "Почему твой Share Extension сломался в iOS 18 (и что с этим делать в 2026)"
date: 2026-01-14
description:
tags: []
---

Раньше я ненавидел функцию Share на мобильных. Много лет это был просто значок, который везде лезет и которым я никогда не пользуюсь. Но в какой-то момент что-то щёлкнуло — я понял, что Share это как pipe в Unix: берёшь контент в одном приложении и одним действием отправляешь в другое. Не нужно копировать-вставлять, сохранять файл, искать «импорт» — просто выбираешь следующий инструмент и продолжаешь цепочку. Только вместо потока Share передаёт пакет (ссылка, текст, файл, несколько фото).

Проблема в том, что в Unix пайпы живут внутри одной пользовательской среды, а Share почти всегда пересекает границы приложений: отдельные песочницы, отдельные процессы, отдельные правила безопасности. Поэтому задача «передать данные» быстро превращается в задачу «передать данные в контекст пользователя»: получатель должен понять, кто сейчас пользователь и куда этот пакет класть. В моём случае: пользователь отправляет ссылку в приложение, но обработка происходит на сервере, а значит сначала нужна аутентификация. Что делать, если Share прилетел, а сессии нет — или она недоступна прямо сейчас?

## Наивное решение: «просто открой приложение»

Первая идея, которая приходит в голову: расширение обнаруживает, что пользователь не авторизован, и открывает основное приложение. Пользователь логинится, возвращается в Safari, снова нажимает Share — и теперь всё работает.

В коде это выглядит просто:

```swift
extensionContext?.open(URL(string: "dropkind://login")!) { success in
    self.extensionContext?.completeRequest(returningItems: nil)
}
```

Или через Universal Links:

```swift
extensionContext?.open(URL(string: "https://dropkind.app/auth")!)
```

Этот паттерн работал годами. Share Extension как launcher: обнаружило проблему, передало эстафету основному приложению, закрылось.

В iOS 18 это перестало работать.

## Что сломала Apple (и почему это не баг)

При попытке открыть приложение из Share Extension в iOS 18 получаем ошибку:

```
LSApplicationWorkspaceErrorDomain Code=115
```

Это не баг и не временная регрессия. Apple [прямо пишет](https://developer.apple.com/forums/thread/764570), что app extensions не имеют права открывать URL напрямую; обходы через runtime ломаются. Если нужно внимание пользователя — используйте local notification.

### Cold start / Warm start

По моему опыту, иногда `extensionContext.open(...)` срабатывает только когда приложение уже было в памяти, но гарантий нет и это не документировано.

Проблема в том, что нельзя контролировать, в каком состоянии находится приложение. Пользователь мог закрыть его час назад, и `extensionContext.open()` молча провалится.

### Что Apple рекомендует вместо openURL

На том же форуме Quinn пишет:

> «If your app extension needs to get the user's attention, do that by posting a local notification.»
>
> (Если расширению нужно привлечь внимание пользователя — используйте local notification.)

Идея в том, что расширение не должно быть трамплином в основное приложение — оно должно само справляться с задачей. Если не может — честно сообщить пользователю через local notification.

### Старые хаки больше не работают

Если вы гуглили эту проблему раньше, то наверняка видели «хак» с UIResponder chain:

```swift
// ЭТО БОЛЬШЕ НЕ РАБОТАЕТ
var responder: UIResponder? = self
while responder != nil {
    if let application = responder as? UIApplication {
        application.perform(#selector(openURL(_:)), with: url)
        break
    }
    responder = responder?.next
}
```

Начиная с iOS 18 этот код выдаёт ошибку песочницы (`NSOSStatusErrorDomain Code=-54`). Система проверяет стек вызовов и блокирует попытки обойти ограничения.

## Как это делают приложения Apple

Интересно посмотреть, как сама Apple решает эту проблему в своих приложениях.

Вот что я обнаружил:

**Заметки (Notes):** при шаринге ссылки в Заметки расширение показывает выбор папки, нажимаешь «Сохранить» и... остаёшься в Safari. Заметка сохраняется через фоновую синхронизацию, узнаёшь об этом, только когда откроешь Заметки.

**Фото:** аналогично — расширение сохраняет в общий контейнер, синхронизация происходит в фоне.

**Сообщения:** если выбрать контакт из «предложений» в Share Sheet, система сама открывает Messages. Это системный путь, а не openURL из расширения.

Получается, приложения Apple либо не открывают основное приложение вообще, либо используют привилегированные системные механизмы, недоступные сторонним разработчикам.

## Три рабочих решения

### Решение А: Shared Keychain — расширение само управляет авторизацией

Лучшее решение — сделать расширение автономным. Если расширение имеет доступ к токену авторизации, оно может само отправить данные на сервер, не трогая основное приложение.

Идея простая: основное приложение при логине сохраняет токен в Keychain с общей группой доступа, а Share Extension его читает и само делает API-запрос.

```swift
// В основном приложении при логине:
let query: [String: Any] = [
    kSecClass as String: kSecClassGenericPassword,
    kSecAttrAccount as String: "authToken",
    kSecAttrAccessGroup as String: "group.com.dropkind.shared",
    kSecValueData as String: token.data(using: .utf8)!
]
SecItemAdd(query as CFDictionary, nil)
```

```swift
// В Share Extension:
let query: [String: Any] = [
    kSecClass as String: kSecClassGenericPassword,
    kSecAttrAccount as String: "authToken",
    kSecAttrAccessGroup as String: "group.com.dropkind.shared",
    kSecReturnData as String: true
]
var result: AnyObject?
SecItemCopyMatching(query as CFDictionary, &result)
```

Главное преимущество — UX идеальный: пользователь нажимает «Сохранить» и остаётся где был. Только нужно настроить Keychain Sharing между targets и убедиться, что токен доступен (не истёк, не отозван).

**Важный нюанс:** Keychain может переживать удаление приложения, так что на автоматическую очистку рассчитывать нельзя. Представьте такой сценарий: пользователь залогинился, удалил приложение, через год создал новый аккаунт (например, в веб-версии сервиса), поставил приложение и сразу использовал Share — расширение найдёт старый токен и отправит данные не тому пользователю.

Спасает то, что App Group UserDefaults, в отличие от Keychain, удаляется вместе с приложением. Храним `currentUserId` в UserDefaults и проверяем его наличие перед использованием токена:

```swift
// В Share Extension:
let shared = UserDefaults(suiteName: "group.com.dropkind.shared")
guard shared?.string(forKey: "currentUserId") != nil else {
    // UserDefaults пуст → приложение переустановлено → требуем логин
    return
}
// Только теперь доверяем токену из Keychain
```

### Решение Б: Вход в приложение через local notification

Если расширение не может открыть приложение программно, пусть это сделает пользователь по тапу на local notification:

1. Расширение обнаруживает, что сессии нет
2. Сохраняет данные во временное хранилище (App Group UserDefaults)
3. Показывает local notification: «Нажмите, чтобы войти и сохранить ссылку»
4. Пользователь нажимает — это легитимное действие, система разрешает запуск приложения

```swift
// В Share Extension:
func showLoginNotification(pendingURL: URL) {
    // Сохраняем данные
    let defaults = UserDefaults(suiteName: "group.com.dropkind.shared")
    defaults?.set(pendingURL.absoluteString, forKey: "pendingShare")

    // Планируем уведомление
    let content = UNMutableNotificationContent()
    content.title = "Требуется вход"
    content.body = "Нажмите, чтобы войти в DropKind и сохранить ссылку"
    content.userInfo = ["action": "completeShare"]

    let request = UNNotificationRequest(
        identifier: "loginRequired",
        content: content,
        trigger: nil // Показать сразу
    )
    UNUserNotificationCenter.current().add(request)
}
```

Реализация простая и работает надёжно. Минус — дополнительный шаг для пользователя и нужно разрешение на уведомления.

### Решение В: OAuth внутри расширения

Самый сложный вариант — это реализовать полноценный логин прямо в Share Extension:

1. Расширение показывает WebView с OAuth-страницей
2. Пользователь логинится
3. Токен сохраняется в Shared Keychain
4. Данные отправляются

```swift
// Упрощённо:
class ShareViewController: SLComposeServiceViewController {
    func presentLogin() {
        let authURL = URL(string: "https://dropkind.app/oauth/authorize?...")!
        let authSession = ASWebAuthenticationSession(
            url: authURL,
            callbackURLScheme: "dropkind"
        ) { callbackURL, error in
            // Обработать токен
        }
        authSession.presentationContextProvider = self
        authSession.start()
    }
}
```

Пользователь не покидает Share Sheet — это хорошо. Но реализация сложная, не все OAuth-провайдеры хорошо работают в расширениях, и есть нюансы с `ASWebAuthenticationSession` внутри extension.

## Что я выбрал

Для DropKind я выбрал комбинацию решений А и Б. Основной путь — Shared Keychain: если пользователь уже залогинен в приложении, расширение подхватывает токен и работает автономно. Если токена нет — показываем local notification.

Конкретика реализации:

1) **Отдельный share‑token в Keychain.** Основное приложение получает отдельный share‑token и сохраняет его в Shared Keychain. Share Extension использует этот токен для прямого POST в API.

2) **user_id в App Group.** Вместе с токеном сохраняем `user_id` в App Group UserDefaults. Это служит двум целям: сервер сверяет владельца токена, а само наличие `user_id` — маркер того, что приложение не переустанавливалось (UserDefaults очищается при удалении, в отличие от Keychain).

3) **Если токена нет** — расширение сохраняет данные в App Group и показывает local notification «Войдите, чтобы сохранить ссылку». По тапу открывается приложение. Если пользователь не дал разрешение на уведомления — показываем ту же просьбу прямо в UI расширения.

4) **Основное приложение “дожимает” позже.** При следующем запуске приложение подхватывает сохранённые данные, ведёт пользователя на логин, а после входа завершает отправку.

Такой подход даёт лучший UX для большинства пользователей (уже залогиненных), но не ломается для новых.

Возвращаясь к аналогии с pipe: `grep` не говорит «откройте терминал и введите паттерн» — он просто работает с тем, что есть. Share Extension должен делать то же самое, когда это возможно.
