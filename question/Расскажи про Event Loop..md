
Event Loop — это механизм в JavaScript, который управляет выполнением кода, асинхронными задачами и событиями. Он работает так:  
1. Синхронные задачи выполняются сразу в стеке вызовов.  
2. Асинхронные операции (например, `setTimeout`, `fetch`) передаются в Web API браузера.  
3. После завершения они попадают в очередь:  
   - Микрозадачи (`Promise`, `MutationObserver`) → очередь микрозадач.  
   - Макрозадачи (`setTimeout`, `setInterval`) → очередь макрозадач.  
4. Event Loop проверяет стек вызовов. Если он пуст, он сначала обрабатывает все микрозадачи, потом одну макрозадачу и повторяет цикл.  

Это позволяет JS работать в однопоточном режиме, не блокируя интерфейс. Например, `Promise.then` сработает раньше `setTimeout`, даже с нулевой задержкой.