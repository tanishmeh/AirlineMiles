const fs = require('fs');

// Function to transform flight data
function transformData(flight) {
    return {
        origin: flight.origin,
        destination: flight.destination,
        departureTime: flight.departTime, // Corrected key name
        arrivalTime: flight.arriveTime,
        flightTime: flight.travelTime,
        options: {
            Economy: flight.Economy,
            Premium: flight.Premium,
            Business: flight.Business,
            First: flight.First
        }
    };
}

// Reading and transforming the data
fs.readFile('AANonstop.json', 'utf8', (err, data) => {
    if (err) {
        console.error("Error reading file:", err);
        return;
    }
    try {
        const flights = JSON.parse(data);
        const transformedFlights = {};
        Object.keys(flights).forEach(date => {
            transformedFlights[date] = Object.keys(flights[date]).map(flightKey =>
                transformData(flights[date][flightKey])
            );
        });
        console.log(JSON.stringify(transformedFlights, null, 2));
    } catch (err) {
        console.error("Error parsing JSON:", err);
    }
});
