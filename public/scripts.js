document.addEventListener('DOMContentLoaded', function() {
  fetch('/flights')
    .then(response => response.json())
    .then(data => {
      const flightsContainer = document.getElementById('flights');
      Object.entries(data).forEach(([date, flights]) => {
        Object.entries(flights).forEach(([flightNumber, flightDetails]) => {
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
      });
    })
    .catch(error => console.error('Error fetching flight data:', error));
});

document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('sort-by').addEventListener('change', sortResults);
});

function sortResults() {
  const sortBy = document.getElementById('sort-by').value;
  // Assuming flights data is rendered and can be sorted directly in the DOM
  // You may need to fetch or access the flights data array depending on how it's stored
  const flightsContainer = document.getElementById('flights');
  let flights = Array.from(flightsContainer.children);
  
  flights.sort((a, b) => {
    // Assuming each flight element has data attributes for pricing and duration for simplicity
    let aValue, bValue;
    switch (sortBy) {
      case 'economyPrice':
        aValue = parseFloat(a.dataset.economyPrice);
        bValue = parseFloat(b.dataset.economyPrice);
        break;
      case 'premiumPrice':
        aValue = parseFloat(a.dataset.premiumPrice);
        bValue = parseFloat(b.dataset.premiumPrice);
        break;
      case 'businessPrice':
        aValue = parseFloat(a.dataset.businessPrice);
        bValue = parseFloat(b.dataset.businessPrice);
        break;
      case 'firstPrice':
        aValue = parseFloat(a.dataset.firstPrice);
        bValue = parseFloat(b.dataset.firstPrice);
        break;
      case 'duration':
        aValue = parseFloat(a.dataset.duration);
        bValue = parseFloat(b.dataset.duration);
        break;
      default:
        // Default to not sorting if no valid sort option is selected
        return 0;
    }
    
    // Sorting logic for numbers
    return aValue - bValue;
  });
  
  // Clear the container before re-adding sorted elements
  flightsContainer.innerHTML = '';
  flights.forEach(flight => {
    flightsContainer.appendChild(flight);
  });
}
