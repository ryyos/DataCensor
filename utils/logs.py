import os

from typing import List
from time import strftime

from utils import *
class Logs:
    def __init__(self, domain: str, path_log: str, path_monitoring: str) -> None:

        self.DOMAIN = domain
        self.PATH_LOG = path_log
        self.PATH_MONITORING = path_monitoring

        self.__logs: List[dict] = []
        self.__monitorings: List[dict] = []
        ...

    def logging(self,
                total: int, 
                failed: int, 
                success: int,
                id_product: any,
                sub_source: str,
                id_review: int,
                status_runtime: str,
                status_conditions: str,
                type_error: str,
                message: str):

        uid_found = False

        try: os.makedirs(f'{"/".join(self.PATH_LOG.split("/")[:-1])}')
        except Exception: ...


        monitoring = {
            "Crawlling_time": now(),
            "id_project": None,
            "project": "Data Intelligence",
            "sub_project": "data review",
            "source_name": self.DOMAIN,
            "sub_source_name": sub_source,
            "id_sub_source": id_product,
            "total_data": total,
            "total_success": success,
            "total_failed": failed,
            "status": status_conditions,
            "assign": "Rio"
        }

        log = {
            "Crawlling_time": now(),
            "id_project": None,
            "project": "Data Intelligence",
            "sub_project": "data review",
            "source_name": self.DOMAIN,
            "sub_source_name": sub_source,
            "id_sub_source": id_product,
            "id_review": id_review,
            "process_name": "Crawling",
            "status": status_runtime,
            "type_error": type_error,
            "message": message,
            "assign": "Rio"
        }

        for index, data in enumerate(self.__monitorings):
            if id_product == data["id_sub_source"]:
                self.__monitorings[index]["total_data"] = total
                self.__monitorings[index]["total_success"] = success
                self.__monitorings[index]["total_failed"] = failed
                self.__monitorings[index]["status"] = status_conditions
                uid_found = True
                break

        if not uid_found:
            self.__monitorings.append(monitoring)

        if not total:
            self.__monitorings.append(monitoring)
            File.write_json(self.PATH_MONITORING, self.__monitorings)

        else:
            File.write_json(self.PATH_MONITORING, self.__monitorings)
            
            if not id_review and status_conditions == 'done':
                ...
            else:
                self.__logs.append(log)
                File.write_json(self.PATH_LOG, self.__logs)
                
        ...
