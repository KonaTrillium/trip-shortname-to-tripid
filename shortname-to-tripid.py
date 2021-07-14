import zipfile, sys, os, csv, io

COLOR_RED   = "\033[1;31m"
COLOR_BLUE  = "\033[1;34m"
COLOR_GREEN = "\033[0;32m"
COLOR_RESET = "\033[0;0m"

def convert_feed_tripids():
    if len(sys.argv) < 2:
        print(COLOR_RED + "No filename provided!" + COLOR_RESET)
        exit()
    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
        print(COLOR_RED + "File does not exist!" + COLOR_RESET)
    gtfs_zipped = zipfile.ZipFile(filepath)
    tripid_map = make_tripid_map(gtfs_zipped)
    if len(tripid_map) == 0:
        print(COLOR_RED + "No trip_short_names found! Exiting..." + COLOR_RESET)
        exit()
    files_with_tripid = ["frequencies.txt", "stop_times.txt", "trips.txt"]
    files_with_different_field_name = [["runcut.txt", ["start_trip_id", "end_trip_id"]]]
    for file in files_with_tripid:
        make_new_file(gtfs_zipped, file, tripid_map)
    for file in files_with_different_field_name:
        make_new_file(gtfs_zipped, file[0], tripid_map, file[1])

def make_tripid_map(gtfs):
    trip_id_map = {}
    with gtfs.open("trips.txt", "r") as trips_file_raw:
        trips_file = io.TextIOWrapper(trips_file_raw)
        trips_csv = csv.DictReader(trips_file)
        seen_trip_names = set()
        for row in trips_csv:
            if "trip_short_name" not in row or not row["trip_short_name"]:
                print(COLOR_BLUE + "no trip_short_name for trip " + row['trip_id'] + ", will not be replaced" + COLOR_RESET)
                continue
            if row["trip_short_name"] in seen_trip_names:
                print(COLOR_RED + "trip_short_name " + row['trip_short_name'] + " has already been seen! Will not create duplicates. Exiting..." + COLOR_RESET)
                exit()
            trip_id_map[row['trip_id']] = row['trip_short_name']
            seen_trip_names.add(row['trip_short_name'])
    return trip_id_map

def make_new_file(gtfs, file_name, tripid_map, field_names=["trip_id"]):
    with gtfs.open(file_name, "r") as file_raw:
        file = io.TextIOWrapper(file_raw)
        csvfile = csv.DictReader(file)
        if os.path.exists(file_name):
            print(COLOR_RED + "File with name " + file_name + " already exists in directory; cannot create a new one. Move this file and try again. Skipping..." + COLOR_RESET)
            return
        new_file = open(file_name, "w")
        new_csv_writer = csv.DictWriter(new_file, fieldnames=csvfile.fieldnames)
        new_csv_writer.writeheader()
        for row in csvfile:
            row_copy = row.copy()
            for field_name in field_names:
                if row[field_name] not in tripid_map:
                    print(COLOR_BLUE + "Invalid field name " + field_name + " for file " + file_name + ", skipping this file" + COLOR_RESET)
                    return
                found_tripid = row_copy[field_name]
                row_copy[field_name] = tripid_map[found_tripid] if found_tripid in tripid_map else found_tripid
            new_csv_writer.writerow(row_copy)
        new_file.close()
        print(COLOR_GREEN + "Exported " + file_name + " with every " + ",".join(field_names) + " set to the trip_short_name" + COLOR_RESET)

if __name__ == "__main__":
    convert_feed_tripids()