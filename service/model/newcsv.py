from pandas._config import config
from .decorators import debug
from ..config.config import Config
from io import StringIO
import pandas as pd


class NewCSV(Config):

    def __init__(self) -> None:
        Config.__init__(self)
        self.s3client = self.get_boto_client('s3')

    def read_object(self, obj: 'client.get_object') -> str:
        """Converts object body to str"""
        body = obj['Body']
        body = body.read().decode('utf-8')
        return StringIO(body)
    
    @debug
    def read_from_s3(self, filename: str, **kwargs) -> pd.DataFrame:
        info = self.s3client.get_object(Bucket=self.BUCKET, Key=self.FOLDER + '/' + filename)
        info = self.read_object(info)
        return pd.read_csv(info, **kwargs)
