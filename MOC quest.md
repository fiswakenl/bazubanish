```dataviewjs
const input = dv.el("input", "", {
    placeholder: "Введите вопрос для поиска",
    style: "margin-bottom: 10px;"
});

// Функция Дебаунса
function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        if (timeoutId) {
            clearTimeout(timeoutId);
        }
        timeoutId = setTimeout(() => {
            func.apply(this, args);
        }, delay);
    };
}

function displayResults(searchProfession) {
    dv.container.empty();
    dv.container.appendChild(input);

    const results = dv.pages('"questions_folder"')
        .filter(page => page.question && page.question.toLowerCase().includes(searchProfession.toLowerCase()));

    // Сохраняем сортировку с логированием
    results.values.sort((a, b) => {
        console.log({ a, b });
        return b.count - a.count;
    });

    // Ограничиваем количество выводимых результатов до 50
    const limitedResults = results.slice(0, 100);

    if (limitedResults.length > 0) {
        const tableData = limitedResults.map(page => {
            const questionLink = `[${page.question}](question/${encodeURIComponent(page.question)})`;
            const questionLinkElement = dv.el("span", questionLink, {
                class: page.file ? "" : "gray-link" // Добавляем класс, если файла нет
            });

            return [
                `[${page.count}](${page.uid})`, // Счетчик
                questionLinkElement, // Вопрос с ссылкой
                page.category // Категория
            ];
        });

        dv.table(["C", "Question", "Category"], tableData);
    } else {
        dv.paragraph("Ничего не найдено.");
    }

    input.focus();
}

// Инициализация
displayResults("");

// Обработчик события с дебаунсом
input.addEventListener("input", debounce((event) => {
    displayResults(event.target.value);
}, 300));

// CSS для серой ссылки без подчеркивания
dv.container.append(dv.el("style", `
    .gray-link {
        color: gray; /* Серый цвет для ссылки */
        pointer-events: none; /* Запретить клики по ссылке, если файла нет */
        text-decoration: none; /* Убираем подчеркивание */
    }
`));
```
