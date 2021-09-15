from ..config.config import Config
from time import time
import json
from decimal import Decimal


class Dynamo(Config):
    """
    This class is used to store information in a DynamoDB Table.
    """

    def __init__(self) -> None:
        Config.__init__(self)
        self.dynamoresource = self.get_boto_resource('dynamodb')
        self.table = self.dynamoresource.Table(self.TABLE)

    def format_summary(self, summary):
        """Transforms decimal values into flt values that Dynamodb can read."""
        return json.loads(json.dumps(summary), parse_float=Decimal)

    def store_summary(self, summary: dict) -> None:
        """
        Writes a record to a Table. The unique ID is a timestamp, and summary is a dictionary
        with all the information of the transactions.
        """
        self.table.put_item(
            Item={
                'Id': str(time()),
                'Summary': self.format_summary(summary)
            }
        )
