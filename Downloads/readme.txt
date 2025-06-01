Overview:
This Python application fetches air quality data from the OpenAQ API, processes it using an ETL (Extract, Transform, Load) pipeline, and stores it in a local SQLite database (openaq_data.db). You can use this script with real-world API data or simulate bad data for testing purposes.

Contents:

air_quality.py — Main script to run the ETL process.

test_data.json — A file containing malformed or incomplete data to test the error handling in the ETL pipeline.

openaq_data.db — SQLite database created by the ETL script (generated after running the script).

README.txt — This guide.

Setup Requirements:

Python 3.7+

Required libraries: requests, sqlite3, json, logging
(You can install missing packages using pip if needed.)

Running the ETL Application:

Step 1 — Clone or copy all files into a working directory.

Step 2 — Add your OpenAQ API key

Open the script air_quality.py in a code editor. At the top of the file, locate this line:

API_KEY = "YOUR_API_KEY_HERE"

Replace it with your actual OpenAQ API key:

API_KEY = "76859ede51b63437d136f69dabafc99343f4db68f23e001cd78b20079880c934"

Step 3 — Confirm the base API endpoint

Make sure the API URL used in the script is correct:

url = f"https://api.openaq.org/v3/locations/{location_id}"

(If OpenAQ changes their endpoint structure, update this URL accordingly.)

Step 4 — Run the script with real data

You can provide a list of real location IDs to fetch their data from the API. Example:

if name == "main":
location_ids = [2178, 1106, 1049] # Use actual location IDs
run_etl(location_ids, test_mode=False)

To run the script:

$ python air_quality.py

The script will:

Fetch the data from OpenAQ API for each location ID

Handle API errors like 404 Not Found or rate limits

Clean and transform the data

Save the data into openaq_data.db

Step 5 — Test the ETL with bad data

To simulate how the script handles invalid or missing data, you can use the test_data.json file. It contains incomplete or malformed data.

To enable test mode, modify the script’s main block like this:

if name == "main":
location_ids = [2178] # Location ID used as a reference in test data
run_etl(location_ids, test_mode=True)

Make sure test_data.json is in the same directory as air_quality.py.

When test_mode=True is set:

The script will load the JSON data from test_data.json instead of making an API call.

Missing or null fields will be handled and logged.

The data will still be cleaned and inserted into the database.

Logs:

All actions, warnings, and errors are logged to the console and can be viewed in real time.

Expected logs include:

INFO - Processing location ID: 2178

WARNING - Missing provider for location 2178, defaulting to "Unknown"

ERROR - Failed to fetch location: HTTP 404

Viewing the Database:

After running the script, openaq_data.db will be created in the same directory. You can inspect the data using tools like:

DB Browser for SQLite (https://sqlitebrowser.org)

SQLite CLI: $ sqlite3 openaq_data.db

Python sqlite3 module

Troubleshooting:

If the script fails with FileNotFoundError for test_data.json, ensure the file is in the correct directory.

If you receive a 404 from the API, check the location ID or the API URL.

If data doesn’t appear in the database, confirm test_mode is set appropriately and the database file is not locked or in use by another program.

Final Notes:

This ETL application was built for educational purposes and demonstrates how to fetch, clean, and store environmental data. Feel free to adapt it for other APIs or data pipelines.

—

For questions or bugs, contact: bengorarmohamed@gmail.com
