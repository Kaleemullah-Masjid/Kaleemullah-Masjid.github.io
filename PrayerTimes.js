// main.js

// Function to format a date according to the specified format
function formatDate(date, format) {
    try {
        format = format || 'DD-MM-YYYY';
        var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        var day = String(date.getDate()).padStart(2, '0');
        var month = String(date.getMonth() + 1).padStart(2, '0');
        var year = date.getFullYear();
        var monthStr = months[date.getMonth()];

        switch (format) {
            case 'DD-MM-YYYY': return day + '-' + month + '-' + year;
            case 'MM/DD/YYYY': return month + '/' + day + '/' + year;
            case 'YYYY-MM-DD': return year + '-' + month + '-' + day;
            case 'YYYY/MM/DD': return year + '/' + month + '/' + day;
            case 'DD/MM/YYYY': return day + '/' + month + '/' + year;
            case 'DD MM YYYY': return day + ' ' + month + ' ' + year;
            case 'DD MMM YYYY': return day + ' ' + monthStr + ' ' + year;
            case 'MMM DD, YYYY': return monthStr + ' ' + day + ', ' + year;
            case 'YYYY MMM DD': return year + ' ' + monthStr + ' ' + day;
            case 'DD-MMM-YYYY': return day + '-' + monthStr + '-' + year;
            default: throw new Error('Unsupported format: ' + format);
        }
    } catch (error) {
        console.error('Error in formatDate:', error);
    }
}

// Function to format Islamic date
function formatIslamicDate(date) {
    try {
        var islamicMonths = {
            1: 'Muharram', 2: 'Safar', 3: 'Rabi al-Awwal', 4: 'Rabi al-Thani',
            5: 'Jumada al-Awwal', 6: 'Jumada al-Thani', 7: 'Rajab', 8: 'Shaban',
            9: 'Ramadan', 10: 'Shawwal', 11: 'Dhu al-Qadah', 12: 'Dhu al-Hijjah'
        };

        var parts = date.split('-');
        var day = parseInt(parts[0], 10);
        var month = parseInt(parts[1], 10);
        var year = parseInt(parts[2], 10);

        if (!islamicMonths[month]) throw new Error('Invalid Islamic month: ' + month);

        return day + '-' + islamicMonths[month] + '-' + year;
    } catch (error) {
        console.error('Error in formatIslamicDate:', error);
    }
}

// Function to parse CSV data and convert it into an array of objects
function parseCSV(csv) {
    try {
        var lines = csv.split('\n');
        var headers = lines[0].split(',');
        var data = [];

        for (var i = 1; i < lines.length; i++) {
            var values = lines[i].split(',');
            var entry = {};

            for (var j = 0; j < headers.length; j++) {
                entry[headers[j]] = values[j];
            }

            data.push(entry);
        }

        return data;
    } catch (error) {
        console.error('Error in parseCSV:', error);
    }
}

// Function to fetch CSV data from a GitHub URL
function fetchCsvFromGitHub() {
    var githubRawUrl = 'https://raw.githubusercontent.com/Kaleemullah-Masjid/Kaleemullah-Masjid.github.io/main/Data/PRAYER_TIMES/PRAYER_TIMES.csv';

    return fetch(githubRawUrl)
        .then(function (response) {
            if (!response.ok) throw new Error('Failed to fetch CSV file');
            return response.text();
        })
        .then(function (csvData) {
            var today = new Date();
            var todayStr = formatDate(today, 'DD MMM YYYY');
            var dataCsv = parseCSV(csvData);

            var filteredData = dataCsv.filter(function (entry) {
                return entry.Date === todayStr;
            });

            if (filteredData.length === 0) throw new Error('No prayer data available for today.');

            return filteredData;
        })
        .catch(function (error) {
            console.error('Error in fetchCsvFromGitHub:', error);
            return [];
        });
}

// Function to fetch sunrise and sunset times from an API
function getSunriseSunsetTime() {
    var latitude = 42.03326482384257;
    var longitude = -87.73497403508489;
    var apiKey = 'YOUR_API_KEY';
    var url = 'https://api.sunrise-sunset.org/json?lat=' + latitude + '&lng=' + longitude + '&date=today&formatted=0';

    return fetch(url)
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            return data.results;
        })
        .catch(function (error) {
            console.error('Error fetching sunrise-sunset data:', error);
            return null;
        });
}

// Function to display the sunrise and sunset times on the HTML page
function displaySunriseSunsetTimes() {
    getSunriseSunsetTime()
        .then(function (sunriseSunsetData) {
            if (!sunriseSunsetData) throw new Error('Sunrise-sunset data is unavailable.');

            var sunriseTime = new Date(sunriseSunsetData.sunrise).toLocaleTimeString();
            var sunsetTime = new Date(sunriseSunsetData.sunset).toLocaleTimeString();

            document.getElementById('sunriseTime').textContent = sunriseTime;
            document.getElementById('sunsetTime').textContent = sunsetTime;
        })
        .catch(function (error) {
            console.error('Error in displaySunriseSunsetTimes:', error);
        });
}

// Function to display the last Sunday of the month
async function displayLastSunday() {
    // Fetch the last Sunday of the month
    const lastSundayDate = await getLastSundayOfMonth();
    const lastSundayElement = document.getElementById("last-sunday");
    if (lastSundayElement) {
        lastSundayElement.textContent = `Join us every last Sunday of the month (${lastSundayDate}) after Maghrib prayer for a group Quran recitation.`;
    }
}

// Function to display prayer times and Islamic date on the HTML page
async function displayISNA() {
    try {
        // Fetch the last Sunday of the month
        await displayLastSunday();

        // Fetch sunrise and sunset times and prayer times
        await displaySunriseSunsetTimes();
        const prayer_temp = await fetchCsvFromGitHub();
        if (prayer_temp.length > 0) {
            //PULL FIRST ROW DATA
            const prayer_times = prayer_temp[0]
            //GET NEW ISLAMIC DATE
            const new_islamic_date = await formatIslamicDate(prayer_times['Islamic_Date'])
            //GET DOCUMENT IDs 
            const FAJR_ISNA = document.getElementById('FAJR_ISNA');
            const SUNRISE_ISNA = document.getElementById('SUNRISE_ISNA');
            const ZUHR_ISNA = document.getElementById('ZUHR_ISNA');
            const ASR_ISNA = document.getElementById('ASR_ISNA');
            const MAGRHEB_ISNA = document.getElementById('MAGRHEB_ISNA');
            const ISHA_ISNA = document.getElementById('ISHA_ISNA');
            const Hijri_date_cell = document.getElementById('Hijri');
            
            // Display prayer times and Islamic date
            Hijri_date_cell.innerHTML = `<b>Today is: </b> ${prayer_times['Date']} || ${new_islamic_date}`;
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

// Function to get the last Sunday of the month
async function getLastSundayOfMonth() {
    const today = new Date();
    const year = today.getFullYear();
    const month = today.getMonth() + 1; // Months are 0-based, so add 1
    const lastDayOfMonth = new Date(year, month, 0); // Get the last day of the current month
    const dayOfWeek = lastDayOfMonth.getDay(); // Get the day of the week (0 = Sunday, 6 = Saturday)
    const lastSunday = new Date(lastDayOfMonth);
    lastSunday.setDate(lastDayOfMonth.getDate() - dayOfWeek); // Subtract days to get the last Sunday
    return lastSunday.toDateString(); // Return the date as a string
}

// Call the main function when the page finishes loading
window.addEventListener('load', displayISNA);