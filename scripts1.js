class Flight {
    constructor(flightNumber, departureTime, arrivalTime, economyPrice, premiumPrice, businessPrice, firstPrice, duration, origin, destination) {
        this.flightNumber = flightNumber;
        this.departureTime = departureTime;
        this.arrivalTime = arrivalTime;
        this.economyPrice = economyPrice;
        this.premiumPrice = premiumPrice;
        this.businessPrice = businessPrice;
        this.firstPrice = firstPrice;
        this.duration = duration;
        this.origin = origin; // Added origin
        this.destination = destination; // Added destination
    }
}

// Global variable to store flights data as Flight objects
let globalFlightsData = [];

document.addEventListener('DOMContentLoaded', function() {
    fetchFlightsData();
    document.getElementById('sort-by').addEventListener('change', sortAndRenderFlights);
});

function fetchFlightsData() {
    fetch('/flights')
        .then(response => response.json())
        .then(data => {
            globalFlightsData = transformData(data);
            renderFlights(globalFlightsData);
        })
        .catch(error => console.error('Error fetching flight data:', error));
}

function transformData(data) {
    let flightsArray = [];
    Object.entries(data).forEach(([date, flights]) => {
        Object.entries(flights).forEach(([flightNumber, flightDetails]) => {
            let temp = new Flight(
                flightNumber,
                flightDetails.departureTime,
                flightDetails.arrivalTime,
                flightDetails.Economy,
                flightDetails.Premium,
                flightDetails.Business,
                flightDetails.First,
                flightDetails.flightTime,
                flightDetails.origin, // Assuming origin is part of flightDetails
                flightDetails.destination // Assuming destination is part of flightDetails
            );
            flightDetails.flightNumber = flightNumber; // Add flight number to details for reference
            flightsArray.push(flightDetails);
        });
    });
    return flightsArray;
}

function sortAndRenderFlights() {
    const sortBy = document.getElementById('sort-by').value;
    globalFlightsData.sort((a, b) => {
        switch (sortBy) {
            case 'economyPrice':
                return a.economyPrice - b.economyPrice;
            case 'premiumPrice':
                return a.premiumPrice - b.premiumPrice;
            case 'businessPrice':
                return a.businessPrice - b.businessPrice;
            case 'firstPrice':
                return a.firstPrice - b.firstPrice;
            case 'duration':
                // Assuming duration is a numeric value representing minutes or similar
                return a.duration - b.duration;
            default:
                return 0;
        }
    });
    renderFlights(globalFlightsData);
}


function renderFlights(flightsData) {
    const flightsContainer = document.getElementById('flights');
    flightsContainer.innerHTML = ''; // Clear existing flights
    flightsData.forEach(flight => {
        const flightDiv = document.createElement('div');
        flightDiv.className = 'flight-card';
        flightDiv.innerHTML = `
            <div class="flight-header">
              <span class="airport">${flight.origin}</span>
              <div class="non-stop">Non Stop</div>
              <span class="airport">${flight.destination}</span>
            </div>
            <div class="flight-times">
              <span>${flight.departureTime}</span>
              <span class="travel-time">${flight.duration}</span>
              <span>${flight.arrivalTime.split('\n')[0]}</span>
            </div>
            <div class="line"></div>
            <div class="flight-pricing">
              <div>Economy<br>${flight.economyPrice}</div>
              <div>Premium<br>${flight.premiumPrice || "N/A"}</div>
              <div>Business<br>${flight.businessPrice || "N/A"}</div>
              <div>First<br>${flight.firstPrice || "N/A"}</div>
            </div>
          `;
        flightsContainer.appendChild(flightDiv);
    });
}
