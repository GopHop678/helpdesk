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


function displayCategory(category) {
    const categories = {
        PRINTER: 'Принтер',
        SOFTWARE: 'Программа',
        HARDWARE: 'Компьютер',
        ETC: 'Другое',
    }
    return categories[category];
}


function displayStatus(status) {
    const statuses = {
        WORKING: 'В работе',
        REJECTED: 'Отклонено',
        COMPLETED: 'Выполнено',
    }
    return statuses[status];
}


document.addEventListener('DOMContentLoaded', async function() {
    const doneRequestsWrapper = document.getElementById('done-requests-wrapper');

    const response = await fetch(`/api/requests/done`);
    const requestObjs = await response.json();

    requestObjs.forEach((requestObj) => {
        const requestWrapper = document.createElement("div");
            requestWrapper.classList.add('request-wrapper');
            const newRequestHeader = document.createElement("div");
        newRequestHeader.classList.add('request-header');
            const newRequestBody = document.createElement("div");
        newRequestBody.classList.add('request-body');

        newRequestHeader.innerHTML = `
        <span class="request-time">${convertDateTime(requestObj.request_date)}</span>
        <span class="request-from">${requestObj.sender.full_name}</span>
        <span class="request-place">${requestObj.place}</span>
        <div class="request-status">${displayStatus(requestObj.status)}</div>`

        newRequestBody.innerHTML = `
        <span class="request-category">${displayCategory(requestObj.category)}</span>
        <span class="request-text">${requestObj.request_text.slice(0, 101)}</span>
        <span class="request-details-btn" id="details-${requestObj.id}">Подробнее</span>`

        const showDetailsBtn = newRequestBody.querySelector(`#details-${requestObj.id}`);
        showDetailsBtn.addEventListener('click', () => {
            showPopup(showDetailsBtn);
        });

        if (requestObj.status === 'COMPLETED') {
            requestWrapper.classList.add('completed');
        } else if (requestObj.status === 'REJECTED') {
            requestWrapper.classList.add('rejected');
        }

        requestWrapper.append(newRequestHeader);
        requestWrapper.append(newRequestBody);
        doneRequestsWrapper.prepend(requestWrapper);
    });
});
