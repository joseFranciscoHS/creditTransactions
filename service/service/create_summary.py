from service.model.decorators import LOGGER
from ..model.transactions import Transaction
from ..config.config import Config
from ..model.database import Dynamo
from ..model.decorators import debug
from ..model.email import Mail
import json


@debug
def delete_sqs(receipt: str):
    """Once an sqs message has finished working with, it is deleted."""
    cfg = Config()
    sqs = cfg.get_boto_client('sqs')
    sqs.delete_message(QueueUrl=cfg.QUEUE, ReceiptHandle=receipt)


@debug
def new_summary(key: str):
    """Creates the summary of transactions."""
    trns = Transaction()
    df = trns.read_transactions(key)
    summary = trns.create_summary(df)
    trns.save_summary(summary)
    return summary


@debug
def new_db_record(summary: dict):
    """Writes the summary to dynamodb."""
    db = Dynamo()
    db.store_summary(summary)


@debug
def send_mail(summary: dict):
    """Sends the summary through an email."""
    mail = Mail()
    mail.new_mail(summary)


@debug
def read_sqs(**event):
    """Reads the information of the sqs message sent to this lambda, and starts the process."""
    for record in event['Records']:
        body = json.loads(record['body'])
        for rec in body['Records']:
            summary = new_summary(rec['s3']['object']['key'])
            new_db_record(summary)
            send_mail(summary)
            delete_sqs(record['receiptHandle'])
