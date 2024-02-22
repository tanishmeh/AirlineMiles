class Flight {
  constructor(flightNumber, origin, destination, departTime, arriveTime, travelTime, Economy, Premium, Business, First) {
    this.flightNumber = flightNumber;
    this.origin = origin;
    this.destination = destination;
    this.departTime = departTime;
    this.arriveTime = arriveTime;
    this.travelTime = travelTime;
    this.Economy = Economy;
    this.Premium = Premium;
    this.Business = Business;
    this.First = First;
  }
}

// Global variable to store flights data
let globalFlightsData = [];

document.addEventListener('DOMContentLoaded', function() {
  fetch('/flights')
  .then(response => response.json())
  .then(data => {
    // Store fetched data for later sorting
    globalFlightsData = transformData(data);
    renderFlights(globalFlightsData);
  })
  .catch(error => console.error('Error fetching flight data:', error));

  // Event listener for sort selection change
  document.getElementById('sort-by').addEventListener('change', function() {
    sortAndRenderFlights();
  });
});

// Transform fetched data into a sortable array
function transformData(data) {
  let flightsArray = [];
  Object.entries(data).forEach(([date, flights]) => {
    Object.entries(flights).forEach(([flightNumber, flightDetails]) => {
      let flight = new Flight(
        flightNumber,
        flightDetails.origin,
        flightDetails.destination,
        flightDetails.departTime,
        flightDetails.arriveTime,
        flightDetails.travelTime,
        flightDetails.Economy,
        flightDetails.Premium,
        flightDetails.Business,
        flightDetails.First
        );
      flightsArray.push(flight);
    });
  });
  return flightsArray;
}

// Sort (if needed) and re-render flights
// Converts price string "10.5K + $5.60" to a numeric value
function parsePrice(priceString) {
  const [kPart, dollarPart] = priceString.split(' + ');
  let total = 0;
  if (kPart) {
    const numericKPart = parseFloat(kPart.replace('K', '')) * 10; // Convert "K" part to numeric
    total += numericKPart;
  }
  if (dollarPart) {
    const numericDollarPart = parseFloat(dollarPart.replace('$', '')); // Convert dollar part to numeric
    total += numericDollarPart;
  }
  return total;
}

function sortAndRenderFlights() {
  let sortBy = document.getElementById('sort-by').value;
  globalFlightsData.sort((a, b) => {
    if (['Economy', 'Premium', 'Business', 'First'].includes(sortBy)) {
      return parsePrice(a[sortBy]) - parsePrice(b[sortBy]);
    } else if (sortBy === 'Duration') {
      return parseDuration(a.duration) - parseDuration(b.duration);
    }
  });
  renderFlights(globalFlightsData);
}


// Function to parse duration string into a comparable number (e.g., total minutes)
function parseDuration(durationStr) {
  // Example implementation for parsing duration strings
  const [hours, minutes] = durationStr.match(/\d+/g);
  return parseInt(hours) * 60 + parseInt(minutes);
}
// Function to render flights to the DOM
function renderFlights(flightsData) {
  const flightsContainer = document.getElementById('flights');
  flightsContainer.innerHTML = ''; // Clear existing flights
  flightsData.forEach(flightDetails => {
    const flightDiv = document.createElement('div');
    flightDiv.className = 'flight-card';
    flightDiv.innerHTML = `
            <div class="flight-header">
              <span class="airport">${flightDetails.origin}</span>
              <div class="non-stop">Non Stop</div>
              <span class="airport">${flightDetails.destination}</span>
            </div>
            <div class="flight-times">
              <span>${flightDetails.departTime}</span>
              <span class="travel-time">${flightDetails.travelTime}</span>
              <span>${flightDetails.arriveTime.split('\n')[0]}</span>
            </div>
            <div class="line"></div>
            <div class="flight-pricing">
              <div>Economy<br>${flightDetails.Economy}</div>
              <div>Premium<br>${flightDetails.Premium || "N/A"}</div>
              <div>Business<br>${flightDetails.Business || "N/A"}</div>
              <div>First<br>${flightDetails.First || "N/A"}</div>
            </div>
          `;
    flightsContainer.appendChild(flightDiv);
  });
}
