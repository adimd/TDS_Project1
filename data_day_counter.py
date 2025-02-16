import datetime

def parse_date(date_str):
    """Parse a date string into a datetime object using multiple formats."""
    for fmt in ("%d-%b-%Y", "%Y/%m/%d %H:%M:%S", "%b %d, %Y", "%Y-%m-%d", "%d-%b-%Y", "%Y/%m/%d"):
        try:
            return datetime.datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    raise ValueError(f"Date format not supported: {date_str}")

def count_weekday(parameters):
    """
    Count the occurrences of a specific weekday in the dates from the source file.
    Save the count to the destination file.
    """
    source_location = parameters.get('source location')
    destination_location = parameters.get('destination location')
    day = parameters.get('day')

    # Map day names to their corresponding weekday numbers (all lowercase)
    day_map = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6
    }
    
    # Convert the input day to lowercase for case-insensitive comparison
    day_lower = day.lower()

    # Check if the day is valid
    if day_lower not in day_map:
        raise ValueError(f"Invalid day: {day}. Must be one of {list(day_map.keys())}.")

    # Get the corresponding weekday number
    target_weekday = day_map[day_lower]

    # Read dates from the source file
    try:
        with open(source_location, 'r') as file:
            dates = file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"Source file not found: {source_location}")

    # Count occurrences of the target weekday
    weekday_count = 0
    for date_str in dates:
        try:
            date_obj = parse_date(date_str)
            if date_obj.weekday() == target_weekday:
                weekday_count += 1
        except ValueError as e:
            print(f"Skipping invalid date: {date_str.strip()} - {e}")

    # Write the count to the destination file
    try:
        with open(destination_location, 'w') as file:
            file.write(f"Total {day_lower.capitalize()}s: {weekday_count}\n")
    except IOError:
        raise IOError(f"Could not write to destination file: {destination_location}")

    return weekday_count

