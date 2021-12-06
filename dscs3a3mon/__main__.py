import logging
import time
from decouple import config, UndefinedValueError
from monitor import Monitor
from commands import COMMANDS

FORMAT = '[%(asctime)s %(levelname)s] %(message)s'


if __name__ == '__main__':
    logging.basicConfig(format=FORMAT, level=logging.INFO, filename='dscs.log')
    try:
        webhook = config('WEBHOOK')
    except UndefinedValueError:
        print('no webhook set in .env file!')
        raise SystemExit

    mon = Monitor(webhook)

    while True:
        for cmd in COMMANDS:
            mon.command(cmd)
        logging.info('waiting 10 minutes...')
        time.sleep(600)
