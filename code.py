"""
Project for Week 4 of "Python Programming Essentials".
This script contains functions to calculate information about dates.
"""

def is_leap(year):
    """
    Helper function to determine if a year is a leap year.
    A year is a leap year if it is divisible by 4,
    except for end-of-century years, which must be divisible by 400.
    """
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def days_in_month(year, month):
    """
    Takes a year and a month as input and returns the number of days in
    that month. It correctly handles leap years for February.
    """
    if month == 2:
        if is_leap(year):
            return 29
        else:
            return 28
    elif month in [4, 6, 9, 11]:
        return 30
    else:
        return 31

def is_valid_date(year, month, day):
    """
    Takes a year, month, and day as input and returns True if the date is valid,
    and False otherwise.
    """
    # Check if types are integers, breaking the line for style
    if not (isinstance(year, int) and isinstance(month, int) and
            isinstance(day, int)):
        return False
        
    # Check if year and month are within a valid range (1-9999 for year).
    # This fixes the bug with year 12000.
    if not (1 <= year <= 9999 and 1 <= month <= 12):
        return False
    
    # Check if the day is valid for the given month and year
    days_in_the_month = days_in_month(year, month)
    if not (1 <= day <= days_in_the_month):
        return False
        
    return True

def days_between(year1, month1, day1, year2, month2, day2):
    """
    Takes two dates as input and returns the number of days between them.
    Returns 0 if the second date is earlier than the first.
    """
    if not is_valid_date(year1, month1, day1) or \
       not is_valid_date(year2, month2, day2):
        return 0
        
    # If the second date is before the first, return 0.
    # This fixes the bug where it returned 1 instead of 0.
    if (year2, month2, day2) < (year1, month1, day1):
        return 0
 
    days = 0
    
    # Create a mutable copy of the start date
    current_year, current_month, current_day = year1, month1, day1

    # Iterate day by day from the start date to the end date
    while (current_year, current_month, current_day) < (year2, month2, day2):
        days += 1
        current_day += 1
        
        # Check if the month needs to be incremented
        if current_day > days_in_month(current_year, current_month):
            current_day = 1
            current_month += 1
            
            # Check if the year needs to be incremented
            if current_month > 12:
                current_month = 1
                current_year += 1
                
    return days

def age_in_days(year, month, day):
    """
    Takes a birthdate as input and returns the person's age in days
    as of today.
    """
    # Import the datetime module to get today's date
    import datetime
    today = datetime.date.today()
    
    # Get today's year, month, and day
    today_year = today.year
    today_month = today.month
    today_day = today.day
    
    # Check for invalid birthdate or a birthdate in the future
    if not is_valid_date(year, month, day) or \
       (year, month, day) > (today_year, today_month, today_day):
        return 0
    
    # Calculate the days between the birthdate and today
    return days_between(year, month, day, today_year, today_month, today_day)
