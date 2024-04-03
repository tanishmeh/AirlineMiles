// index.js
document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('flightSearchForm');
    searchForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission

        const from = document.getElementById('departureAirport').value;
        const to = document.getElementById('arrivalAirport').value;
        const date1 = document.getElementById('departureDate1').value;
        const date2 = document.getElementById('departureDate2').value;

        window.location.href = '/results';

        sendInputs(from, to, date1, date2).then(() => {
        }).catch(error => {
            console.error('Submission error:', error);
        });
    });
});

function sendInputs(from, to, date1, date2) {
    return fetch('/AAOneWayFINAL', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ from, to, date1, date2 }),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not OK');
            }
            return response.json();
        })
        .catch(error => {
            console.error('Error:', error);
            throw error;
        });
}
