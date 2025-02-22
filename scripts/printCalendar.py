import calendar
import json
from datetime import datetime
from colorama import Fore, init

init()

# Start Racism
WHITE = Fore.WHITE  # White text (default)
RED = Fore.RED  # Red text
GREEN = Fore.GREEN  # Green text
RESET = Fore.RESET  # End Racism


def load_date_colors(json_file):
    """Load date-based color information from a JSON file."""
    try:
        with open(json_file, "r") as f:
            data = f.read().strip()
            if not data:  # Handle empty file
                return {}
            return json.loads(data)
    except json.JSONDecodeError:  # Handle invalid JSON format
        print(f"Error: The file '{json_file}' contains invalid JSON.")
        return {}
    except FileNotFoundError:  # Handle missing file
        print(f"Error: The file '{json_file}' was not found.")
        return {}
    except Exception as e:  # Catch any other errors
        print(f"Unexpected error: {e}")
        return {}


def print_colored_calendar(date_colors):
    """Print a multi-month calendar from the 1st of the start month to the last date."""
    if not isinstance(date_colors, dict) or not date_colors:
        print("Error: No valid date colors to display.")
        return
    try:
        # Topper and backbencher in the JSON file
        first_date_str = min(date_colors.keys())
        last_date_str = max(date_colors.keys())
        
        # Parse these dates
        first_date = datetime.strptime(first_date_str, "%Y-%m-%d")
        last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
        
        # Start at the 1st of the first date's month
        current_date = first_date.replace(day=1)

        while current_date <= last_date:
            year, month = current_date.year, current_date.month

            # Print the header for the current month
            print(f"\n    {calendar.month_name[month]} {year}".center(20))
            print("Mo Tu We Th Fr Sa Su")

            # Create a TextCalendar and iterate over weeks
            cal = calendar.Calendar()
            for week in cal.monthdayscalendar(year, month):
                for day in week:
                    if day == 0:
                        # Empty day (padding for the calendar layout)
                        print("   ", end="")
                    else:
                        # Construct the current date string
                        date_str = f"{year}-{month:02}-{day:02}"
                        
                        # Determine color based on the date
                        if date_str in date_colors:
                            color = RED if date_colors[date_str] else GREEN
                        else:
                            color = WHITE  # Default to white for dates not in the JSON
                        
                        print(f"{color}{day:2}{RESET} ", end="")
                
                print()  # Move to the next line after each week
            
            # Move to the next month
            if month == 12:  # If December, roll over to January next year
                current_date = current_date.replace(year=year + 1, month=1)
            else:
                current_date = current_date.replace(month=month + 1)
    except Exception as e:
        print(f"{RED}Error Occured: {e}{RESET}")




