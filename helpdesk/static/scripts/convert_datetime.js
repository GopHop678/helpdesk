function convertDateTime(inputDateTime) {
    // Создаем объект Date из входной строки
    const date = new Date(inputDateTime);
    // Извлекаем компоненты даты
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = String(date.getFullYear()).slice(-2);
    // Извлекаем компоненты времени
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    // Форматируем результат
    return `${day}.${month}.${year} | ${hours}:${minutes}`;
}

export { convertDateTime };
