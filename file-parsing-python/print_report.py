#!/usr/bin/env python
"""
Parse transactional data of different banks
and find source accounts with maximum average transaction
"""
import sys
from src.integrations.sweet_bank import work
from src.integrations.acme_financials import process
from src.integrations.gringotts_bank import find_accounts_with_max_average_transaction


def gringotts_post_process(data):
    """
    Function to process result of Gringotts Bank maximum average transaction
    :param data:
    :return:
    """
    accounts = data[1]
    avg_max_trans = data[2]
    print("\n{}".format(data[0]))
    for account in accounts:
        print("Account: {}, Average Max Transaction: {} ".format(account, avg_max_trans))


if __name__ == '__main__':
    BANK_NAME = sys.argv[1]
    if BANK_NAME == "sweet_bank":
        for f in ["../../assets/sweet_bank_financials_1.csv",
                  "../../assets/sweet_bank_financials_2.csv",
                  "../../assets/sweet_bank_financials_3.csv"]:
            file_name = f.split('/')[-1]
            print(file_name)
            work(file_name)
            print()
            print()

    if BANK_NAME == "acme_bank":
        for f in ["../../assets/acme_bank_financials_1.json"]:
            file_name = f.split('/')[-1]
            result = process(file_name)
            print(file_name)
            print(result)

    if BANK_NAME == "gringotts_bank":
        import multiprocessing
        # Create a pool of processes, number process is equal to the cpu of the machine
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            for file_path in ["/assets/gringotts_5b36864e-8089-40f7-8d3d-25c14715656d.txt"]:
                pool.apply_async(find_accounts_with_max_average_transaction,
                                 args=(file_path, ),
                                 callback=gringotts_post_process)

            pool.close()
            pool.join()
