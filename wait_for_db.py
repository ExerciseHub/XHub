import time
from django.db import connections
from django.db.utils import OperationalError

def wait_for_db(max_retries=5, delay=5):
    db_conn = None
    retries = 0
    while not db_conn and retries < max_retries:
        try:
            db_conn = connections['default']
        except OperationalError:
            retries += 1
            time.sleep(delay)

if __name__ == "__main__":
    wait_for_db()
