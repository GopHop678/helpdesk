import { convertDateTime } from "./convert_datetime";


async function UpdateBoard(pk) {
    const response = await fetch(`http://localhost:8000/api/request/${pk}`);
    const requestObj = await response.json();

    const board = document.querySelector(".requests-wrapper");
    const category = requestObj.category;

    const requestWrapper = document.createElement("div");
        requestWrapper.classList.add('requests-wrapper');
    const newRequestHeader = document.createElement("div");
        newRequestHeader.classList.add('request-header');
    const newRequestBody = document.createElement("div");
        newRequestBody.classList.add('request-body');

    newRequestHeader.innerHTML = `
        <span class="request-time">requestObj.request_date</span>
        <span class="request-from">requestObj.sender.full_name</span>
        <span class="request-place">{{ requestObj.place }}</span>
        <div class="complete-btn-wrapper"><button class="complete-btn">Выполнить</button></div>
        <div class="reject-btn-wrapper"><button class="reject-btn">Отклонить</button></div>
        <div class="request-status">{{ requestObj.status }}</div>`

    newRequestBody.innerHTML = `
        <span class="request-category">{{ requestObj.category }}</span>
        <span class="request-text">{{ requestObj.request_text.slice(0, 101) }}</span>`
        // <span class="request-details-btn" id="details_{{ requestObj.id }}">Подробнее</span>

    if (category === 'PRINTER') {
        requestWrapper.classList.add('printer');
    } else if (category === 'SOFTWARE') {
        requestWrapper.classList.add('software');
    } else if (category === 'HARDWARE') {
        requestWrapper.classList.add('hardware');
    } else if (category === 'ETC') {
        requestWrapper.classList.add('etc');
    }
    console.log(requestObj);
    requestWrapper.append(newRequestHeader);
    requestWrapper.append(newRequestBody);
    board.prepend(requestWrapper);

    // const requestHeader = wrapper.querySelector('.request-details-header');
    // const requestCategory = requestHeader.querySelector('.request-details-category');
    // requestCategory.textContent = displayCategory(requestObj.category);
    // const requestTime = requestHeader.querySelector('.request-details-time');
    // requestTime.textContent = convertDateTime(requestObj.request_date);
    // const requestSender = requestHeader.querySelector('.request-details-sender');
    // requestSender.textContent = requestObj.sender.full_name;
    // const requestPlace = requestHeader.querySelector('.request-details-place');
    // requestPlace.textContent = requestObj.place;
    // const requestBody = wrapper.querySelector('.request-details-body');
    // const requestText = requestBody.querySelector('.request-details-text');
    // requestText.textContent = requestObj.request_text;
}


document.addEventListener('DOMContentLoaded', function() {
    const socket = new WebSocket("ws://" + window.location.host + "/ws/tmp/");
    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        const requestId = data.data.request_id;
        UpdateBoard(requestId);
    }
});