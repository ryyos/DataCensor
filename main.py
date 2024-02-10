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


    @task.command('gofood')
    @click.option('--s3', '-s3', is_flag=True, default=False)
    @click.option('--thread', '-th',  is_flag=True, default=False)
    @click.option('--save', '-sv',  is_flag=True, default=False)
    def gofood(s3: bool, save: bool, thread: bool):
        sof = Gofood(s3, save, thread)
        sof.main()


    @task.command('softonic')
    @click.option('--s3', '-s3', is_flag=True, default=False)
    @click.option('--thread', '-th',  is_flag=True, default=False)
    @click.option('--save', '-sv',  is_flag=True, default=False)
    def softonic(s3: bool, save: bool, thread: bool):
        sof = Softonic(s3, save, thread)
        sof.main()


    @task.command('appsapk')
    def appsapk():
        sof = AppsApk()
        sof.main()


    @task.command('uptodown')
    def uptodown():
        sof = Uptodown()
        sof.main()


    @task.command('mister_aladin')
    def mister_aladin():
        sof = MisterAladin()
        sof.main()


    @task.command('indeed')
    def indeed():
        ind = Indeed()
        ind.main()


    @task.command('4shared')
    @click.option('--save', '-sv',  is_flag=True, default=False)
    def fourShared(save: bool):
        start = perf_counter()

        sof = FourShared(save)
        sof.main()

        Runtime.end(start, perf_counter())



if __name__=='__main__':
    main = Main()
    main.task()