import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")

def get_sales_data():
    """
    Get sales data from the user
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by comma")
        print("Example: 10,20,30,40,50,60 \n")

        data_str = input("Enter your data here: ")
        
        sales_data = data_str.split(",")
        validate_data(sales_data)

        if validate_data(sales_data):
            print("Data is valid!")
            break
    
    return sales_data       

def validate_data(values):
    """
    validates data by trying the code provided, if exception
    from correct format, an error will be raised in the terminal
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly six (6) values required,  you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again \n")
        return False

    return True

def update_sales_worksheet(data):
    """
    update sales worksheet, add new row to sales worksheet 
    using list data provided
    """
    print("updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("sales data updated successfully! \n")

def calculate_surplus_data(sales_row):
    """
    calculate surplus data based on stock - sales data.
    """
    print("calculating surplus data... \n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock.pop()
    print(stock_row)
    print([int(num) for num in stock_row])

def main():
    """
    run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(data)

print("Welcome to love sandwiches Data Automation")
main()    