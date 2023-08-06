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
function getCurrentFormattedDate() {
    const months = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ];

    const today = new Date();
    const day = String(today.getDate()).padStart(2, '0');
    const month = months[today.getMonth()];
    const year = today.getFullYear();

    return `${day}-${month}-${year}`;
}

function getFormattedDate() {
    const today = new Date();

    const year = today.getFullYear();
    const month = today.getMonth() + 1; // Months are zero-based, so add 1
    const day = today.getDate();
    //Output: "2023-08-03" (current date will vary)
    //const formattedDate = `${year}-${month < 10 ? '0' : ''}${month}-${day < 10 ? '0' : ''}${day}`;
    //05-08-2023 DD-MM-YYYY
    const formattedDate = `${day < 10 ? '0' : ''}${day}-${month < 10 ? '0' : ''}${month}-${year}`;

    return formattedDate;
}
async function getIslamicDate() {
    const date = getFormattedDate(); // Replace with the desired Gregorian date

    //Example Request: http://api.aladhan.com/v1/gToH/07-12-2014
    const apiUrl = `https://api.aladhan.com/v1/gToH?date=${date}`;

    try {
        const response = await fetch(apiUrl);
        const data = await response.json();
        if (response.ok && data.code === 200) {
            const hijri_year = data.data.hijri.year;
            const hijri_day = data.data.hijri.day;
            const hijri_month = data.data.hijri.month.number;
            const hijri_month_str = data.data.hijri.month.en;
            const islamicDate_1 = data.data.hijri.date
            const islamicDate_2 = `${hijri_day}-${hijri_month_str}-${hijri_year}`;
            const islamicDate = {islamicDate_1,islamicDate_2}
            return islamicDate;
        } else {
            console.error('Failed to fetch Islamic date.');
            return null;
        }
    } catch (error) {
        console.error('Error fetching Islamic date:', error);
        return null;
    }
}
// Function to display the sunrise and sunset times on the HTML page
function displayHijriDate(Hijri_date_t) {
    const Hijri_date_Cell = document.getElementById('Hijri');
    const formattedDate = getCurrentFormattedDate();
    Hijri_date_Cell.innerHTML = `<b>Today is: </b> ${formattedDate} || ${Hijri_date_t}`;
    
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
    const islamic_dates = await getIslamicDate();
    if (sunriseSunsetData) {
        if (islamic_dates) {
            const islamic_date = islamic_dates.islamicDate_2
            const sunriseTime = new Date(sunriseSunsetData.sunrise).toLocaleTimeString();
            const sunsetTime = new Date(sunriseSunsetData.sunset).toLocaleTimeString();
            
            displayHijriDate(islamic_date);
            displaySunriseSunsetTimes(sunriseTime, sunsetTime);
        } else {z
            console.log('Unable to fetch Islamic Date data.');
        }
        
    } else {
            console.log('Unable to fetch sunrise-sunset data.');
    }
}


// Call the main function when the page finishes loading
window.addEventListener('load', loadSunriseSunsetData);
