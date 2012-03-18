import logging
import random
import time
import traceback
import os
import sys

try:
    import settings
except ImportError:
    sys.path.append(os.path.dirname(__file__))
    import settings

sys.path.append(os.path.join(settings.APP_DIR, 'scrapers'))

import sbs
import afl

logging.basicConfig(filename=settings.LOG_FILE, level=logging.ERROR)

def scrape(module, league):
    try:
        module.scrape_league(league)
    except Exception as e:
        a = traceback.format_exc()
        logging.error(a)
        pass

if __name__ == '__main__':
    # backoff = random.randint(0, 10)
    # time.sleep(backoff * 60)

    # sbs
    scrape(sbs, 'epl')
    scrape(sbs, 'bundesliga')

    # afl
    scrape(afl,'afl')
