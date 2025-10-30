async function changeStatus (e) {
    const requestId = e.id.split('-')[2];
    const changeTo = e.id.slice(0, 1);
    let newStatus = ''
    if (changeTo === 'c') {
        newStatus = 'COMPLETED'
    } else if (changeTo === 'r') {
        newStatus = 'REJECTED'
    }
    const response = await fetch(`/api/request/${requestId}/change_status`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newStatus),
    });
    const responseMsg = await response.json();
    if (response.status !== 200) {
        window.location.reload(); //////////
    }
}


document.addEventListener('DOMContentLoaded', function() {
    const detailsButtons = Array.from(document.getElementsByClassName('change-status-btn'));
    detailsButtons.forEach(detailsButton =>
        detailsButton.addEventListener('click', () => {changeStatus(detailsButton)}))
});