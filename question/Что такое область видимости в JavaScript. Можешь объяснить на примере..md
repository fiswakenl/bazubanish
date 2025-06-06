**Область видимости** в JavaScript — это контекст, в котором доступны переменные и функции. Существует три типа:

1. **Глобальная**: переменные, объявленные вне функций, доступны везде.
2. **Функциональная**: переменные, объявленные внутри функции, доступны только в этой функции.
3. **Блочная**: переменные, объявленные с помощью `let` или `const` в блоках (`if`, `for`), доступны только внутри этих блоков.

Пример:

```javascript
var globalVar = 'Глобальная';

function myFunction() {
    var localVar = 'Локальная';
    if (true) {
        let blockVar = 'Блочная';
        console.log(blockVar); // доступна
    }
    console.log(localVar); // доступна
    // console.log(blockVar); // ошибка: не определена
}

myFunction();
console.log(globalVar); // доступна
// console.log(localVar); // ошибка: не определена
```
