
- **any** отключает проверку типов, что делает его небезопасным и может привести к ошибкам, так как позволяет использовать любые значения без проверки.
- **unknown** безопаснее, требует сужения типа перед использованием, что заставляет проверять значения перед вызовом методов или обращением к свойствам.
- **never** используется для функций, которые никогда не возвращают значение (например, из-за бесконечного цикла или выбрасывания ошибки), и также применяется для отфильтровки типов в утилити-типах и конструкциях `switch` с `enum`.