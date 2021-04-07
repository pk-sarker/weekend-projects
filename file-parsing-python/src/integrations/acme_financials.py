import json
import pathlib
from collections import defaultdict

def process(fileNm = None):
    def populate_transactions(fileNm = None):
        current = str(pathlib.Path().parent.parent.absolute())
        full_fn = current + '/assets/' + fileNm
        trans_sum = defaultdict(int)
        trans_num = defaultdict(int)
        with open(full_fn, encoding='utf-8-sig') as file:
            batches = json.loads(file.read())["batches"]
            for batch in batches:
                transactions = batch["transactions"]
                for transaction in transactions:
                    source_account = transaction["source_account"]
                    trans_sum[source_account] += transaction["amount_in_cents"]
                    trans_num[source_account] += 1
        return trans_sum, trans_num

    def find_account_with_max_avg_trans(trans_sum, trans_num):
        max_avg_trans_size = None
        max_source_account = None
        for source_account in trans_sum:
            avg_trans_size = trans_sum[source_account] / trans_num[source_account]
            if max_avg_trans_size is None or avg_trans_size > max_avg_trans_size:
                max_avg_trans_size = avg_trans_size
                max_source_account = source_account
        return max_source_account

    trans_sum, trans_num = populate_transactions(fileNm)
    return find_account_with_max_avg_trans(trans_sum, trans_num)
