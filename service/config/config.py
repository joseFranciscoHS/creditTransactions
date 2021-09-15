import os
import logging
import boto3


class Config:
    """
    This class sets up global variables to be used in this service.
    Reads the following environmet variables:
        'BUCKET': is the S3 bucket to be used.
        'FOLDER': is the S3 folder where the csv files are going the be stored.
        'LOGGLEVEL': is the level to be set for logging in CloudWatch.
        'TABLE': is the dynamodb table to store the generated summaries.
        'QUEUE': is the url of the sqs used to trigger the lambda.
        'SENDER': is the email of the sender.
        'PASSWORD': is password of the sender email.
    """
    BUCKET = os.environ['BUCKET']
    FOLDER = os.environ['FOLDER']
    LOGLEVEL = os.environ['LOGLEVEL']
    TABLE = os.environ['TABLE']
    QUEUE = os.environ['QUEUE']
    SENDER = os.environ['SENDER']
    PASSWORD = os.environ['PASSWORD']

    def get_logger(self) -> logging.Logger:
        """Initiates a new logger session."""
        logger = logging.getLogger()
        logger.setLevel(self.LOGLEVEL)
        return logger

    def get_boto_client(self, clientname: str) -> boto3.client:
        """Initiates a new boto3 client."""
        return boto3.client(clientname)

    def get_boto_resource(self, resourcename: str) -> boto3.client:
        """Initiates a new boto3 resource."""
        return boto3.resource(resourcename)
