from Controller import Controller
from Transactions import Transactions


def main():
    transactions = Transactions()
    Controller.run(transactions)


if __name__ == '__main__':
    main()
