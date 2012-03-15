import random
import subprocess
import time

def scrape(*args):
    call_args = ['python']
    s(call_args.extend(args))

if __name__ == '__main__':
    backoff = random.randint(0, 10)
    time.sleep(backoff * 60)

    # English premier league
    subprocess.call(['python','scrapers/sbs.py'])

    # afl
    subprocess.call(['python','scrapers/afl.py'])
