users_db = {}
transactions_log = []
txn_counter = 1000


def generate_transaction_id():
    global txn_counter
    txn_counter = txn_counter + 1
    return "TXN" + str(txn_counter)


def find_account(customer_id):
    if customer_id in users_db:
        return users_db[customer_id]
    else:
        return None


def create_account():
    print("\n--- Create New Account ---")

    customer_id = input("Enter Customer ID: ")

    if customer_id == "":
        print("Customer ID cannot be empty!")
        return

    if customer_id in users_db:
        print("Customer ID already exists!")
        return

    name = input("Enter Holder Name: ")

    if name == "":
        print("Holder name cannot be empty!")
        return

    pin = input("Set 4-Digit PIN: ")

    if len(pin) != 4 or not pin.isdigit():
        print("PIN must be exactly 4 digits!")
        return

    print("Select Account Type:")
    print("1. Savings Account")
    print("2. Current Account")

    type_choice = input("Choice (1 or 2): ")

    if type_choice == "1":
        acc_type = "Savings"
    elif type_choice == "2":
        acc_type = "Current"
    else:
        print("Invalid account type!")
        return

    initial_deposit = input("Enter Initial Deposit: ")

    if not initial_deposit.isdigit():
        print("Please enter numbers only!")
        return

    initial_deposit = float(initial_deposit)

    if acc_type == "Savings" and initial_deposit < 500:
        print("Savings account requires at least $500!")
        return

    new_account = {
        "name": name,
        "pin": pin,
        "type": acc_type,
        "balance": initial_deposit,
        "history": []
    }

    users_db[customer_id] = new_account

    txn_id = generate_transaction_id()

    record = "[" + txn_id + "] Initial Deposit: +$" + str(initial_deposit)

    users_db[customer_id]["history"].append(record)
    transactions_log.append(record)

    print("Account created successfully!")


def deposit_money(account):
    amount = input("Enter Deposit Amount: ")

    if not amount.isdigit():
        print("Please enter numbers only!")
        return

    amount = float(amount)

    if amount > 0:
        account["balance"] = account["balance"] + amount

        txn_id = generate_transaction_id()

        record = "[" + txn_id + "] Deposit: +$" + str(amount)

        account["history"].append(record)
        transactions_log.append(record)

        print("Deposit successful! New balance: $" + str(account["balance"]))
    else:
        print("Amount must be greater than zero!")


def withdraw_money(account):
    amount = input("Enter Withdrawal Amount: ")

    if not amount.isdigit():
        print("Please enter numbers only!")
        return

    amount = float(amount)

    if account["type"] == "Savings":
        min_balance = 500
    else:
        min_balance = 0

    if amount <= 0:
        print("Amount must be greater than zero!")

    elif account["balance"] - amount < min_balance:
        print("Cannot withdraw! Minimum balance rule violated.")

    else:
        account["balance"] = account["balance"] - amount

        txn_id = generate_transaction_id()

        record = "[" + txn_id + "] Withdrawal: -$" + str(amount)

        account["history"].append(record)
        transactions_log.append(record)

        print("Withdrawal successful! New balance: $" + str(account["balance"]))


def transfer_money(sender_account, sender_customer_id):
    receiver_customer_id = input("Enter Destination Customer ID: ")

    if receiver_customer_id == sender_customer_id:
        print("Cannot transfer to your own account!")
        return

    receiver_account = find_account(receiver_customer_id)

    if receiver_account == None:
        print("Destination customer ID not found!")
        return

    amount = input("Enter Transfer Amount: ")

    if not amount.isdigit():
        print("Please enter numbers only!")
        return

    amount = float(amount)

    if sender_account["type"] == "Savings":
        min_balance = 500
    else:
        min_balance = 0

    if amount <= 0:
        print("Amount must be greater than zero!")

    elif sender_account["balance"] - amount < min_balance:
        print("Transfer failed! Insufficient balance.")

    else:
        sender_account["balance"] = sender_account["balance"] - amount
        receiver_account["balance"] = receiver_account["balance"] + amount

        txn_id = generate_transaction_id()

        s_record = (
            "[" + txn_id + "] Transfer to "
            + receiver_account["name"]
            + ": -$"
            + str(amount)
        )

        r_record = (
            "[" + txn_id + "] Received from "
            + sender_account["name"]
            + ": +$"
            + str(amount)
        )

        sender_account["history"].append(s_record)
        receiver_account["history"].append(r_record)

        transactions_log.append(
            "[" + txn_id + "] Transfer: "
            + sender_customer_id
            + " to "
            + receiver_customer_id
        )

        print("Transfer successful!")


def calculate_interest(account):
    if account["type"] == "Savings":
        interest = account["balance"] * (0.05 / 12)

        print("Estimated Monthly Interest: $" + str(interest))
    else:
        print("Interest calculation is only for Savings accounts.")


def account_statement(account):
    print("\n--- Account Statement for " + account["name"] + " ---")

    print("Current Balance: $" + str(account["balance"]))

    print("Transaction History:")

    if len(account["history"]) == 0:
        print("No transactions yet.")
    else:
        for item in account["history"]:
            print("- " + item)


def bank_dashboard():
    total_accounts = len(users_db)
    total_transactions = len(transactions_log)

    total_money = 0

    for customer_id in users_db:
        total_money = total_money + users_db[customer_id]["balance"]

    print("\n=== Bank Dashboard ===")
    print("Total Accounts: " + str(total_accounts))
    print("Total Money Held: $" + str(total_money))
    print("Total Transactions: " + str(total_transactions))


def user_menu(account, customer_id):
    while True:
        print("\n=== User Menu: " + account["name"] + " ===")

        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transfer Money")
        print("5. Calculate Interest")
        print("6. Account Statement")
        print("7. Logout")

        choice = input("Select option (1-7): ")

        if choice == "1":
            print("Current Balance: $" + str(account["balance"]))

        elif choice == "2":
            deposit_money(account)

        elif choice == "3":
            withdraw_money(account)

        elif choice == "4":
            transfer_money(account, customer_id)

        elif choice == "5":
            calculate_interest(account)

        elif choice == "6":
            account_statement(account)

        elif choice == "7":
            print("Logged out.")
            break

        else:
            print("Invalid choice!")


def main():
    while True:
        print("\n=== Banking Management System ===")

        print("1. Create New Account")
        print("2. Login")
        print("3. Bank Dashboard")
        print("4. Exit")

        choice = input("Select option (1-4): ")

        if choice == "1":
            create_account()

        elif choice == "2":
            customer_id = input("Enter Customer ID: ")
            pin = input("Enter PIN: ")

            account = find_account(customer_id)

            if account != None and account["pin"] == pin:
                print(
                    "Login successful! Welcome "
                    + account["name"]
                )

                user_menu(account, customer_id)

            else:
                print("Invalid Customer ID or PIN!")

        elif choice == "3":
            bank_dashboard()

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()