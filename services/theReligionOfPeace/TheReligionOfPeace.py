
from icecream import ic

from library import TheReligionOfPeaceLibs

class TheReligionOfPeace(TheReligionOfPeaceLibs):
    def __init__(self, stream: bool, all: bool) -> None:
        super().__init__()

        self.stream: bool = stream
        self.all: bool = all
        ...

    def main(self) -> None:

        if self.all:
            for year, url in self.collect_year(self.main_url):
                ic(year)
                ic(url)
            ...
        ...