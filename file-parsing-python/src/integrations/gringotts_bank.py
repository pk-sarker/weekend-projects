"""
This file parse Gringotts Bank transaction log
and find source accounts with maximum average
transaction.
"""
import os
from collections import defaultdict


def find_accounts_with_max_average_transaction(relative_file_path=None):
    """
    Function to parse given file based on Gringotts Banks' documentation
    :param relative_file_path: relative path of the file from root directory of the project
    :return: Returns a list of source accounts with maximum average transactions
    """

    def parse_account(account):
        """
        Function to parse account number.
        Account number format:
        - first 9 numbers are bank id
        - next 2 letters are account holder
        - and next 9  numbers are account id
        :param account:
        :return: returns bank id, account holder, account id
        """
        if not account:
            raise Exception("Account number is null or empty")

        bank_id = account[0:9]
        ac_holder = account[9:11]
        ac_id = account[11:len(account)]

        return bank_id, ac_holder, ac_id

    def parse_transaction_amount(trans_amount):
        """
        Function to parse transaction amount
        :param trans_amount:
        :return: amount and currency
        """
        amount = None
        currency = None
        if trans_amount is not None:
            currency = trans_amount[0:3]
            amount = trans_amount[3:len(trans_amount)]
        return amount, currency

    def parse_transaction_file(file_path):
        """
        Function to parse transactions listed in a given file.
        Transaction are in batch. Start of transaction batch is identified by a line where
        first 4 letters represent bank identification - GTTB for Gringotts Bank

        In the file each transaction is represented in 4 lines,
        - 1st line: Transaction ID
        - 2nd line: Source account
        - 3rd line: Destination Account
        - 4th line: Transfer Amount
        :param file_path:
        :return: Dictionary of transactions by source account id as key
        """

        source_account_transactions = defaultdict()
        transaction = defaultdict(lambda: None)

        # Read file line by line
        with open(os.getcwd() + file_path, encoding='utf-8-sig') as file_stream:

            # trans_line_count maintains
            # line number of a transaction block
            trans_line_count = -1

            for line in file_stream:
                line = line.rstrip()
                if line[0:4] == 'GTTB':
                    trans_line_count = 0
                    transaction = defaultdict(lambda: None)
                    continue

                # New transaction block
                if trans_line_count >= 4:
                    transaction = defaultdict(lambda: None)
                    trans_line_count = 0

                # Skip Transaction ID
                if trans_line_count == 0:
                    # Line 1 of a transaction block is transaction id
                    transaction["transaction_id"] = line
                    trans_line_count += 1
                    continue

                if trans_line_count < 4:
                    if trans_line_count == 1:
                        # Line 2 of a transaction block is source account number
                        bank_id, ac_holder, ac_id = parse_account(line)
                        transaction["s_bank_id"] = bank_id
                        transaction["s_ac_holder"] = ac_holder
                        transaction["s_ac_id"] = ac_id
                    if trans_line_count == 2:
                        # Line 3 of a transaction block is destination account number
                        bank_id, ac_holder, ac_id = parse_account(line)
                        transaction["d_bank_id"] = bank_id
                        transaction["d_ac_holder"] = ac_holder
                        transaction["d_ac_id"] = ac_id
                    if trans_line_count == 3:
                        # Line 4 of a transaction block is transaction amount
                        amount, currency = parse_transaction_amount(line)
                        if amount is not None:
                            amount = int(amount)
                        transaction["amount"] = amount
                        transaction["currency"] = currency

                    trans_line_count += 1

                # Compute Average
                if trans_line_count >= 4:
                    source_account = transaction.get("s_ac_id")
                    if not source_account_transactions.__contains__(source_account):
                        source_account_transactions[source_account] = defaultdict()
                        source_account_transactions[source_account]["transactions"] = []
                        source_account_transactions[source_account]["sum_of_trans"] = 0
                        source_account_transactions[source_account]["trans_count"] = 0
                        source_account_transactions[source_account]["avg_trans"] = 0

                    source_account_transactions[source_account]["transactions"].append(transaction)
                    source_account_transactions[source_account]["trans_count"] += 1
                    source_account_transactions[source_account]["sum_of_trans"] += transaction["amount"]
                    source_account_transactions[source_account]["avg_trans"] = \
                        source_account_transactions[source_account]["sum_of_trans"] / \
                        source_account_transactions[source_account]["trans_count"]
        return source_account_transactions

    def find_account_with_max_avg_trans(transactions, file_path):
        """
        This function finds source accounts with max average transactions
        from a set of accounts and their transactions

        :param transactions: Dictionary, source account as key
        :param file_path:
        :return: Tuple of input file name, source accounts, max transaction
        """
        source_ac_max_avg_tran = []
        max_avg_transaction = -1
        for source_ac in transactions.keys():
            source_ac_trans = transactions.get(source_ac)
            if source_ac_trans.get("avg_trans") > max_avg_transaction:
                max_avg_transaction = source_ac_trans.get("avg_trans")
                source_ac_max_avg_tran = [source_ac]
            elif source_ac_trans.get("avg_trans") == max_avg_transaction:
                source_ac_max_avg_tran.append(source_ac)

        return file_path.split('/')[2], source_ac_max_avg_tran, max_avg_transaction

    transactions_by_account = parse_transaction_file(relative_file_path)
    return find_account_with_max_avg_trans(transactions_by_account, relative_file_path)
