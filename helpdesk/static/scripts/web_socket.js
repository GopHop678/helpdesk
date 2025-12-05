async function UpdateBoard(pk) {
    const response = await fetch(`/api/request/${pk}`);
    const requestObj = await response.json();

    const board = document.querySelector(".requests-wrapper");
    const category = requestObj.category;

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
        <div class="complete-btn-wrapper">
            <button class="complete-btn change-status-btn" id="complete-btn-${requestObj.id}">Выполнить</button>
        </div>
        <div class="reject-btn-wrapper change-status-btn">
            <button class="reject-btn change-status-btn" id="reject-btn-${requestObj.id}">Отклонить</button>
        </div>
        <div class="request-status">${displayStatus(requestObj.status)}</div>`

    newRequestBody.innerHTML = `
        <span class="request-category">${displayCategory(requestObj.category)}</span>
        <span class="request-text">${requestObj.request_text.slice(0, 101)}</span>
        <span class="request-details-btn" id="details-${requestObj.id}">Подробнее</span>`

    const showDetailsBtn = newRequestBody.querySelector(`#details-${requestObj.id}`);
    showDetailsBtn.addEventListener('click', () => {
        showPopup(showDetailsBtn);
    });

    const completeBtn = newRequestHeader.querySelector(`#complete-btn-${requestObj.id}`);
    completeBtn.addEventListener('click', () => {
        changeStatus(completeBtn);
    });

    const rejectBtn = newRequestHeader.querySelector(`#reject-btn-${requestObj.id}`);
    rejectBtn.addEventListener('click', () => {
        changeStatus(rejectBtn);
    });

    if (category === 'PRINTER') {
        requestWrapper.classList.add('printer');
    } else if (category === 'SOFTWARE') {
        requestWrapper.classList.add('software');
    } else if (category === 'HARDWARE') {
        requestWrapper.classList.add('hardware');
    } else if (category === 'ETC') {
        requestWrapper.classList.add('etc');
    }

    requestWrapper.append(newRequestHeader);
    requestWrapper.append(newRequestBody);
    board.prepend(requestWrapper);
}


document.addEventListener('DOMContentLoaded', function() {
    const socket = new WebSocket("ws://" + window.location.host + "/ws/board/");
    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        const requestId = data.data.request_id;
        UpdateBoard(requestId);
    }
});