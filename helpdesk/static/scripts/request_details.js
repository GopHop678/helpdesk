function displayCategory(category) {
    const categories = {
        PRINTER: 'Принтер',
        SOFTWARE: 'Программа',
        HARDWARE: 'Компьютер',
        ETC: 'Другое',
    }
    return categories[category];
}


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



async function showPopup (e) {
    const requestId = e.id.slice(8);
    const response = await fetch(`http://localhost:8000/api/request/${requestId}`);
    const requestObj = await response.json();

    if (!requestObj) {
        return;
    }

    const popup = document.getElementById('request-details-popup');
    popup.addEventListener('click', (e) => {
        // Если клик был на самом popup (не на его дочерних элементах)
        if (e.target === popup) {
            popup.style.display = 'none';
        }
    });

    const wrapper = popup.querySelector('.request-details-wrapper');
    const requestHeader = wrapper.querySelector('.request-details-header');
        const requestCategory = requestHeader.querySelector('.request-details-category');
            requestCategory.textContent = displayCategory(requestObj.category);
        const requestTime = requestHeader.querySelector('.request-details-time');
            requestTime.textContent = convertDateTime(requestObj.request_date);
        const requestSender = requestHeader.querySelector('.request-details-sender');
            requestSender.textContent = requestObj.sender.full_name;
        const requestPlace = requestHeader.querySelector('.request-details-place');
            requestPlace.textContent = requestObj.place;
    const requestBody = wrapper.querySelector('.request-details-body');
        const requestText = requestBody.querySelector('.request-details-text');
            requestText.textContent = requestObj.request_text;

    popup.style.display = 'flex';
}


document.addEventListener('DOMContentLoaded', function() {
    const detailsButtons = Array.from(document.getElementsByClassName('request-details-btn'));
    // console.log(detailsButtons);

    detailsButtons.forEach(detailsButton =>
        detailsButton.addEventListener('click', () => {showPopup(detailsButton)}))
});
