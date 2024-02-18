import os
import click
from time import perf_counter
from utils import Runtime

from services import *
from share import *

class Main:

    @click.group()
    @staticmethod
    def task(): ...
    
    @task.group('reviews')
    @staticmethod
    def reviews(): ...

    @task.group('admiralty')
    @staticmethod
    def admiralty(): ...

    @task.group('shared')
    @staticmethod
    def shared():... 

    @task.group('download')
    @staticmethod
    def download():... 

    """ <----------------------[ REVIEWS ]-------------------------->"""

    @reviews.command('gofood')
    @click.option('--s3', '-s3', is_flag=True, default=False)
    @click.option('--thread', '-th',  is_flag=True, default=False)
    @click.option('--save', '-sv',  is_flag=True, default=False)
    def gofood(s3: bool, save: bool, thread: bool):
        start = perf_counter()

        sof = Gofood(save=save, s3=s3, thread=thread)
        sof.main()

        Runtime.end(start, perf_counter())


    @reviews.command('softonic')
    @click.option('--s3', '-s3', is_flag=True, default=False)
    @click.option('--thread', '-th',  is_flag=True, default=False)
    @click.option('--save', '-sv',  is_flag=True, default=False)
    def softonic(s3: bool, save: bool, thread: bool):
        start = perf_counter()

        sof = Softonic(save=save, s3=s3, thread=thread)
        sof.main()

        Runtime.end(start, perf_counter())


    @reviews.command('appsapk')
    @click.option('--s3', '-s3', is_flag=True, default=False)
    @click.option('--thread', '-th',  is_flag=True, default=False)
    @click.option('--save', '-sv',  is_flag=True, default=False)
    def appsapk(s3: bool, save: bool, thread: bool):
        start = perf_counter()

        sof = AppsApk(save=save, s3=s3, thread=thread)
        sof.main()

        Runtime.end(start, perf_counter())


    @reviews.command('uptodown')
    @click.option('--s3', '-s3', is_flag=True, default=False)
    @click.option('--thread', '-th',  is_flag=True, default=False)
    @click.option('--save', '-sv',  is_flag=True, default=False)
    def uptodown(s3: bool, save: bool, thread: bool):
        start = perf_counter()

        sof = Uptodown(save=save, s3=s3, thread=thread)
        sof.main()

        Runtime.end(start, perf_counter())


    @reviews.command('mister_aladin')
    @click.option('--s3', '-s3', is_flag=True, default=False)
    @click.option('--thread', '-th',  is_flag=True, default=False)
    @click.option('--save', '-sv',  is_flag=True, default=False)
    def mister_aladin(s3: bool, save: bool, thread: bool):
        start = perf_counter()

        sof = MisterAladin(save=save, s3=s3, thread=thread)
        sof.main()

        Runtime.end(start, perf_counter())

    """ <----------------------[ ADMIRALTY ]-------------------------->"""

    @admiralty.command('4shared')
    @click.option('--s3', '-s3', is_flag=True, default=False)
    @click.option('--thread', '-th',  is_flag=True, default=False)
    @click.option('--save', '-sv',  is_flag=True, default=False)
    @click.option('--url', '-u', required=True, type=str)
    @click.option('--type', '-t', required=True, type=str)
    def fourShared(s3: bool, save: bool, thread: bool, url: str, type: str):
        start = perf_counter()

        sof = FourShared(save=save, s3=s3, thread=thread, url=url, type=type)
        sof.main()

        Runtime.end(start, perf_counter())

    @admiralty.command('jihadimalmo')
    @click.option('--s3', '-s3', is_flag=True, default=False)
    @click.option('--thread', '-th',  is_flag=True, default=False)
    @click.option('--save', '-sv',  is_flag=True, default=False)
    def jihadimalmo(s3: bool, save: bool, thread: bool):
        start = perf_counter()

        sof = Jihadimalmo(save=save, s3=s3, thread=thread)
        sof.main()

        Runtime.end(start, perf_counter())


    @admiralty.command('trop')
    @click.option('--all', '-a',  is_flag=True, default=False)
    def theReligionOfPeace(all: bool):
        start = perf_counter()

        trop = TheReligionOfPeace(all=all)
        trop.main()

        Runtime.end(start, perf_counter())

    """ <----------------------[ SHARE FROM LOCAL ]-------------------------->"""

    @shared.command('s3v2')
    @click.option('--source', '-sc', required=True, type=str)
    @click.option('--change', '-c',  is_flag=True, default=False)
    @click.option('--new_path', '-np', required=False, type=str)
    @click.option('--start_path', '-st', required=False, type=str)
    def sharev2(source: str, new_path: str, change: bool, start_path: int):
        start = perf_counter()

        share = ShareV2()
        share.main(source=source, change_path=change, new_path=new_path, start_main_path=start_path)

        Runtime.end(start, perf_counter())

    @shared.command('s3')
    @click.option('--source', '-sc', required=True, type=str)
    def share(source: str):
        start = perf_counter()

        share = Share(base_path=source)
        share.main()

        Runtime.end(start, perf_counter())

    @shared.command('kafka')
    @click.option('--source', '-sc', required=True, type=str)
    @click.option('--topic', '-t', required=True, type=str)
    def share(source: str, topic: str):
        start = perf_counter()

        share = ShareKafka(base_path=source, topic=topic)
        share.main()

        Runtime.end(start, perf_counter())

    @shared.command('trop')
    @click.option('--source', '-sc', required=True, type=str)
    @click.option('--topic', '-t', required=True, type=str)
    def share(source: str, topic: str):
        start = perf_counter()

        share = TheReligionOfPeaceShare(base_path=source, topic=topic)
        share.main()

        Runtime.end(start, perf_counter())

    """ <----------------------[ INSTAN DOWNLOAD ]-------------------------->"""

    @download.command('down')
    @click.option('--url', '-u', required=True, type=str)
    @click.option('--domain', '-d', required=True, type=str)
    @click.option('--path', '-p', required=False, type=str, default=None)
    @click.option('--save', '-sv',  is_flag=True, default=False)
    @click.option('--s3', '-s3', is_flag=True, default=False)
    def down(url: str, domain: str, s3:bool, save: bool, path: str) -> None:
        start = perf_counter()

        down = Download(save=save, s3=s3)
        down.main(url=url, domain=domain, path=path)

        Runtime.end(start, perf_counter())
        ...



if __name__=='__main__':
   main = Main()
   main.task()
   ...
    