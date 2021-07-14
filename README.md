# README

## Purpose
This script can be used to set every instance of a GTFS `trip_id` to the `trip_short_name` found in the feed's `trips.txt` file.

## Usage 
Tested with Python 2.7 and 3.9.
`python shortname-to-tripid.py feed.zip`
The script will run automatically. Adjusted files are exported to the current directory for human review before manually adding to the feed's .zip file.

## Notes 
- If a trip does not have a `trip_short_name`, the corresponding `trip_id` will not be adjusted elsewhere. 
- If a `trip_short_name` is seen multiple times, the script will stop execution to avoid reusing it as a trip ID. When used with feeds exported from Trillium's GTFS Manager, this could be a sign that a previous or upcoming calendar needs to be removed.
- Currently alters `trip_id` in `trips.txt`, `stop_times.txt`, and `frequencies.txt` and `start_trip_id` and `end_trip_id` in `runcut.txt`. 