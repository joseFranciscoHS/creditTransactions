from ..service.create_summary import read_sqs
from ..config.config import Config

LOGGER = Config().get_logger()

def lambda_handler(event, context):
    """This function starts the process."""
    LOGGER.info(f'Starting process with the following data {event}')
    read_sqs(**event)