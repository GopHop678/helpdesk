async function showPopup (e) {
    const requestId = e.id.slice(8);
    const response = await fetch(`/api/request/${requestId}`);
    const requestObj = await response.json();

    if (!requestObj) {
        return;
    }

    const popup = document.getElementById('request-details-popup');
    popup.addEventListener('click', (e) => {
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

    const detailsBtnCollection = wrapper.getElementsByClassName('details-btn');
    const detailsBtns = Array.from(detailsBtnCollection);

    const completeBtn = wrapper.querySelector('.complete-btn')
    const rejectBtn = wrapper.querySelector('.reject-btn')

    console.log(detailsBtnCollection);
    console.log(detailsBtns);
    console.log(completeBtn);
    console.log(rejectBtn);
    console.log(true);

    if (completeBtn) {
        completeBtn.id = `complete_-btn-${requestId}`;
        completeBtn.addEventListener('click', () => {
            changeStatus(completeBtn);
            popup.style.display = 'none';
        })
    }
    if (rejectBtn) {
        rejectBtn.id = `reject_-btn-${requestId}`;
        rejectBtn.addEventListener('click', () => {
            changeStatus(rejectBtn);
            popup.style.display = 'none';
        })
    }

    if (['COMPLETED', 'REJECTED'].includes(requestObj.status)) {
        detailsBtns.forEach(btn => {
            btn.style.display = 'none';
        })
    } else {
        detailsBtns.forEach(btn => {
            btn.style.display = 'inherit';
        })
    }

    popup.style.display = 'flex';


    const filesWrapper = wrapper.querySelector('.request-details-files');
    const imagesWrapper = filesWrapper.querySelector('.request-details-images');
    const docsWrapper = filesWrapper.querySelector('.request-details-docs');

    imagesWrapper.innerHTML = '';
    docsWrapper.innerHTML = '';

    const responseFiles = await fetch(`/api/request/${requestId}/files`);
    const files = await responseFiles.json();

    for (const file of files) {
        if (['png', 'jpg', 'jpeg'].includes(file.file_type.toLowerCase())) {
            const newImage = document.createElement('img');
            newImage.src = file.file;
            imagesWrapper.appendChild(newImage);
        } else {
            const newFile = document.createElement('a');
            newFile.href = file.file;
            newFile.target = '_blank';
            newFile.textContent = decodeURIComponent(file.file).split('/').slice(-1);
            docsWrapper.appendChild(newFile);
        }
    }
}


document.addEventListener('DOMContentLoaded', function() {
    const detailsButtons = Array.from(document.getElementsByClassName('request-details-btn'));
    detailsButtons.forEach(detailsButton =>
        detailsButton.addEventListener('click', () => {showPopup(detailsButton)}))
});
