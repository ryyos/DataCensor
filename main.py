import os
import click

from click.core import Context
from time import perf_counter
from utils import Stream

from services import *
from share import *

class Main:

    @click.group()
    @staticmethod
    def task(): ...
    
    @task.group('reviews')
    @click.option('--s3', '-s3', is_flag=True, default=False)
    @click.option('--thread', '-th',  is_flag=True, default=False)
    @click.option('--save', '-sv',  is_flag=True, default=False)
    @click.pass_context
    @staticmethod
    def reviews(ctx: Context, **kwargs):
        ctx.obj = kwargs
        ...

    @task.group('admiralty')
    @click.option('--s3', '-s3', is_flag=True, default=False)
    @click.option('--thread', '-th',  is_flag=True, default=False)
    @click.option('--save', '-sv',  is_flag=True, default=False)
    @click.option('--type', '-t', required=False, type=str)
    @click.pass_context
    @staticmethod
    def admiralty(ctx: Context, **kwargs):
        ctx.obj = kwargs
        ...

    @task.group('shared')
    @staticmethod
    def shared():... 

    @task.group('download')
    @staticmethod
    def download():... 

    """ <----------------------[ REVIEWS ]-------------------------->"""

    @reviews.command('gofood')
    @click.pass_context
    def gofood(ctx: Context):
        start = perf_counter()

        gof = Gofood(save=ctx.obj['save'], s3=ctx.obj['s3'], thread=ctx.obj['thread'])
        gof.main()

        Stream.end(start, perf_counter())


    @reviews.command('softonic')
    @click.pass_context
    def softonic(ctx: Context):
        start = perf_counter()

        sof = Softonic(save=ctx.obj['save'], s3=ctx.obj['s3'], thread=ctx.obj['thread'])
        sof.main()

        Stream.end(start, perf_counter())


    @reviews.command('appsapk')
    @click.pass_context
    def appsapk(ctx: Context):
        start = perf_counter()

        app = AppsApk(save=ctx.obj['save'], s3=ctx.obj['s3'], thread=ctx.obj['thread'])
        app.main()

        Stream.end(start, perf_counter())


    @reviews.command('uptodown')
    @click.pass_context
    def uptodown(ctx: Context):
        start = perf_counter()

        up = Uptodown(save=ctx.obj['save'], s3=ctx.obj['s3'], thread=ctx.obj['thread'])
        up.main()

        Stream.end(start, perf_counter())


    @reviews.command('mister_aladin')
    @click.pass_context
    def mister_aladin(ctx: Context):
        start = perf_counter()

        mis = MisterAladin(save=ctx.obj['save'], s3=ctx.obj['s3'], thread=ctx.obj['thread'])
        mis.main()

        Stream.end(start, perf_counter())

    """ <----------------------[ ADMIRALTY ]-------------------------->"""

    @admiralty.command('4shared')
    @click.option('--url', '-u', required=False, type=str)
    @click.pass_context
    def fourShared(ctx: Context, url: str):
        start = perf_counter()

        sof = FourShared(save=ctx.obj['save'], s3=ctx.obj['s3'], thread=ctx.obj['thread'], url=url, type=ctx.obj['type'])
        sof.main()

        Stream.end(start, perf_counter())

    @admiralty.command('jihadimalmo')
    @click.pass_context
    def jihadimalmo(ctx: Context):
        start = perf_counter()

        sof = Jihadimalmo(save=ctx.obj['save'], s3=ctx.obj['s3'], thread=ctx.obj['thread'])
        sof.main()

        Stream.end(start, perf_counter())


    @admiralty.command('trop')
    @click.option('--all', '-a',  is_flag=True, default=False)
    def theReligionOfPeace(all: bool):
        start = perf_counter()

        trop = TheReligionOfPeace(all=all)
        trop.main()

        Stream.end(start, perf_counter())


    @admiralty.command('archive')
    @click.option('--url', '-u', required=True, type=str)
    @click.pass_context
    def archive(ctx: Context, url: str):
        start = perf_counter()

        arch = Archive(save=ctx.obj['save'], s3=ctx.obj['s3'], threads=ctx.obj['thread'], url=url, types=ctx.obj['type'])
        arch.main()

        Stream.end(start, perf_counter())

    @admiralty.command('bri')
    def bri():
        start = perf_counter()

        bri = Bri()
        bri.main()

        Stream.end(start, perf_counter())

    @admiralty.command('mandiri')
    def maindiri():
        start = perf_counter()

        maindiri = Bankmandiri()
        maindiri.main()

        Stream.end(start, perf_counter())


    @admiralty.command('btn')
    def btn():
        start = perf_counter()

        bt = Btn()
        bt.main()

        Stream.end(start, perf_counter())

    @admiralty.command('danamon')
    def danamon():
        start = perf_counter()

        danamon = Danamon()
        danamon.main()

        Stream.end(start, perf_counter())

    @admiralty.command('permata')
    def danamon():
        start = perf_counter()

        permata = Permata()
        permata.main()

        Stream.end(start, perf_counter())


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

        Stream.end(start, perf_counter())

    @shared.command('s3')
    @click.option('--source', '-sc', required=True, type=str)
    def share(source: str):
        start = perf_counter()

        share = Share(base_path=source)
        share.main()

        Stream.end(start, perf_counter())

    @shared.command('kafka')
    def share():
        start = perf_counter()

        share = ShareKafka()
        share.main()

        Stream.end(start, perf_counter())

    @shared.command('trop')
    @click.option('--source', '-sc', required=True, type=str)
    @click.option('--topic', '-t', required=True, type=str)
    def share(source: str, topic: str):
        start = perf_counter()

        share = TheReligionOfPeaceShare(base_path=source, topic=topic)
        share.main()

        Stream.end(start, perf_counter())

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

        Stream.end(start, perf_counter())
        ...



if __name__=='__main__':
   Main.task()
   ...
    