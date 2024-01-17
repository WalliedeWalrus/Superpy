# Imports
from datetime import datetime
import csv

# Profit today
def profit_today(todays_date):
    profit = 0

    # Increase profit with sell price amount 
    with open("sold.csv", "r") as csv_file:
        csv_sold = csv.reader(csv_file)
        next(csv_file)
        for row_sold in csv_sold:
            sell_date = datetime.strptime(row_sold[2], "%Y-%m-%d").date()
            if sell_date == todays_date:
                profit += float(row_sold[3]) * int(row_sold[4])

                # Decrement profit with buy price amount
                with open("bought.csv", "r") as csv_file:
                    csv_bought = csv.reader(csv_file)
                    for row_bought in csv_bought:
                        if row_sold[1] == row_bought[0]:
                            profit -= float(row_bought[3]) * int(row_sold[4])
    
    print("Today's profit is: " + str(profit))

# Profit yesterday
def profit_yesterday(yesterdays_date):
    profit = 0
    # Increase profit with sell price amount
    with open("sold.csv", "r") as csv_file:
        csv_sold = csv.reader(csv_file)
        next(csv_file)
        for row_sold in csv_sold:
            sell_date = datetime.strptime(row_sold[2], "%Y-%m-%d").date()
            if sell_date == yesterdays_date:
                profit += float(row_sold[3]) * int(row_sold[4])

                # Lower profit with buy price amount
                with open("bought.csv", "r") as csv_file:
                    csv_bought = csv.reader(csv_file)
                    for row_bought in csv_bought:
                        if row_sold[1] == row_bought[0]:
                            profit -= float(row_bought[3]) * int(row_sold[4])

    print("Yesterday's profit is: " + str(profit))

# Profit specific date, month or year
def profit_date(date):
    profit = 0

    # Date format YYYY-MM-DD to report specific date
    try:
        year_month_day = datetime.strptime(date, "%Y-%m-%d").strftime("%d %B, %Y")

        # Increase profit with sell price amount
        with open("sold.csv", "r") as csv_file:
            csv_sold = csv.reader(csv_file)
            next(csv_file)
            for row_sold in csv_sold:
                sell_date = datetime.strptime(row_sold[2], "%Y-%m-%d").strftime("%Y-%m-%d")
                if sell_date == date:
                    profit += float(row_sold[3]) * int(row_sold[4])

                    # Lower profit with buy price amount
                    with open("bought.csv", "r") as csv_file:
                        csv_bought = csv.reader(csv_file)
                        for row_bought in csv_bought:
                            if row_sold[1] == row_bought[0]:
                                profit -= float(row_bought[3]) * int(row_sold[4])

        print("The profit on " + year_month_day + " is: " + str(profit))

    # Date format YYYY-MM to report specific year and month
    except ValueError:
        try:
            year_month = datetime.strptime(date, "%Y-%m").strftime("%B, %Y")

            # Increase profit with sell price amount
            with open("sold.csv", "r") as csv_file:
                csv_sold = csv.reader(csv_file)
                next(csv_file)
                for row_sold in csv_sold:
                    sell_date = datetime.strptime(row_sold[2], "%Y-%m-%d").strftime("%Y-%m")
                    if sell_date == date:
                        profit += float(row_sold[3]) * int(row_sold[4])

                        # Lower profit with buy price amount
                        with open("bought.csv", "r") as csv_file:
                            csv_bought = csv.reader(csv_file)
                            for row_bought in csv_bought:
                                if row_sold[1] == row_bought[0]:
                                    profit -= float(row_bought[3]) * int(row_sold[4])
            
            print("The profit in " + year_month + " is: " + str(profit))

        # Date format YYYY to report specific year
        except ValueError:
            year = datetime.strptime(date, "%Y").strftime("%Y")

            # Increase profit with sell price amount
            with open("sold.csv", "r") as csv_file:
                csv_sold = csv.reader(csv_file)
                next(csv_file)
                for row_sold in csv_sold:
                    sell_date = datetime.strptime(row_sold[2], "%Y-%m-%d").strftime("%Y")
                    if sell_date == date:
                        profit += float(row_sold[3]) * int(row_sold[4])

                        # Lower profit with buy price amount
                        with open("bought.csv", "r") as csv_file:
                            csv_bought = csv.reader(csv_file)
                            for row_bought in csv_bought:
                                if row_sold[1] == row_bought[0]:
                                    profit -= float(row_bought[3]) * int(row_sold[4])

            print("The profit in " + year + " is: " + str(profit))
