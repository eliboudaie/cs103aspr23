from transaction import Transaction
import datetime

def main():
    db_name = 'tracker.db'
    transaction = Transaction(db_name)
    print("Welcome to the Financial Tracker Program!")
    print_menu()

    while True:
        choice = input("Please enter your choice (enter 11 to print the menu): ")
        if choice == '0':
            print("Goodbye!")
            break
        elif choice == '1':
            show_categories(transaction)
        elif choice == '2':
            add_category(transaction)
        elif choice == '3':
            modify_category(transaction)
        elif choice == '4':
            show_transactions(transaction)
        elif choice == '5':
            add_transaction(transaction)
        elif choice == '6':
            delete_transaction(transaction)
        elif choice == '7':
            summarize_by_date(transaction)
        elif choice == '8':
            summarize_by_month(transaction)
        elif choice == '9':
            summarize_by_year(transaction)
        elif choice == '10':
            summarize_by_category(transaction)
        elif choice == '11':
            print_menu()
        else:
            print("Invalid choice. Please try again.")

def print_menu():
    print("0. quit")
    print("1. show categories")
    print("2. add category")
    print("3. modify category")
    print("4. show transactions")
    print("5. add transaction")
    print("6. delete transaction")
    print("7. summarize transactions by date")
    print("8. summarize transactions by month")
    print("9. summarize transactions by year")
    print("10. summarize transactions by category")
    print("11. print this menu")

def show_categories(transaction):
    categories = transaction.get_categories()
    print("Categories:")
    for row in categories:
        print(row[0])

def add_category(transaction):
    category = input("Enter new category: ")
    transaction.add_category(category)
    print("Category added successfully.")

def modify_category(transaction):
    old_category = input("Enter category to modify: ")
    new_category = input("Enter new category name: ")
    transaction.modify_category(old_category, new_category)
    print("Category modified successfully.")

def show_transactions(transaction):
    transactions = transaction.get_transactions()
    if not transactions:
        print("no transaction recorded")
    else:
        for row in transactions:
            print(row)

def add_transaction(transaction):
    item_num = int(input("Enter item number: "))
    amount = float(input("Enter amount: "))
    category = input("Enter category: ")
    date = input("Enter date (YYYY-MM-DD): ")
    description = input("Enter description: ")
    transaction.add_transaction(item_num, amount, category, date, description)
    print("Transaction added successfully.")

def delete_transaction(transaction):
    id = int(input("Enter transaction ID: "))
    transaction.delete_transaction(id)
    print("Transaction deleted successfully.")

def summarize_by_date(transaction):
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    results = transaction.summarize_by_date(start_date, end_date)
    print("Transactions by date:")
    for row in results:
        print(row)

def summarize_by_month(transaction):
    year = input("Enter year (YYYY): ")
    results = transaction.summarize_by_month(year)
    print("Transactions by month:")
    for row in results:
        print(row)


def summarize_by_year(transaction):
    results = transaction.summarize_by_year()
    print("Transactions by year:")
    for row in results:
        print(row)

def summarize_by_category(transaction):
    category = input("Enter category: ")
    results = transaction.summarize_by_category(category)
    print(f"Transactions by category ({category}):")
    for row in results:
        print(row)

if __name__ == '__main__':
    main()

