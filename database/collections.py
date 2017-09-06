from .import Mongua
import json
import redis
import time
class Cache(object):
    def get(self, key):
        pass

    def set(self, key, value):
        pass

class RedisCache(Cache):
    redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)

    def set(self, key, value):
        return RedisCache.redis_db.set(key, value)

    def get(self, key):
        return RedisCache.redis_db.get(key)

class Collections(Mongua):

    __fields__ = Mongua.__fields__ + [
        ('username', str, ''),
        ('date', str, ''),
        ('movieid', str, ''),
    ]

    def to_json(self):
        # return (json.dumps(self, default=lambda obj: obj.__dict__))
        d = dict()
        for k in Collections.__fields__:
            key = k[0]
            if not key.startswith('_'):
                d[key] = getattr(self, key)
        return json.dumps(d)

    @classmethod
    def from_json(cls, j):
        d = json.loads(j)
        instance = cls()
        for k, v in d.items():
            setattr(instance, k, v)
        return instance

    @classmethod
    def all_delay(cls):
        time.sleep(3)
        return Collections.all()

    should_update_all = True
    redis_cache = RedisCache()

    @classmethod
    def cache_all(cls):
        #  redis cache
        if Collections.should_update_all:
            Collections.redis_cache.set('Collections_all', json.dumps([i.to_json() for i in cls.all_delay()]))
            Collections.should_update_all = False
        j = json.loads(Collections.redis_cache.get('Collections_all').decode('utf-8'))
        j = [Collections.from_json(i) for i in j]
        return j