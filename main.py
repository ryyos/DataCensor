import os
import click

from services import Softonic
from services import AppsApk
from services import Gofood
from services import Uptodown
from services import MisterAladin
from services import Indeed

class Main:
    
    @click.group()
    @staticmethod
    def task(): ...


    @task.command('gofood')
    @click.option('--s3', '-s3', is_flag=True, default=False)
    @click.option('--thread', '-th',  is_flag=True, default=False)
    @click.option('--save', '-sv',  is_flag=True, default=False)
    def gofood(s3, thread, save):
        sof = Gofood(s3, save, thread)
        sof.main()


    @task.command('softonic')
    def softonic():
        sof = Softonic()
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

if __name__=='__main__':
    main = Main()
    main.task()