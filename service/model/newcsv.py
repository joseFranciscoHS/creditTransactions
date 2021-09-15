from .decorators import debug
from ..config.config import Config
from io import StringIO
import pandas as pd
import csv


class NewCSV(Config):
    """
    This class reads from s3 a list of transactions, and stores in /tmp a summary
    of the transactions.
    """

    def __init__(self) -> None:
        Config.__init__(self)
        self.s3client = self.get_boto_client('s3')

    def read_object(self, obj: 'client.get_object') -> str:
        """Converts object body to str."""
        body = obj['Body']
        body = body.read().decode('utf-8')
        return StringIO(body)

    @debug
    def read_from_s3(self, key: str, **kwargs) -> pd.DataFrame:
        """Reads a csv file from s3."""
        info = self.s3client.get_object(Bucket=self.BUCKET, Key=key)
        info = self.read_object(info)
        return pd.read_csv(info, **kwargs)

    @debug
    def save_summary(self, summary: dict):
        """Writes a csv file to /tmp directory."""
        with open('/tmp/summary.csv', 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(['Month', 'Average Debit',
                             'Average Credit', 'Total Balance'])
            writer.writerow(['Overall', summary['generalsummary']['AvgD'],
                             summary['generalsummary']['AvgC'], summary['generalsummary']['TotalBalance']])
            writer.writerow(['Month', 'Average Debit',
                             'Average Credit', 'Transactions Count'])
            writer.writerows([
                [k, *v.values()] for k, v in summary['monthlysummary'].items()
            ])
