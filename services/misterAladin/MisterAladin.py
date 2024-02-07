import os
import requests

from pyquery import PyQuery
from requests import Response
from library import MisterAladinLibs
from dekimashita import Dekimashita
from concurrent.futures import ThreadPoolExecutor, wait
from typing import List
from time import time
from icecream import ic
from component import codes
from tqdm import tqdm
from utils import *

class MisterAladin(MisterAladinLibs):
    def __init__(self) -> None:
        super().__init__()
        
        self.__executor = ThreadPoolExecutor(max_workers=5)
        ...

    def get_reviews(self, headers: dict) -> None:
        response: Response = self.api.get(url=self.API_REVIEW+str(headers["id"]), params=self.build_param_review(1))

        all_reviews: List[dict] = []
        error: List[dict] = []

        if response.status_code == 200:

            detail_reviews: List[dict] = [
                {
                    "score_rating": detail["value"],
                    "category_rating": detail["name_en"]
                } for detail in response.json()["data"]["criteria"]
            ]
            
            for page in range(response.json()["meta"]["total_pages"]):
                response: Response = self.api.get(url=self.API_REVIEW+str(headers["id"]), params=self.build_param_review(page))

                reviews = [{
                  "id_review": review["category"]["id"],
                  "username_reviews": review["username"],
                  "image_reviews": None,
                  "created_time": change_format(review["reviewed_at"]),
                  "created_time_epoch": convert_time(change_format(review["reviewed_at"])),
                  "email_reviews": None,
                  "company_name": None,
                  "location_reviews": None,
                  "title_detail_reviews": review["title"],
                  "reviews_rating": review["total_score"],
                  "detail_reviews_rating": None,
                  "total_likes_reviews": None,
                  "total_dislikes_reviews": None,
                  "total_reply_reviews": None,
                  "content_reviews": review["description"],
                  "reply_content_reviews": {
                    "username_reply_reviews": None,
                    "content_reviews": None
                  },
                  "date_of_experience": change_format(review["reviewed_at"]),
                  "date_of_experience_epoch": convert_time(change_format(review["reviewed_at"]))
                } for review in response.json()["data"]["review"]] if response.status_code == 200 else error.append({
                    "message": response.text,
                    "type": codes[str(response.status_code)],
                    "id": None
                })

                all_reviews.extend(reviews)
                ...

            total_error = 0
            for index, review in enumerate(all_reviews):

                path = f'{self.create_dir(headers)}/{review["username_reviews"]}.json'
                
                headers["reviews_rating"]["detail_total_rating"] = detail_reviews
                headers.update({
                    "detail_reviews": review,
                    "path_data_raw": 'S3://ai-pipeline-statistics/'+path,
                    "path_data_clean": 'S3://ai-pipeline-statistics/'+convert_path(path)
                })

                # response: int = self.s3.upload(path, Dekimashita.vdict(headers, ['\n', '\r']), self.bucket)
                response = 200

                self.logs.logsS3(func=self.logs,
                                            all_reviews=all_reviews,
                                            error=error,
                                            header=headers,
                                            index=index,
                                            response=response,
                                            total_err=total_error)

                # File.write_json(path, Dekimashita.vdict(headers, ['\n']))

        ic('panggil out')
        self.logs.zero(func=self.logs,
                                  header=headers)
        
        ...

    def extract_detail(self, hotel: dict, url: str) -> dict[str, any]:
        response: Response = self.api.get(url)
        html = PyQuery(response.text)

        headers = {
            "id": hotel["id"],
            "email": hotel["email"],
            "link": url,
            "domain": self.DOMAIN,
            "tag": ['www.misteraladin.com'],
            "crawling_time": now(),
            "crawling_time_epoch": int(time()),
            "path_data_raw": "",
            "path_data_clean": "",
            "reviews_name": hotel["name"],
            "location_reviews": hotel["address"],
            "category_reviews": "travel",
            "star_hotel": hotel["star_rating"],

            "description": Dekimashita.vtext(self.set_descriptions(html)),
            "country": hotel["area"]["city"]["state"]["country"]["slug"],
            "city": hotel["area"]["city"]["slug"],
            "subdistrict": hotel["area"]["slug"],
            "tourist_attraction": self.tourist_attraction(hotel),
            "available_rooms": self.available_rooms(hotel),

            "total_reviews": hotel["review"]["count"],
            "reviews_rating": {
              "total_rating": hotel["review"]["score"],
              "detail_total_rating": []
            }
        }

        path_detail = f'{self.create_dir(headers)}/detail/{Dekimashita.vdir(headers["reviews_name"]).lower()}.json'
        headers.update({
            "path_data_raw": 'S3://ai-pipeline-statistics/'+path_detail,
            "path_data_clean": 'S3://ai-pipeline-statistics/'+convert_path(path_detail)
        })

        File.write_json(path_detail, Dekimashita.vdict(headers, ['\n']))
        # response = self.s3.upload(key=path_detail, body=Dekimashita.vdict(headers, ['\n', '\r']), bucket=self.bucket)
        # ic(response)
        self.get_reviews(headers)
        ...

    def extract_hotel(self, hotel: dict) -> None:

        url: str = self.build_url(hotel)
        self.extract_detail(hotel, url)

        ...


    def main(self) -> None:
        
        for city in range(1000):

            page = 1
            while True:
                hotels: list[dict] = self.collect_hotels(city_id=city+1, page=page)
                if not hotels: break
                ic(page)
                page+=1
                
                task_executor = []
                for hotel in tqdm(hotels, ascii=True, smoothing=0.1, total=len(hotels)):

                    task_executor.append(self.__executor.submit(self.extract_hotel, hotel))
                    # self.extract_hotel(hotel)
                
                wait(task_executor)
                    
        
        self.__executor.shutdown(wait=True)




# https://www.misteraladin.com/api/hotel-review/review/hotel/328473?sort=newest&page=1&perpage=10
# https://www.misteraladin.com/hotel-review/review/hotel/328473?page=1&perpage=10&sort=newest