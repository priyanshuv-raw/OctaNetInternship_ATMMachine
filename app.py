import os


ACCOUNTS_FILE = 'accounts.txt'


class ATM:
    def __init__(self):
        self.accounts = self.load_accounts()

    def load_accounts(self):
        accounts = {}
        if os.path.exists(ACCOUNTS_FILE):
            with open(ACCOUNTS_FILE, 'r') as file:
                for line in file:
                    account_num, pin, balance = line.strip().split(',')
                    accounts[account_num] = {'pin': pin, 'balance': float(balance)}
        return accounts

    def save_accounts(self):
        with open(ACCOUNTS_FILE, 'w') as file:
            for account_num, account_info in self.accounts.items():
                pin = account_info['pin']
                balance = account_info['balance']
                file.write(f"{account_num},{pin},{balance}\n")

    def authenticate(self, account_num, pin):
        if account_num in self.accounts and self.accounts[account_num]['pin'] == pin:
            return True
        else:
            return False

    def deposit(self, account_num, amount):
        self.accounts[account_num]['balance'] += amount
        self.save_accounts()

    def withdraw(self, account_num, amount):
        if self.accounts[account_num]['balance'] >= amount:
            self.accounts[account_num]['balance'] -= amount
            self.save_accounts()
            return True
        else:
            print("Insufficient funds.")
            return False

    def transfer(self, from_account_num, to_account_num, amount):
        if self.withdraw(from_account_num, amount):
            self.deposit(to_account_num, amount)
            print("Transfer successful.")
        else:
            print("Transfer failed due to insufficient funds.")

def write_to_file(file_path, data):
    try:
        with open(file_path, 'a') as file:
            file.write(data)
    except Exception as e:
        print('An error occurred:', str(e))

def print_file(file_path):
    try:
        with open(file_path, 'r') as file:
            file_contents = file.read()
            print(file_contents)
    except FileNotFoundError:
        print('File not found.')
    except Exception as e:
        print('An error occurred:', str(e))

def main():
    atm = ATM()

    while True:
        print("Welcome to the ATM Console")
        
        account_num = input("Enter your account number: ")
        pin = input("Enter your PIN: ")

        path = "Accounts/"+account_num+".txt"
        file_path = path

        if atm.authenticate(account_num, pin):
            while True:
                print("\nATM Menu:")
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Transfer")
                print("4. Check Balance")
                print("5. History")
                print("6. Exit")

                choice = input("Enter your choice: ")

                if choice == '1':
                    amount = float(input("Enter the amount to deposit: "))
                    atm.deposit(account_num, amount)
                    file_path = path 
                    data_to_write = f"Deposited               ${amount}                                  ${atm.accounts[account_num]['balance']:.2f}\n"
                    write_to_file(file_path, data_to_write)
                elif choice == '2':
                    amount = float(input("Enter the amount to withdraw: "))
                    atm.withdraw(account_num, amount)
                    file_path = path 
                    data_to_write = f"Withdraw                                    ${amount}              ${atm.accounts[account_num]['balance']:.2f}\n"
                    write_to_file(file_path, data_to_write)
                elif choice == '3':
                    to_account_num = input("Enter the recipient account number: ")
                    amount = float(input("Enter the amount to transfer: "))
                    atm.transfer(account_num, to_account_num, amount)
                    print(f"Your account balance: ${atm.accounts[account_num]['balance']:.2f}")
                    file_path = path 
                    data_to_write = f"Transfer to A/C{to_account_num}                         ${amount}              ${atm.accounts[account_num]['balance']:.2f}\n"
                    write_to_file(file_path, data_to_write)

                    newpath =  "Accounts/"+to_account_num+".txt"
                    data = f"Recieved From A/C{account_num}      ${amount}                                 ${atm.accounts[to_account_num]['balance']:.2f}\n"
                    write_to_file(newpath,data)
                elif choice == '4':
                    print(f"Your account balance: ${atm.accounts[account_num]['balance']:.2f}")
                elif choice == '5':
                    print_file(file_path)
                elif choice == '6':
                    atm.save_accounts()
                    print("Thank you for using the ATM. Goodbye!")
                    return
                else:
                    print("Invalid choice. Please try again.")

        else:
            print("Invalid account number or PIN. Please try again.")


if __name__ == "__main__":
    main()



   
