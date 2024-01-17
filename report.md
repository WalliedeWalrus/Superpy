# winc-superpy

The application stores the purchases and sales of the shop.  
It can report the store's inventory, revenue and profit at different moments in time.
For test purposes the application can be warped in time.

The application consists of 3 files: main.py, profit.py and revenue.py.

# Main.py

This is the main part of the application that needs to be called to run the program.
The argparse module is used to handle different commands and arguments.
It parses the commands with arguments and calls the relevant functions with the data provided by the user.
The parser takes either the -advance-time argument or one of the commands: buy, sell or report.
The report command has it's own sub-parser running the following commands: inventory, revenue or profit.

If any arguments or commands are invalid it displays an message tot the user.

# Profit.py and revenue.py

These parts hold the profit and revenue function of the application. They get called from Main.py.

## CSV and TXT files

The application uses 3 different files in the working directory: bought.csv, sold.csv and date.txt.

## bought.csv

records the bought stock as follows:
id,product_name,buy_date,buy_price,expiration_date,amount

## sold.csv

records the sold stock as follows:
id,bought_id,sell_date,sell_price,amount

## date.txt

records the current date as YYYY-MM-DD. This file gets updated whenever the user advances time (--advance-time) or sets a specific date. This file is called constantly throughout the program to check which entries in bought.csv and sold.csv are relevant.

### Technical challenge 1

I wanted to sell an amount of a product with a number. The difficult part was that I wanted to be able to sell everything in one command also when two or more identical product rows in bought.csv had been bought.
My solution was to make a list of the row that had been completely sold, and iterate the next viable row until the amount selling had been depleted.

For example:

```
# If amount unsold higher than amount selling, row amount is product amount and product amount hits zero

 if amount_unsold > product_amount:
    row_bought[5] = product_amount
    list_sell.append(row_bought)
    product_amount = 0

    # Else, row amount is amount unsold and product amount is lowered with amount unsold

       else:
       row_bought[5] = amount_unsold
       list_sell.append(row_bought)
       product_amount -= amount_unsold
```

With the list I was able to add everything once the selling amount hit 0, and add nothing at all when the selling amount never hit 0.

### Technical challenge 2

I wanted the items 'revenue' and 'profit' to use also the additional date formats 'YYYY-MM' and 'YYYY' working on the '--date' argument.
I used the 'try' and 'except' method inside of the 'validate_date' function when parsing the date argument. I managed to do this by turning the datetime format to a string so that in the called function it would only receive the year and month or year to work with.

For example:

```
# Validates date and returns the choosen data format as a string
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
                message = "not a valid date: {0!r}\n".format(date) + "Valid data formats are 'YYYY-MM-DD', 'YYYY-MM' and 'YYYY'."
                raise argparse.ArgumentTypeError(message)
```

The called function has the same 'try' and 'except' method as 'validate_date' and will function accordingly to the chosen data format.

### challenge 3

I used the rich module to print good looking tables when displaying the inventory.

## Finally

I learned a lot of this assignment but it took a lot of time. I had a hard time figuring everything out while doing my normal daytime job and then returning to the assignment again. Looking back I wasted lots of time but in the end I learned and I like the result.
