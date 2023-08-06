import re
from datetime import datetime, timedelta
from calendar import monthrange
import zipfile
import os

def convert_date(date_string):
    # Parse the date string
    if len(date_string) == 4:
        date = datetime.strptime(date_string, "%Y")
        # Set the date to the first day of the year
        date = date.replace(day=1, month=1)
    elif len(date_string) == 7:
        date = datetime.strptime(date_string, "%Y-%m")
        # Set the date to the first day of the month
        date = date.replace(day=1)
    elif len(date_string) == 10:
        date = datetime.strptime(date_string, "%Y-%m-%d")
        return date.date()
        # Check if the day is not set
        if date.day == 1:
            # Set the date to the first day of the month
            date = date.replace(day=1)
        else:
            # Set the date to the last day of the month
            _, last_day = monthrange(date.year, date.month)
            date = date.replace(day=last_day)
    return date.date()

def get_next_date(date_string):
    if len(date_string) == 4:
        # Get the first day of the next year
        year = int(date_string) + 1
        next_date = datetime(year, 1, 1).date()
    elif len(date_string) == 7:
        # Get the first day of the next month
        year, month = map(int, date_string.split('-'))
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
        next_date = datetime(year, month, 1).date()
    elif len(date_string) == 10:
        # Get the next day
        current_date = datetime.strptime(date_string, "%Y-%m-%d").date()
        next_date = current_date + timedelta(days=1)
    else:
        raise ValueError("Invalid date format")

    # Get the minimum date between new date and current date
    min_date = min(next_date, datetime.now().date())
    return min_date

def extract_date(string):
    # Extract the date using regular expression
    date_match = re.search(r'\d{4}-\d{2}-\d{2}', string)

    if date_match:
        extracted_date = date_match.group(0)
        return datetime.strptime(extracted_date, "%Y-%m-%d").date()
    else:
        return datetime.now().date()

def match_date(string, start_date, end_date):
    date_match = re.search(r'\d{4}-\d{2}-\d{2}', string)
    if date_match:
        date_val = datetime.strptime(date_match.group(0), "%Y-%m-%d").date()
        return start_date <= date_val < end_date
    else:
        return False
    
def zip_files_with_condition(source_dir, destination_zip, start_date, end_date, exceptional_files=[]):
    with zipfile.ZipFile(destination_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if match_date(file, start_date, end_date) or file in exceptional_files:
                    zipf.write(file_path, os.path.relpath(file_path, source_dir))