# Imports
from datetime import datetime
import csv

# Revenue today
def revenue_today(todays_date):
    revenue = 0

    # Increase revenue with sell price amount and print
    with open("sold.csv", "r") as csv_file:
        csv_sold = csv.reader(csv_file)
        next(csv_file)
        for row_sold in csv_sold:
            sell_date = datetime.strptime(row_sold[2], "%Y-%m-%d").date()
            if sell_date == todays_date:
                revenue += float(row_sold[3]) * int(row_sold[4])
    
    print("Today's revenue is: " + str(revenue))

# Revenue yesterday
def revenue_yesterday(yesterdays_date):
    revenue = 0
    
    # Increase revenue with sell price amount
    with open("sold.csv", "r") as csv_file:
        csv_sold = csv.reader(csv_file)
        next(csv_file)
        for row_sold in csv_sold:
            sell_date = datetime.strptime(row_sold[2], "%Y-%m-%d").date()
            if sell_date == yesterdays_date:
                revenue += float(row_sold[3]) * int(row_sold[4])

    print("Yesterday's revenue is: " + str(revenue))

# Revenue specific date, month or year
def revenue_date(date):
    revenue = 0

    # Date format YYYY-MM-DD to report specific date
    try:
        year_month_day = datetime.strptime(date, "%Y-%m-%d").strftime("%d %B, %Y")

        # Increase revenue with sell price amount
        with open("sold.csv", "r") as csv_file:
            csv_sold = csv.reader(csv_file)
            next(csv_file)
            for row_sold in csv_sold:
                sell_date = datetime.strptime(row_sold[2], "%Y-%m-%d").strftime("%Y-%m-%d")
                if sell_date == date:
                    revenue += float(row_sold[3]) * int(row_sold[4])

        print("The revenue on " + year_month_day + " is: " + str(revenue))

    # Date format YYYY-MM to report specific year and month
    except ValueError:
        try:
            year_month = datetime.strptime(date, "%Y-%m").strftime("%B, %Y")

            # Increase revenue with sell price amount
            with open("sold.csv", "r") as csv_file:
                csv_sold = csv.reader(csv_file)
                next(csv_file)
                for row_sold in csv_sold:
                    sell_date = datetime.strptime(row_sold[2], "%Y-%m-%d").strftime("%Y-%m")
                    if sell_date == date:
                        revenue += float(row_sold[3]) * int(row_sold[4])
            
            print("The revenue in " + year_month + " is: " + str(revenue))

        # Date format YYYY to report specific year
        except ValueError:
            year = datetime.strptime(date, "%Y").strftime("%Y")

            # Increase revenue with sell price amount
            with open("sold.csv", "r") as csv_file:
                csv_sold = csv.reader(csv_file)
                next(csv_file)
                for row_sold in csv_sold:
                    sell_date = datetime.strptime(row_sold[2], "%Y-%m-%d").strftime("%Y")
                    if sell_date == date:
                        revenue += float(row_sold[3]) * int(row_sold[4])

            print("The revenue in " + year + " is: " + str(revenue))
