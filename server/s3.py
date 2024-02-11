import os
import boto3

from botocore.config import Config

from dotenv import *
from json import dumps
from icecream import ic
from utils import Runtime

class ConnectionS3:
    def __init__(self, access_key_id, secret_access_key, endpoint_url) -> None:
        self.config = Config(retries = {
            "max_attempts": 10,
            "mode": "standard"
        })

        self.__s3 = boto3.client('s3', 
                                 aws_access_key_id= access_key_id, 
                                 aws_secret_access_key=secret_access_key, 
                                 endpoint_url=endpoint_url,
                                #  config=self.config
                                 )
        
        self.__s3_resource = boto3.resource('s3', 
                                endpoint_url=endpoint_url,
                                aws_access_key_id = access_key_id,
                                aws_secret_access_key = secret_access_key
                            ) 

    def upload(self, key: str, body: dict, bucket: str) -> int:
        response: dict = self.__s3.put_object(Bucket=bucket, Key=key, Body=dumps(body, indent=2, ensure_ascii=False))
        self.__s3
        
        Runtime.s3(bucket, response['ResponseMetadata']['HTTPStatusCode'])
        return response['ResponseMetadata']['HTTPStatusCode']
        # return 400
    
    def upload_file(self, path: str, bucket: str, key: str) -> int:
        response: dict = self.__s3_resource.Bucket(bucket).put_object(
                                Key = key, 
                                Body = open(path, 'rb')
                            )
        Runtime.s3(bucket, response['ResponseMetadata']['HTTPStatusCode'])
        return response['ResponseMetadata']['HTTPStatusCode']
        ...
    


if(__name__ == '__main__'):
    load_dotenv()
    conn = ConnectionS3(access_key_id=os.getenv('ACCESS_KEY_ID'),
                                 secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
                                 endpoint_url=os.getenv('ENDPOINT'),
                                 )
    conn.upload('test/initesting2.json', {"apakah_berhasil": True}, os.getenv('BUCKET'))