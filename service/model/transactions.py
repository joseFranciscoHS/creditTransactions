from .newcsv import NewCSV
import pandas as pd
from .decorators import debug


class Transaction(NewCSV):

    def __init__(self) -> None:
        NewCSV.__init__(self)

    def read_transactions(self, filename: str) -> pd.DataFrame:
        return self.read_from_s3(filename, dtype={'Id': int, 'Date': str, 'Transaction': str})
    
    @debug
    def create_summary(self, df: pd.DataFrame) -> dict:

        def get_month(df):
            return df.Date.apply(lambda x: int(x.split('/')[0]))

        def get_transaction_type(df):
            return df.Transaction.apply(lambda x: 'D' if x[0] == '-' else 'C')

        def clean_transaction(df):
            return df.Transaction.apply(lambda x: float(x) if x[0] == '-' else float(x[1:]))

        df['Month'] = get_month(df)
        df['TransactionType'] = get_transaction_type(df)
        df['CleanTransaction'] = clean_transaction(df)

        monthlysummary = df.groupby(['Month']).apply(lambda x: {
            'CountTransaction': len(x.Id),
            'AvgD': x.loc[x.TransactionType == 'D']['CleanTransaction'].mean(),
            'AvgC': x.loc[x.TransactionType == 'C']['CleanTransaction'].mean()
        }).to_dict()
        generalsummary = {
            'TotalBalance': df.CleanTransaction.sum(),
            'AvgD': df.loc[df.TransactionType == 'D']['CleanTransaction'].mean(),
            'AvgC': df.loc[df.TransactionType == 'C']['CleanTransaction'].mean()
        }
        return {
            'monthlysummary': monthlysummary,
            'generalsummary': generalsummary
        }
