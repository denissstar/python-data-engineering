"""
This program reads a "sales.csv" file, converts the epoch timestamps to a readable format, 
and calculates the total sales for each product. The program then writes the first sale datetime, 
last sale datetime, product name, total quantity sold, and total sales amount to a new PSV file named "sales_report.psv".
"""

import csv
from decimal import Decimal
from datetime import datetime
from os import path


def get_sales_summary(filename):
    # Read the sales.csv file
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        sales = {}

        # Iterate over each row in the sales.csv file
        for row in reader:
            timestamp = convert_timestamp(row["Timestamp"])
            product = row["Product Name"]
            quantity = int(row["Quantity"])
            price = Decimal(row["Price"])

            if product in sales:
                if timestamp < sales[product]["first_sale"]:
                    sales[product]["first_sale"] = timestamp
                if timestamp > sales[product]["last_sale"]:
                    sales[product]["last_sale"] = timestamp
                sales[product]["quantity"] += quantity
                sales[product]["total_amount"] += quantity * price
            else:
                sales[product] = {
                "first_sale": timestamp,
                "last_sale": timestamp,
                "quantity": quantity,
                "total_amount": quantity * price,
            }         
    return sales


def write_report(sales_data):
    # Write the sales report to a new PSV file
    with open(path.join("data", "sales_report.psv"), "w") as file:
        fieldnames = [
            "Product Name",
            "First Sale",
            "Last Sale",
            "Total Quantity Sold",
            "Total Sales Amount"
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter="|")
        writer.writeheader()

        sorted_products = sorted(sales_data.keys())
        for product in sorted_products:
            data = sales_data[product]
            writer.writerow({
                "Product Name": product,
                "First Sale": data["first_sale"],
                "Last Sale": data["last_sale"],
                "Total Quantity Sold": data["quantity"],
                "Total Sales Amount": data["total_amount"]
            })


def convert_timestamp(timestamp):
    return datetime.fromtimestamp(int(timestamp)).strftime("%Y-%m-%d %H:%M:%S")


sales_data = get_sales_summary(path.join("data", "sales.csv"))
write_report(sales_data)

# Print report file to the console
with open(path.join("data", "sales_report.psv"), "r") as file:
    for line in file:
        print(line.strip())