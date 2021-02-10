# Strava_data_transfer
#### Transferring workouts from ".gpx", ".tcx", "json" or ".csv" files to Strava.<br>

While transferring my workouts from Endomondo and Runkeeper to Strava, I am facing problems, so I decided to create my own program.
First, you need to edit in accordance with your tasks, and separately run parsing_<type_of_file>.py to examine the files that need to be uploaded to the Strava.
Next, you need to get an access token for the Strava API and create your application according to the instructions - [Getting Started with the Strava API](https://developers.strava.com/docs/getting-started/).
Finally, edit and run the main.py file to start loading the activities.
