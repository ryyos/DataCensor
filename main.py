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


    @task.command('softonic')
    def softonic():
        sof = Softonic()
        sof.main()


    @task.command('appsapk')
    def appsapk():
        sof = AppsApk()
        sof.main()


    @task.command('gofood')
    def gofood():
        sof = Gofood()
        sof.main()


    @task.command('uptodown')
    def uptodown():
        sof = Uptodown()
        sof.main()


    @task.command('mister_aladin')
    def mister_aladin():
        sof = MisterAladin()
        sof.main()


    @task.command('mister_aladin')
    def mister_aladin():
        ind = Indeed()
        ind.main()

if __name__=='__main__':
    main = Main()
    main.task()