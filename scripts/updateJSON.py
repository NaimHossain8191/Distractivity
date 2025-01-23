import json
from datetime import datetime, timedelta


# pull the data from the file
def load_days(days_file):
    try:
        with open(days_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # File not found? We create it! ✨
        with open(days_file, "w") as file:
            json.dump({}, file)
        return {}

# push the data to the file
def save_days(data, days_file):
    with open(days_file, "w") as file:
        json.dump(data, file, indent=4)

def sort_days(data):
    # no chaos here 📅
    return {date: data[date] for date in sorted(data.keys())}

# Fill in the missing dates, no skipping 🗓️
def fill_missing_days(data):
    if not data:
        return {}

    sorted_dates = sorted(data.keys())
    start_date = datetime.strptime(sorted_dates[0], "%Y-%m-%d")
    end_date = datetime.now() - timedelta(days=1)

    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        if date_str not in data:
            data[date_str] = False
        current_date += timedelta(days=1)

    return data

# "Gotcha, you used socials today"
def update_today(data, value):
    today_str = datetime.now().strftime("%Y-%m-%d")
    if today_str not in data and value == True:
        data[today_str] = value
    return data

# Let's start cooking
def update_json(json_file, today_value):
    # Pull data
    days_data = load_days(json_file)

    # Fill all gaps
    days_data = fill_missing_days(days_data)

    # Sort dates
    days_data = sort_days(days_data)

    days_data = update_today(days_data, today_value)

    # Push the updated data
    save_days(days_data, json_file)