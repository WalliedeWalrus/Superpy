# Imports
import argparse
import csv
from datetime import datetime
from rich.console import Console
from rich.table import Table
from datetime import date, datetime, timedelta
from revenue import revenue_today, revenue_yesterday, revenue_date
from profit import profit_today, profit_yesterday, profit_date

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
def main():
    pass

# Validate and return input date as a string
def validate_date(date):
    try:
        return datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        try: 
            return datetime.strptime(date, "%Y-%m").strftime("%Y-%m")
        except ValueError:
            try:
                return datetime.strptime(date, "%Y").strftime("%Y")
            except ValueError:
                message = "Sorry, this is not a valid date: {0!r}\n".format(date) + "Enter the date, month or year in this format: 'YYYY-MM-DD', 'YYYY-MM' and 'YYYY'."
                raise argparse.ArgumentTypeError(message)
            
# Validate and return datetime.date
def validate_specific_date(date):
    try:
        return datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
                message = "Sorry, this is not a valid date: {0!r}\n".format(date) + "Enter the date in this format: 'YYYY-MM-DD'."
                raise argparse.ArgumentTypeError(message)

# Create parser, argument and subparser
parser = argparse.ArgumentParser(prog="Python main.py", formatter_class=argparse.RawTextHelpFormatter, 
description="Welcome to the Superpy store.\n"
"From the command line you can buy or sell products, change the date and report the inventory, revenue and profit of the store.\n"
"Start each command with: Python main.py and then choose between 'buy', 'sell' or 'report'.\nYou can change the date with: '--advance_date', '--reverse_date', '--current_date' or '--set_date'")
parser.add_argument("--advance_date", type=int, help="Advance date by entered number.")
parser.add_argument("--reverse_date", type=int, help="Reverse date by entered number.")
parser.add_argument("--current_date", action="store_true", help="Changes date to current date.")
parser.add_argument("--set_date", type=validate_specific_date, help="Set a specific date. Date format is 'YYYY-MM-DD'.")
subparsers = parser.add_subparsers(dest="command")

# Subparse buy
buy_parser = subparsers.add_parser("buy", help="Buy a product. Required arguments are '--product_name', '--price', '--expiration_date' and '--amount'.")
buy_parser.add_argument("--product_name", type=str, required=True, help="The name of the product (use underscore if product name has multiple words).")
buy_parser.add_argument("--price", type=float, required=True, help="Buying price of the product. (Requires a number and accepts number after decimal point.)")
buy_parser.add_argument("--expiration_date", type=validate_specific_date, required=True, help="Expiration date of the product. The date format is 'YYYY-MM-DD'.")
buy_parser.add_argument("--amount", type=int, required=True, help="The amount of the product you want to buy.")

# Subparse sell
sell_parser =  subparsers.add_parser("sell", help="Sell a product. Required arguments are '--product_name', '--price' and '--amount'.")
sell_parser.add_argument("--product_name", type=str, required=True, help="Name of the product (use underscore if product name has multiple words).")
sell_parser.add_argument("--price", type=float, required=True, help="Requires number and accepts number after decimal point.")
sell_parser.add_argument("--amount", type=int, required=True, help="The amount of the product you want to sell.")


# Subparser report
report = subparsers.add_parser("report", help="Reports requested information. Choose between inventory, revenue or profit.")
subparsers_report = report.add_subparsers(dest="command")

# Report inventory
inventory_parser = subparsers_report.add_parser("inventory", help="Reports the products in inventory. Date arguments are '--today', '--yesterday' and '--date'.")
inventory_parser.add_argument("--today", action="store_true", help="Reports the products in inventory today.")
inventory_parser.add_argument("--yesterday", action="store_true", help="Reports the products in inventory yesterday.")
inventory_parser.add_argument("--date", type=validate_specific_date, help="Reports the products in inventory at a specific date. Date format is 'YYYY-MM-DD'.")

# Report revenue
revenue_parser = subparsers_report.add_parser("revenue", help="Reports revenue. Date arguments are '--today', '--yesterday', '--date'.")
revenue_parser.add_argument("--today", action="store_true", help="Reports today's revenue.")
revenue_parser.add_argument("--yesterday", action="store_true", help="Reports yesterday's revenue.")
revenue_parser.add_argument("--date", type=validate_date, help="Reports revenue for a specific date, month or year. Date format is 'YYYY-MM-DD', 'YYYY-MM' and 'YYYY'.")

# Report profit
profit_parser = subparsers_report.add_parser("profit", help="Reports profit. Date arguments are '--today', '--yesterday', '--date'.")
profit_parser.add_argument("--today", action="store_true", help="Reports today's profit.")
profit_parser.add_argument("--yesterday", action="store_true", help="Reports yesterday's profit.")
profit_parser.add_argument("--date", type=validate_date, help="Reports profit for a specific date, month or year. Date format is 'YYYY-MM-DD', 'YYYY-MM' and 'YYYY'.")

# Parse args
args = parser.parse_args()


# Open date txt
with open("date.txt", "r") as txt_file:
    time = txt_file.read()

# Change date
if args.advance_date:
    with open("date.txt", "w") as txt_file:
        txt_file.write(str(validate_specific_date(time) + timedelta(args.advance_date)))
    print("OK, date is advanced " + str(args.advance_date) + " day(s)")
if args.reverse_date:
    with open("date.txt", "w") as txt_file:
        txt_file.write(str(validate_specific_date(time) - timedelta(args.reverse_date)))
    print("OK, date is reversed " + str(args.reverse_date) + " day(s)")
if args.current_date:
    with open("date.txt", "w") as txt_file:
        txt_file.write(str(date.today()))
        current_date = date.today()
    print("OK, date is now current date ", current_date)
if args.set_date:
    with open("date.txt", "w") as txt_file:
        txt_file.write(str(args.set_date))
    print("OK, date is now "  + str(args.set_date))


# Date name variables
todays_date = datetime.strptime(time, "%Y-%m-%d").date()
yesterdays_date = todays_date - timedelta(1)

# Function buy product
def buy_product(product_name,price,expiration_date,amount,todays_date):
    with open("bought.csv", "a", newline="") as csv_file:
        bought_csv = csv.writer(csv_file)

        # Create last row id 
        with open("bought.csv", "r") as csv_file:
            rows_bought = list(csv.reader(csv_file))
        last_row_bought = rows_bought[-1]
        if last_row_bought[0] == "id":
            last_row_id = 0
        else: 
            last_row_id = last_row_bought[0]

        # Write command line to bought csv
        bought_csv.writerow([int(last_row_id) + 1,str.title(product_name).replace("_", " "),todays_date,"%.2f" % price,expiration_date,amount])
        print("OK, you have bought " + str (amount) +" " + str(product_name))

# Function sell product
def sell_product(product_name,price,amount,todays_date):
    list_sell = list()
    product_amount = amount

    # Check bought csv if product and amount is in stock and exp date valid
    with open("bought.csv", "r") as csv_file:
        csv_bought = csv.reader(csv_file)
        next(csv_file)
        for row_bought in csv_bought:
            buy_date = datetime.strptime(row_bought[2], "%Y-%m-%d").date()
            expiration_date = datetime.strptime(row_bought[4], "%Y-%m-%d").date()
            if row_bought[1] == str.title(product_name).replace("_", " ") and buy_date <= todays_date and expiration_date > todays_date and product_amount != 0:
                combine_amount = 0

                # Increment combine amount when more than one row has the same id
                with open("sold.csv", "r") as csv_file:
                    csv_sold = csv.reader(csv_file)
                    for row_sold in csv_sold:
                        if row_bought[0] == row_sold[1]:
                            combine_amount += int(row_sold[4])

                    # If product has been partially sold, create var amount unsold
                    if int(row_bought[5]) != combine_amount:
                        amount_unsold = int(row_bought[5]) - combine_amount

                        # If amount unsold higher than amount sell, row amount is product amount and product amount hits zero
                        if amount_unsold > product_amount:
                            row_bought[5] = product_amount
                            list_sell.append(row_bought)
                            product_amount = 0
                            
                        # Else, row amount is amount unsold and product amount is lowered with amount unsold
                        else:
                            row_bought[5] = amount_unsold
                            list_sell.append(row_bought)
                            product_amount -= amount_unsold

    # If product amount is lowered to zero, open sold csv
    if product_amount == 0:
        with open("sold.csv", "a", newline="") as csv_file:
            csv_sold = csv.writer(csv_file)
            
            # Create var for last row id and increase id
            with open("sold.csv", "r") as csv_file:
                rows_sold = list(csv.reader(csv_file))
            last_row_sold = rows_sold[-1]
            if last_row_sold[0] == "id":
                last_row_id = 0
            else: 
                last_row_id = last_row_sold[0]
            increment_id = 1

            # Append to sold csv and increment var increase id
            for row in list_sell:
                csv_sold.writerow([int(last_row_id) + increment_id,row[0],todays_date,"%.2f" % price,row[5]])
                increment_id += 1
            print("OK, you have sold "  + str (amount) +" " + str(product_name))

    # Else prints error that product or product amount is not in stock
    else:
        print("Sorry, the product " + str(product_name) + " or requested amount (" +  str (amount) + ") is not in stock.")


# Function inventory today
def inventory_today(todays_date):

    # Table
    table_today = Table(title="Inventory today")
    table_today.add_column("Product Name", justify="right", style="yellow")
    table_today.add_column("Count", style="green")
    table_today.add_column("Buy Price", justify="right", style="blue")
    table_today.add_column("Expiration Date", justify="right", style="red")

    # Add rows to table
    with open("bought.csv", "r") as csv_file:
        csv_bought = csv.reader(csv_file)
        next(csv_file)
        for row_bought in csv_bought:
            buy_date = datetime.strptime(row_bought[2], "%Y-%m-%d").date()
            expired_date = datetime.strptime(row_bought[4], "%Y-%m-%d").date()
            if buy_date <= todays_date and expired_date >= todays_date:
                combine_amount = 0

                # Increase combine amount when more than one row has the same id
                with open("sold.csv", "r") as csv_file:
                    csv_sold = csv.reader(csv_file)
                    for row_sold in csv_sold:
                        if row_bought[0] == row_sold[1]:
                            sell_date = datetime.strptime(row_sold[2], "%Y-%m-%d").date()
                            if sell_date <= todays_date:
                                combine_amount += int(row_sold[4])

                # Lowers the amount that has been sold with combine amount
                if row_bought[5] != str(combine_amount):
                    amount_unsold = int(row_bought[5]) - combine_amount
                    row_bought[5] = str(amount_unsold)
                    table_today.add_row(row_bought[1], row_bought[5], row_bought[3], row_bought[4])

    # Print table
    console = Console()
    console.print(table_today)

# Function inventory yesterday
def inventory_yesterday(yesterdays_date):

    # Table
    table_yesterday = Table(title="Inventory yesterday")
    table_yesterday.add_column("Product Name", justify="right", style="yellow")
    table_yesterday.add_column("Count", style="green")
    table_yesterday.add_column("Buy Price", justify="right", style="blue")
    table_yesterday.add_column("Expiration Date", justify="right", style="red")

    # Add rows to table
    with open("bought.csv", "r") as csv_file:
        csv_bought = csv.reader(csv_file)
        next(csv_file)
        for row_bought in csv_bought:
            buy_date = datetime.strptime(row_bought[2], "%Y-%m-%d").date()
            expired_date = datetime.strptime(row_bought[4], "%Y-%m-%d").date()
            if buy_date <= yesterdays_date and expired_date >= yesterdays_date:
                combine_amount = 0

                # Increase combine amount when more than one row has the same id
                with open("sold.csv", "r") as csv_file:
                    csv_sold = csv.reader(csv_file)
                    for row_sold in csv_sold:
                        if row_bought[0] == row_sold[1]:
                            sell_date = datetime.strptime(row_sold[2], "%Y-%m-%d").date()
                            if sell_date <= yesterdays_date:
                                combine_amount += int(row_sold[4])

                # Lowers the amount that has been sold with combine amount
                if row_bought[5] != str(combine_amount):
                    amount_unsold = int(row_bought[5]) - combine_amount
                    row_bought[5] = str(amount_unsold)
                    table_yesterday.add_row(row_bought[1], row_bought[5], row_bought[3], row_bought[4])

    # Print table
    console = Console()
    console.print(table_yesterday)

# Function inventory date
def inventory_date(date):
    title_date = date.strftime("%d %B, %Y")

    # Table
    table_date = Table(title="Inventory on " + title_date)
    table_date.add_column("Product Name", justify="right", style="yellow")
    table_date.add_column("Count", style="green")
    table_date.add_column("Buy Price", justify="right", style="blue")
    table_date.add_column("Expiration Date", justify="right", style="red")

    # Add rows to table
    with open("bought.csv", "r") as csv_file:
        csv_bought = csv.reader(csv_file)
        next(csv_file)
        for row_bought in csv_bought:
            buy_date = datetime.strptime(row_bought[2], "%Y-%m-%d").date()
            expired_date = datetime.strptime(row_bought[4], "%Y-%m-%d").date()
            if buy_date <= date and expired_date >= date:
                combine_amount = 0

                # Increase combine amount when more than one row has the same id
                with open("sold.csv", "r") as csv_file:
                    csv_sold = csv.reader(csv_file)
                    for row_sold in csv_sold:
                        if row_bought[0] == row_sold[1]:
                            sell_date = datetime.strptime(row_sold[2], "%Y-%m-%d").date()
                            if sell_date <= date:
                                combine_amount += int(row_sold[4])

                # Lowers the amount that has been sold with combine amount
                if row_bought[5] != str(combine_amount):
                    amount_unsold = int(row_bought[5]) - combine_amount
                    row_bought[5] = str(amount_unsold)
                    table_date.add_row(row_bought[1], row_bought[5], row_bought[3], row_bought[4])

    # Print table
    console = Console()
    console.print(table_date)

# Call buy product function
if args.command == "buy":
    buy_product(args.product_name,args.price,args.expiration_date,args.amount,todays_date)

# Call sell product function
if args.command == "sell":
    sell_product(args.product_name,args.price,args.amount,todays_date)

# Call inventory function based on selected date
if args.command == "inventory":
    if args.today:
        inventory_today(todays_date)
    if args.yesterday:
        inventory_yesterday(yesterdays_date)
    if args.date:
        inventory_date(args.date)

# Call revenue function based on selected date
if args.command == "revenue":
    if args.today:
        revenue_today(todays_date)
    if args.yesterday:
        revenue_yesterday(yesterdays_date)
    if args.date:
        revenue_date(args.date)  
    
# Call profit function based on selected date
if args.command == "profit":
    if args.today:
        profit_today(todays_date)
    if args.yesterday:
        profit_yesterday(yesterdays_date)
    if args.date:
        profit_date(args.date)
       
if __name__ == "__main__":
    main()
