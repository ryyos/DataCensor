
from typing import List
from time import strftime

from utils import *
class Logs:
    def __init__(self, domain: str, path_log: str, path_monitoring: str) -> None:

        self.DOMAIN = domain
        self.PATH_LOG = path_log
        self.PATH_MONITORING = path_monitoring

        self.__datas: List[dict] = []
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

        content = {
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

        monitoring = {
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

        for index, data in enumerate(self.__datas):
            if id_product == data["id_sub_source"]:
                self.__datas[index]["total_data"] = total
                self.__datas[index]["total_success"] = success
                self.__datas[index]["total_failed"] = failed
                self.__datas[index]["status"] = status_conditions
                uid_found = True
                break

        if not uid_found:
            self.__datas.append(content)

        self.__monitorings.append(monitoring)
        File.write_json(self.PATH_MONITORING, self.__datas)
        if not id_review and status_conditions is not 'done':
            File.write_json(self.PATH_LOG, self.__monitorings)
        ...
