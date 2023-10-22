async function fetchData() {
    try {
        // Fetch the SQLite database file
        const response = await fetch('https://github.com/Kaleemullah-Masjid/Kaleemullah-Masjid.github.io/blob/main/Data/Weather_Data/Weather_Data.db');
        const buffer = await response.arrayBuffer();

        // Load the database
        const db = await SQL.open({ buffer });

        // Perform a query
        const result = await db.exec('SELECT * From Weather_Forcast');

        // Handle the result
        console.log(result);
    } catch (error) {
        console.error('Error:', error);
    }
}

// Call the function to initiate the process
fetchData();