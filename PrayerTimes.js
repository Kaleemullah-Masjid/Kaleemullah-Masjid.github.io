// main.js

// Function to format a date according to the specified format
async function formatDate(date, format = 'DD-MM-YYYY') {
    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based, so add 1
    const year = date.getFullYear();
    const month_str = months[date.getMonth()];

     // Determine the date format and return the formatted date string
    if (format === 'DD-MM-YYYY') {          ////  "DD-MM-YYYY": Day-Month-Year (e.g., 23-08-2023)
        return `${day}-${month}-${year}`;
    } else if (format === 'MM/DD/YYYY') {   //"MM/DD/YYYY": Month/Day/Year (e.g., 08/23/2023)
        return `${month}/${day}/${year}`;
    } else if (format === 'YYYY-MM-DD') {   //"YYYY-MM-DD": Year-Month-Day (e.g., 2023-08-23)
        return `${year}-${month}-${day}`;
    } else if (format === 'YYYY/MM/DD') {   //"YYYY/MM/DD": Year/Month/Day (e.g., 2023/08/23)
        return `${year}-${month}-${day}`;
    } else if (format === 'DD/MM/YYYY') {   //"DD/MM/YYYY": Day/Month/Year (e.g., 23/08/2023)
        return `${day}-${month}-${year}`;
    }
    else if (format === 'DD MM YYYY') {   //"DD MMM YYYY": Day Month Year (e.g., 23 Aug 2023)
        return `${day} ${month} ${year}`;
    } else if (format === 'DD MMM YYYY') {   //"DD MMM YYYY": Day Month Year (e.g., 23 Aug 2023)
        return `${day} ${month_str} ${year}`;
    } else if (format === 'MMM DD, YYYY') {   //"MMM DD, YYYY": Month Day, Year (e.g., Aug 23, 2023)
        return `${month_str} ${day}, ${year}`;
    } else if (format === 'YYYY MMM DD') {   //"YYYY MMM DD": Year Month Day (e.g., 2023 Aug 23)
        return `${year} ${month_str} ${day}`;
    } else if (format === 'DD-MMM-YYYY') {   //"DD-MMM-YYYY": Day Month Year (e.g., 23-Aug-2023)
        return `${day}-${month_str}-${year}`;
    }
}

async function format_Islamic_Date(date){
    const_islamic_dates = {1: 'Muharram'
        , 2:'Safar'
        , 3:'Rabi al-Awwal'
        , 4:'Rabi al-Thani'
        , 5:'Jumada al-Awwal'
        , 6:'Jumada al-Thani'
        , 7:'Rajab'
        , 8:"Shaban"
        , 9:'Ramadan'
        , 10:'Shawwal'
        , 11:'Dhu al-Qadah'
        , 12:'Dhu al-Hijjah'
    }
    islamic_date_list = date.split('-')
    islamic_month = parseInt(islamic_date_list[1])
    islamic_month_str = const_islamic_dates[islamic_month]
    islamic_date_list_new = islamic_date_list
    islamic_date_list_new[1] = islamic_month_str

    new_islamic_date = islamic_date_list_new.join('-')
    
    return(new_islamic_date)

}
// Function to parse CSV data and convert it into an array of objects
async function parseCSV(csv) {
    const lines = csv.split('\n');
    const headers = lines[0].split(',');
    const data = [];

    for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',');
        const entry = {};

        for (let j = 0; j < headers.length; j++) {
            entry[headers[j]] = values[j];
        }

        data.push(entry);
    }

    return data;
}

// Function to fetch CSV data from a GitHub URL
async function fetchCsvFromGitHub() {
    const githubRawUrl = 'https://raw.githubusercontent.com/Kaleemullah-Masjid/Kaleemullah-Masjid.github.io/main/Data/PRAYER_TIMES/PRAYER_TIMES.csv'; // Replace with your GitHub URL

    try {
        const response = await fetch(githubRawUrl);
        if (response.ok) {
            const csvData = await response.text();
            // Process the CSV data here
            const today = new Date();
            const today_str = await formatDate(today, format = 'DD MMM YYYY');
            const data_csv = await parseCSV(csvData);
            const filteredData = data_csv.filter(entry => entry.Date === today_str);

            return(filteredData)

        } else {
            throw new Error('Failed to fetch CSV file');
        }
    } catch (error) {
        console.error(error);
    }
}

// Function to fetch sunrise and sunset times from an API
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
async function displaySunriseSunsetTimes() {
    const sunriseSunsetData = await getSunriseSunsetTime();
    const sunriseTime = new Date(sunriseSunsetData.sunrise).toLocaleTimeString();
    const sunsetTime = new Date(sunriseSunsetData.sunset).toLocaleTimeString();
    const sunsetTimeCell = document.getElementById('sunsetTime');
    const sunriseTimeCell = document.getElementById('sunriseTime');
    sunriseTimeCell.textContent = sunriseTime;
    sunsetTimeCell.textContent = sunsetTime;   
}



// Function to display prayer times and Islamic date on the HTML page
async function displayISNA() {
    try {
        // Fetch sunrise and sunset times and prayer times
        await displaySunriseSunsetTimes();
        const prayer_temp = await fetchCsvFromGitHub();
        if (prayer_temp.length > 0) {
            //PULL FIRST ROW DATA
            const prayer_times = prayer_temp[0]
            //GET NEW ISLAMIC DATE
            const new_islamic_date = await format_Islamic_Date(prayer_times['Islamic_Date'])
            //GET DOCUMENT IDs 
            const FAJR_ISNA = document.getElementById('FAJR_ISNA');
            const SUNRISE_ISNA = document.getElementById('SUNRISE_ISNA');
            const ZUHR_ISNA = document.getElementById('ZUHR_ISNA');
            const ASR_ISNA = document.getElementById('ASR_ISNA');
            const MAGRHEB_ISNA = document.getElementById('MAGRHEB_ISNA');
            const ISHA_ISNA = document.getElementById('ISHA_ISNA');
            const Hijri_date_Cell = document.getElementById('Hijri');
            
            // Display prayer times and Islamic date
            Hijri_date_Cell.innerHTML = `<b>Today is: </b> ${prayer_times['Date']} || ${new_islamic_date}`;
            FAJR_ISNA.textContent = prayer_times['Fajr'];
            SUNRISE_ISNA.textContent = prayer_times['Sunrise'];
            ZUHR_ISNA.textContent = prayer_times['Dhuhr'];
            ASR_ISNA.textContent = prayer_times['Asr'];
            MAGRHEB_ISNA.textContent = prayer_times['Maghrib'];
            ISHA_ISNA.textContent = prayer_times['Isha'];
        } else {
            console.error('No prayer data available for today.');
        }
    } catch (error) {
        console.error('Error displaying prayer times:', error);
    }
}

// Call the main function when the page finishes loading
window.addEventListener('load', displayISNA);