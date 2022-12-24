import time
import redis

while True:
    r = redis.Redis(host='localhost', port=26379)
    print(r.get('key'))
    time.sleep(1)