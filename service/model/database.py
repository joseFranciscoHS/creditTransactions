from ..config.config import Config
from time import time
import json
from decimal import Decimal


class Dynamo(Config):

    def __init__(self) -> None:
        Config.__init__(self)
        self.dynamoresource = self.get_boto_resource('dynamodb')
        self.table = self.dynamoresource.Table(self.TABLE)

    def format_summary(self, summary):
        return json.loads(json.dumps(summary), parse_float=Decimal)

    def store_summary(self, summary: dict) -> None:
        self.table.put_item(
            Item={
                'Id': str(time()),
                'Summary': self.format_summary(summary)
            }
        )
