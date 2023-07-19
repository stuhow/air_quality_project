import requests
import glob
import os
import pandas as pd
from datetime import datetime, timedelta, date

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

    print(date_list[:10])

def get_new_data():
    pass

most_recent_date = get_most_recent_date()
create_dates_list(most_recent_date)
