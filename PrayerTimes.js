async function getPrayerTimes() {
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
            //Create Prayer Times Table
            const prayer_times_dict = {}
            //For Every Row get Prayer Times
            for(const row in data.data) {
                date_x = data.data[row].date.readable
                prayer_times = data.data[row].timings
                prayer_times_dict[date_x] = prayer_times
            }
            //Return Prayer Times
            return(prayer_times_dict)
        } else {
            console.error('Failed to fetch Islamic Prayer Times.');
            return null;
        }
    } catch (error) {
        console.error('Error fetching Islamic Prayer Times:', error);
        return null;
    }
}