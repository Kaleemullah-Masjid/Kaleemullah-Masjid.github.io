// Replace these with your latitude and longitude coordinates
const latitude = 42.03326482384257;
const longitude = -87.73497403508489;

// Function to fetch sunrise and sunset times using the API
async function getSunriseSunsetTime(latitude, longitude) {
    const apiKey = 'YOUR_API_KEY'; // Replace with your actual API key (sign up at https://sunrise-sunset.org/api)
    const url = `https://api.sunrise-sunset.org/json?lat=${latitude}&lng=${longitude}&date=today&formatted=0`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        return data.results;
    } catch (error) {
        console.error('Error fetching sunrise-sunset data:', error);
        return null;
    }
}
// Function to display the sunrise and sunset times on the HTML page
function displaySunriseSunsetTimes(sunriseTime, sunsetTime) {
    const sunriseSunsetInfoDiv = document.getElementById('Prayer_Times');
    sunriseSunsetInfoDiv.innerHTML = `
        <h1>Sunrise and Sunset Times</h1>
        <p>Sunrise: ${sunriseTime}</p>
        <p>Sunset: ${sunsetTime}</p>
    `;
}
// Function to display the sunrise and sunset times
function displaySunriseSunsetTime(data) {
    if (data) {
        const sunriseTime = new Date(data.sunrise).toLocaleTimeString();
        const sunsetTime = new Date(data.sunset).toLocaleTimeString();
        console.log('Sunrise Time:', sunriseTime);
        console.log('Sunset Time:', sunsetTime);
        displaySunriseSunsetTimes(sunrise, sunset);
    } else {
        console.log('Unable to fetch sunrise-sunset data.');
    }
}

// Call the functions
getSunriseSunsetTime(latitude, longitude)
    .then(displaySunriseSunsetTime)
    .catch((error) => console.error('Error:', error));
