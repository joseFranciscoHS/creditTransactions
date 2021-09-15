from service.model.decorators import LOGGER
from ..model.transactions import Transaction
from ..config.config import Config
from ..model.database import Dynamo
from ..model.decorators import debug
import json


@debug
def delete_sqs(receipt: str):
    cfg = Config()
    sqs = cfg.get_boto_client('sqs')
    sqs.delete_message(QueueUrl=cfg.QUEUE, ReceiptHandle=receipt)


@debug
def new_summary(key: str):
    trns = Transaction()
    df = trns.read_transactions(key)
    summary = trns.create_summary(df)
    return summary


@debug
def new_db_record(summary: dict):
    db = Dynamo()
    db.store_summary(summary)


@debug
def read_sqs(**event):
    for record in event['Records']:
        body = json.loads(record['body'])
        for rec in body['Records']:
            summary = new_summary(rec['s3']['object']['key'])
            new_db_record(summary)
            delete_sqs(record['receiptHandle'])
