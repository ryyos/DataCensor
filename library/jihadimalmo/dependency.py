
from components import JihadimalmoComponent
from ApiRetrys import ApiRetry

class JihadimalmoLibs(JihadimalmoComponent):
    def __init__(self) -> None:
        super().__init__()

        self.api = ApiRetry(show_logs=True, defaulth_headers=True)
        ...