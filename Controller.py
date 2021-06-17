from tabulate import tabulate


class Controller:

    @staticmethod
    def do_1(transactions):
        """Print added transactions"""
        print(tabulate(transactions.data, headers='keys', tablefmt='psql'))

    @staticmethod
    def do_2(transactions):
        """Add transaction"""
        transactions.add_transaction()

    @staticmethod
    def do_3(transactions):
        """Remove transaction"""
        print('Removing transaction')

    @staticmethod
    def do_4(transactions):
        """Aggregate holdings"""
        print('Aggregating holdings')
        agg = transactions.aggregate_holdings()
        print(tabulate(agg, headers='keys', tablefmt='psql'))

    @staticmethod
    def do_5(transactions):
        """Remove all transactions data"""
        print('Removing all transactions data')
        transactions.remove_all_transactions()

    @staticmethod
    def do_6(transactions):
        """Calculate investments"""
        print('Calculating investments')
        inv = transactions.calculate_investments()
        print(tabulate(inv, headers='keys', tablefmt='psql'))

    @staticmethod
    def do_7(transactions):
        """Exit program"""
        if transactions.data is not None:
            transactions.save()
        print('Exiting...')

    @staticmethod
    def execute(user_input, transactions):
        controller_name = f"do_{user_input}"
        try:
            controller = getattr(Controller, controller_name)
        except AttributeError:
            print("Method not found")
        else:
            controller(transactions)

    @staticmethod
    def run(transactions):
        user_input = 0
        while user_input != 7:
            Controller.generate_menu()
            user_input = int(input())
            Controller.execute(user_input, transactions)
        print("Program stopped.")

    @staticmethod
    def generate_menu():
        print("==========================================")
        print("                  MENU                    ")
        print("==========================================")
        do_methods = [m for m in dir(Controller) if m.startswith("do_")]
        menu_string = "\n".join([f"{method[-1]}. {getattr(Controller, method).__doc__}"
                                 for method in do_methods])
        print(menu_string)
        print("==========================================")
        print("Insert a number: ")
