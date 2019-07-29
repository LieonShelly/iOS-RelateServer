import redis
from flask import current_app
from flask import request, abort


class RedisClient(object):
    def init_app(self, app):
        host = app.config['REDIS_HOST']
        port = app.config['REDIS_PORT']
        password = app.config['REDIS_PASSWORD']
        pool = redis.ConnectionPool(host=host, port=port, password=password, decode_responses=True)
        self.db = redis.StrictRedis(connection_pool=pool)

    # def __init__(self, host=current_app.config['REDIS_HOST'], port=current_app.config['REDIS_PORT'], password=urrent_app.config['REDIS_PASSWORD']):
    #     pool = redis.ConnectionPool(host=host, port=port, password=password, decode_responses=True)
    #     self.db = redis.StrictRedis(connection_pool=pool)
        
    def hm_set(self,db_key, mapping):
        self.db.hmset(db_key, mapping)
    
    def hm_get(self,db_key, field):
       return self.db.hmget(db_key, field)

    def zremrangebyscore(self, name, min, max):
        self.db.zremrangebyscore(name, min=min, max=max)

    def zrangebyscore(self,name, min, max):
       return self.db.zrangebyscore(name, min=min, max=max)

    def zadd(self, db_key, mapping):
         self.db.zadd(db_key, mapping)

    def zscore(self, db_key, filed):
        self.db.zscore(name=db_key, value=filed)

    def zincrby(self, name, value, amount):
        self.db.zincrby(name=name, value=value, amount=amount)
    
    def zscore(self, name, value):
       return self.db.zscore(name=name, value=value)

    def zcard(self,name):
       return self.db.zcard(name)
        
    def set(self, key, value, expire_time=None):
          self.db.set(key, value, expire_time)
    
    def get(self,key):
        try:
           return self.db.get(key)
        except:
            abort(403)
            return {"msg": "redis error"}

    def incrby(self, name, amount):
        self.db.incrby(name=name, amount=amount)

    def delete(self, key):
        self.db.delete(key)

