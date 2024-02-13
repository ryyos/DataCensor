import os
import mysql.connector

from dotenv import load_dotenv

class SQL:

    def __init__(self) -> None:
        load_dotenv()

        self.connection = mysql.connector.connect(
            host='127.0.0.1',
            user=os.getenv('USER_SQL'),
            password=os.getenv('PASS_SQL'),
            database="datacensor"
        )
        ...
