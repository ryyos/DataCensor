import os
import click
from time import perf_counter
from utils import Runtime

from services import Softonic
from services import AppsApk
from services import Gofood
from services import Uptodown
from services import MisterAladin
from services import Indeed
from services import FourShared

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

    """ <----------------------[ REVIEWS ]-------------------------->"""

    @reviews.command('gofood')
    @click.option('--s3', '-s3', is_flag=True, default=False)
    @click.option('--thread', '-th',  is_flag=True, default=False)
    @click.option('--save', '-sv',  is_flag=True, default=False)
    def gofood(s3: bool, save: bool, thread: bool):
        sof = Gofood(save=save, s3=s3, thread=thread)
        sof.main()


    @reviews.command('softonic')
    @click.option('--s3', '-s3', is_flag=True, default=False)
    @click.option('--thread', '-th',  is_flag=True, default=False)
    @click.option('--save', '-sv',  is_flag=True, default=False)
    def softonic(s3: bool, save: bool, thread: bool):
        sof = Softonic(save=save, s3=s3, thread=thread)
        sof.main()


    @reviews.command('appsapk')
    @click.option('--s3', '-s3', is_flag=True, default=False)
    @click.option('--thread', '-th',  is_flag=True, default=False)
    @click.option('--save', '-sv',  is_flag=True, default=False)
    def appsapk(s3: bool, save: bool, thread: bool):
        sof = AppsApk(save=save, s3=s3, thread=thread)
        sof.main()


    @reviews.command('uptodown')
    def uptodown():
        sof = Uptodown()
        sof.main()


    @reviews.command('mister_aladin')
    @click.option('--s3', '-s3', is_flag=True, default=False)
    @click.option('--thread', '-th',  is_flag=True, default=False)
    @click.option('--save', '-sv',  is_flag=True, default=False)
    def mister_aladin(s3: bool, save: bool, thread: bool):
        sof = MisterAladin(save=save, s3=s3, thread=thread)
        sof.main()


    @reviews.command('indeed')
    def indeed():
        ind = Indeed()
        ind.main()


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



if __name__=='__main__':
   main = Main()
   main.task()
   ...
    