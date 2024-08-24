import logging


class Logging:
    def __init__(self):
        self.logging = logging.getLogger(__name__)
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                            filename='app.log',
                            encoding='utf-8',
                            filemode='w',
                            level=logging.INFO)

    def debug(self, message: str):
        self.logging.debug(message)

    def info(self, message: str):
        self.logging.info(message)