import logging
from click import style

logging.basicConfig(datefmt='%m/%d/%Y %I:%M:%S %p', encoding="utf-8", level=logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

console = logging.StreamHandler()
console.setLevel(level=logging.DEBUG) 
console.setFormatter(formatter)

logger = logging.getLogger()
for existing_handler in logger.handlers[:]:
       logger.removeHandler(existing_handler)

logger.addHandler(console)

class Runtime:

       @staticmethod
       def info(name: str, total: int, success: int, error: int) -> None:
              logger.info(f'[ {style(name, fg="bright_green")} ] :: {style("total data", fg="magenta")}: [ {total} ] | {style("success", fg="bright_blue")}: [ {success} ] | {style("error", fg="red")}: [ {error} ]')

       @staticmethod
       def cards(name: str, text: str, page: int, total: int) -> None:
              logger.info(f'[ {style(name, fg="bright_green")} ] :: {style(f"total {text}", fg="magenta")}: [ {total} ] | {style("page", fg="magenta")}: [ {page} ]')

       @staticmethod
       def s3(bucket: str, response: int) -> None:
              logger.info(f'[ {style("UPLOAD TO S3", fg="bright_green")} ] :: {style(f"bucket", fg="magenta")}: [ {bucket} ] | {style("response", fg="magenta")}: [ {response} ]')

       @staticmethod
       def end(start: float, end: float) -> float:
              logger.info(f'[ {style(end, fg="red")} ] :: {style(f"time", fg="magenta")}: [ {start - end} ]')