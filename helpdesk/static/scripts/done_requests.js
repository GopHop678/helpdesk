async function loadDoneRequests() {
    const doneRequestsWrapper = document.getElementById('done-requests-wrapper');
    doneRequestsWrapper.innerHTML = '';

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
}


document.addEventListener('DOMContentLoaded', loadDoneRequests());
