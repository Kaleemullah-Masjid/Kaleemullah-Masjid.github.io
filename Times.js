// Function to fetch sunrise and sunset times using the API
async function getSunriseSunsetTime() {
    const latitude = 42.03326482384257;
    const longitude = -87.73497403508489;
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
    const sunsetTimeCell = document.getElementById('sunsetTime');
    const sunriseTimeCell = document.getElementById('sunriseTime');
    sunriseTimeCell.textContent = sunriseTime;
    sunsetTimeCell.textContent = sunsetTime;
    
}
// Function to display the sunrise and sunset times
async function loadSunriseSunsetData(data) {
    const sunriseSunsetData = await getSunriseSunsetTime();
    if (sunriseSunsetData) {
        const sunriseTime = new Date(sunriseSunsetData.sunrise).toLocaleTimeString();
        const sunsetTime = new Date(sunriseSunsetData.sunset).toLocaleTimeString();
        displaySunriseSunsetTime(sunriseTime,sunsetTime);
        console.log('Sunrise Time:', sunriseTime);
        console.log('Sunset Time:', sunsetTime);
        displaySunriseSunsetTimes(sunrise, sunset);
    } else {
        console.log('Unable to fetch sunrise-sunset data.');
    }
}
// Call the main function when the page finishes loading
window.addEventListener('load', loadSunriseSunsetData);
