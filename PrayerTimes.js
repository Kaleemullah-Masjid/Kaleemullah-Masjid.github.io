async function formatDate(date, format = 'DD-MM-YYYY') {
    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based, so add 1
    const year = date.getFullYear();
    const month_str = months[date.getMonth()];
    ///////////////
    // MMM Month
    ///////////////
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
async function get_islamic_data() {
    //Get Today's Date
    const today = new Date();
    const year = today.getFullYear();
    const month = today.getMonth() + 1; // Months are zero-based, so add 1
    //Kaleemullah Masjid Lat & Long
    const lat = 42.03326482384257;
    const long = -87.73497403508489;
    //Prayer Time EndPoint
    //Example Request:  http://api.aladhan.com/v1/calendar/2017/4?latitude=51.508515&longitude=-0.1254872&method=2
    const apiUrl = `https://api.aladhan.com/v1/calendar/${year}/${month}?latitude=${lat}&longitude=${long}&school=1`;

    try {
        //Fetch Response
        const response = await fetch(apiUrl);
        //Collect Response Data
        const data = await response.json();
        //Check to see if Good Response 
        if (response.ok && data.code === 200) {
            //Return Data
            return (data.data);
        } else {
            console.error('Failed to fetch Islamic Prayer Times.');
            return null;
        }
    } catch (error) {
        console.error('Error fetching Islamic Prayer Times:', error);
        return null;
    }
}
async function get_Prayer_Times(data) {
    //Create Prayer Times Table
    const prayer_times_dict = {}
    //For Every Row get Prayer Times
    for(const row in data) {
        date_x = data[row].date.readable
        prayer_times = data[row].timings
        prayer_times_dict[date_x] = prayer_times
    }
    //Return Prayer Times
    return(prayer_times_dict)
}
async function get_Islamic_Dates(data) {
    //Create Prayer Times Table
    const prayer_times_dict = {}
    //For Every Row get Prayer Times
    for(const row in data) {
        date_x = data[row].date.readable
        prayer_times = data[row].date.hijri
        prayer_times_dict[date_x] = prayer_times
        prayer_times_dict[date_x]['MONTH_ENG'] = data[row].date.hijri.designation.expanded
        prayer_times_dict[date_x]['MONTH_ENG'] = data[row].date.hijri.month.en
        prayer_times_dict[date_x]['MONTH_ARABIC'] = data[row].date.hijri.month.ar
        prayer_times_dict[date_x]['WEEKDAY_ENG'] = data[row].date.hijri.weekday.en
        prayer_times_dict[date_x]['WEEKDAY_ARABIC'] = data[row].date.hijri.month.ar
    }
    //Return Prayer Times
    return(prayer_times_dict)
}
function armyTimeToAMPM(armyTime) {
    const [hour, minute] = armyTime.split(':').map(Number);
    const period = hour >= 12 ? 'PM' : 'AM';
    const hour12 = hour % 12 || 12;
    return `${hour12}:${minute.toString().padStart(2, '0')} ${period}`;
}
function convertTimesToAMPM(timesObject) {
    const convertedTimes = {};
    for (const date in timesObject) {
        convertedTimes[date] = {};
        for (const prayer in timesObject[date]) {
            const armyTime = timesObject[date][prayer].split(' ')[0];
            const ampmTime = armyTimeToAMPM(armyTime);
            convertedTimes[date][prayer] = `${ampmTime}`;
        }
    }
    return convertedTimes;
}
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
// Function to display the sunrise and sunset times on the HTML page
function displayHijriDate(Today_Hijri_Date, Today_Date) {
    const Hijri_date_Cell = document.getElementById('Hijri');
    Hijri_date_Cell.innerHTML = `<b>Today is: </b> ${Today_Date} || ${Today_Hijri_Date}`;   
}
// Function to display the sunrise and sunset times on the HTML page
function displayISNA(prayer_times) {
    const FAJR_ISNA = document.getElementById('FAJR_ISNA');
    const SUNRISE_ISNA = document.getElementById('SUNRISE_ISNA');
    const ZUHR_ISNA = document.getElementById('ZUHR_ISNA');
    const ASR_ISNA = document.getElementById('ASR_ISNA');
    const MAGRHEB_ISNA = document.getElementById('MAGRHEB_ISNA');
    const ISHA_ISNA = document.getElementById('ISHA_ISNA');
    FAJR_ISNA.textContent = prayer_times['Fajr'];
    SUNRISE_ISNA.textContent = prayer_times['Sunrise'];
    ZUHR_ISNA.textContent = prayer_times['Dhuhr'];
    ASR_ISNA.textContent = prayer_times['Asr'];
    MAGRHEB_ISNA.textContent = prayer_times['Sunset'];
    ISHA_ISNA.textContent = prayer_times['Isha'];
    
}
// Function to display the sunrise and sunset times
async function loadSunriseSunsetData() {
    const sunriseSunsetData = await getSunriseSunsetTime();
    const Islamic_Data = await get_islamic_data();
    const Prayer_Times_Army = await get_Prayer_Times(Islamic_Data);
    const Prayer_Times_AM_PM = convertTimesToAMPM(Prayer_Times_Army);
    const Islamic_Dates = await get_Islamic_Dates(Islamic_Data);
    const today = new Date();
    today_str = await formatDate(today, format='DD MMM YYYY');
    Today_Date = await formatDate(today, format='DD-MMM-YYYY');

    const Today_Prayer_Times = await Prayer_Times_AM_PM[today_str];
    const Today_Islamic_Dates = await Islamic_Dates[today_str];

    if (sunriseSunsetData) {
        if (Today_Islamic_Dates) {
            const sunriseTime = new Date(sunriseSunsetData.sunrise).toLocaleTimeString();
            const sunsetTime = new Date(sunriseSunsetData.sunset).toLocaleTimeString();
            const Today_Hijri_Date = `${Today_Islamic_Dates.day}-${Today_Islamic_Dates.MONTH_ENG}-${Today_Islamic_Dates.year}`
            //console.log(Today_Prayer_Times)
            //console.log(Today_Islamic_Dates)
            displayHijriDate(Today_Hijri_Date,Today_Date);
            displaySunriseSunsetTimes(sunriseTime, sunsetTime);
            displayISNA(Today_Prayer_Times);
        } else {
            console.log('Unable to fetch Islamic Date data.');
        }
        
    } else {
            console.log('Unable to fetch sunrise-sunset data.');
    }
}

// Call the main function when the page finishes loading
window.addEventListener('load', loadSunriseSunsetData);