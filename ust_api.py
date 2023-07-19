import requests
import glob
import os
import pandas as pd
from datetime import datetime, timedelta, date
import time

def get_most_recent_date():

    folder_path = "raw_data/"

    # Use glob to find all files with the naming convention "ust_aq_timeseries_*.csv"
    csv_files = glob.glob(os.path.join(folder_path, "ust_aq_timeseries_*.csv"))

    # Extract years from the file names and find the file with the highest year
    max_year = max(int(filename.split("_")[4].split(".")[0]) for filename in csv_files)
    file_with_max_year = f"ust_aq_timeseries_{max_year}.csv"

    # Read the most recent file and find the most recent date
    file_path = os.path.join(folder_path, file_with_max_year)
    df = pd.read_csv(file_path)

    # Extract the most recent date
    dates = pd.to_datetime(df['endtime'], format="%Y-%m-%d %H:%M:%S")
    most_recent_date = dates.max()

    print(f"The most recent date is: {most_recent_date.date()}")

    return most_recent_date

def create_dates_list(most_recent_date):
    end_date = datetime.now().date()

    # Create a list of dates between start_date and most_recent_date (excluding most_recent_date)
    date_list = []
    current_date = most_recent_date + timedelta(days=1)  # Skip the start date
    while current_date < end_date:
        date_list.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)

    print('Date list complete')

    return date_list

def get_new_data(date_list):
    print(f"Retrieving data for {len(date_list)} dates")
    if len(date_list) == 0:
        print('No new dates')
    else:

        for index, single_date in enumerate(date_list):
            url = f"https://api.ust.is/aq/a/getDate/date/{single_date}"
            stations = requests.get(url).json()

            rows =[]
            for station_local_id, elements in stations.items():
                for pollutantnotation, times in elements['parameters'].items():
                    for key, data in times.items():
                        if not isinstance(data, str):

                            validity = 1
                            if data['value'] == None:
                                validity = None

                            row = {
                                "station_name": elements['name'],
                                "pollutantnotation": pollutantnotation,
                                "endtime": data['endtime'],
                                "the_value": data['value'],
                                "resolution": times['resolution'],
                                "verification": data['verification'],

                                "validity": validity,
                                "station_local_id": elements['local_id'],
                                "concentration": times['unit'],

                            }
                            rows.append(row)

            df = pd.DataFrame(rows)

            year = df['endtime'][0][:4]
            file_name = f"ust_aq_timeseries_{year}.csv"
            folder_path = "raw_data/"

            file_path = os.path.join(folder_path, file_name)

            if os.path.isfile(file_path):
                df.to_csv(file_path, mode='a', index=False, header=False)
            else:
                df.to_csv(file_path, mode='w' ,index=False)

            time.sleep(1)

            if index % 50 == 0:
                print(f"{index} out of {len(date_list)} complete!")


most_recent_date = get_most_recent_date()
date_list = create_dates_list(most_recent_date)
get_new_data(date_list)
