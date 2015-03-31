import redis
import json

r = redis.StrictRedis()

print type(json.dumps(r.hgetall('platforms')))

application_data = r.lrange('application_data', 0, -1)
for i in application_data:
    print i
    print type(i)
