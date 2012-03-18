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

APP_PYTHON = os.path.join(settings.APP_DIR, 'bin', 'python')

def scrape(*args):
    call_args = ['python']
    s(call_args.extend(args))

if __name__ == '__main__':
    backoff = random.randint(0, 10)
    time.sleep(backoff * 60)

    # English premier league
    # bundesliga
    subprocess.call([APP_PYTHON, 'scrapers/sbs.py'])

    # afl
    subprocess.call([APP_PYTHON, 'scrapers/afl.py'])
