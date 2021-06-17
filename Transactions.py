import os

import numpy as np
import pandas as pd


class Transactions:

    def __init__(self, path='.'):
        self.file_path = os.path.join(path, "crypto_transactions.csv")
        if not os.path.exists(self.file_path):
            self.create_transactions_file()
        self.data = pd.read_csv(self.file_path, header=0, index_col=0)
        self.agg_data = None

    def create_transactions_file(self):
        df = pd.DataFrame(columns=['coin', 'price', 'amount', 'paid_with', 'amount_paid'])
        self.data = df
        self.save()

    def add_transaction(self):
        print("What cryptocurrency have you bought?: ")
        coin = str(input())
        print("What was the price of that coin (without currency)?: ")
        price = float(input())
        print("What cryptocurrency did you pay with?: ")
        currency = str(input())
        print("How much cryptocurrency have you bought?: ")
        crypto_amount = float(input())
        record = pd.Series({
            "coin": coin,
            "price": price,
            "amount": crypto_amount,
            "paid_with": currency,
            "amount_paid": price * crypto_amount,
        })
        self.data = self.data.append(record, ignore_index=True)
        self.save()

    def remove_all_transactions(self):
        print("Are you sure you want to remove all transactions data? [Y/n]: ")
        answer = str(input())
        if answer == 'Y':
            print("Are you really, really sure you want to remove all transactions data? [Y/n]: ")
            second_answer = str(input())
            if second_answer == 'Y':
                os.remove(self.file_path)
                self.data = None
                print("Removed all transaction data!")
            elif second_answer == 'n':
                print("Ufff...")
            else:
                raise Exception("Wrong answer, only [Y/n]!")
        elif answer == 'n':
            print("Ufff...")
        else:
            raise Exception("Wrong answer, only [Y/n]!")

    def aggregate_holdings(self):
        agg_df = self.data.groupby(["coin", "paid_with"]).agg({"price": 'mean', "amount": 'sum'})
        agg_df.columns = ["mean_price", "total_amount"]
        agg_df["holding_value"] = agg_df["mean_price"] * agg_df["total_amount"]
        self.agg_data = agg_df
        return self.agg_data

    def calculate_investments(self):
        current_prices = {}
        for coin in self.agg_data.index:
            print(f"What is the current price for {coin}?: ")
            current_prices[coin] = float(input())
        self.agg_data["current_price"] = current_prices.values()
        self.agg_data["current_value"] = self.agg_data["total_amount"] * self.agg_data["current_price"]
        self.agg_data["value_gain"] = self.agg_data["current_value"] - self.agg_data["holding_value"]
        self.agg_data["gain_percentage"] = (self.agg_data["value_gain"] / self.agg_data["holding_value"]) * 100.
        return self.agg_data

    def save(self):
        self.data.to_csv(self.file_path)
