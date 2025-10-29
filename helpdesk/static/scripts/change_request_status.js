async function changeStatus (e) {
    const requestId = e.id.split('-')[2];
    const changeTo = e.id.slice(0, 1);
    let newStatus = ''
    console.log(requestId);
    if (changeTo === 'c') {
        newStatus = 'COMPLETED'
    } else if (changeTo === 'r') {
        newStatus = 'REJECTED'
    }
    console.log(newStatus);
    const response = await fetch(`http://localhost:8000/api/request/${requestId}/change_status`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newStatus),
    });
    const responseMsg = await response.json();
    console.log(responseMsg);
}


document.addEventListener('DOMContentLoaded', function() {
    const detailsButtons = Array.from(document.getElementsByClassName('change-status-btn'));
    detailsButtons.forEach(detailsButton =>
        detailsButton.addEventListener('click', () => {changeStatus(detailsButton)}))
});