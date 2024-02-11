import click

from share import FourSharedShere

class Shared:

    @click.group()
    @staticmethod
    def task():... 


    @task.command('4shared')
    def fourShared():
        four = FourSharedShere()
        four.main()


if __name__ == '__main__':
    shared = Shared()
    shared.task()