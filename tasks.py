import random
import subprocess
import time
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

def scrape(module, league):
    try:
        module.scrape_league(league)
    except:
        # Do some logging.
        pass

if __name__ == '__main__':
    # backoff = random.randint(0, 10)
    # time.sleep(backoff * 60)

    # sbs
    scrape(sbs, 'epl')
    scrape(sbs, 'bundesliga')

    # afl
    scrape(afl,'afl')
