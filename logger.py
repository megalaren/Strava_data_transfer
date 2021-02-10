import logging
from datetime import datetime


logger = logging.getLogger(__name__)

# logger setup
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
name = 'logs_' + datetime.now().strftime('%d-%m-%Y_%H-%M-%S') + '.log'
file_handler = logging.FileHandler(name)

file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
