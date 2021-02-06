import logging
import time
import json
import redis
import uuid

from os import environ

redisClient: redis.Redis = None
redisPubSub: redis.client.PubSub = None

redisDb = environ.get('REDIS_DATABASE')

downloadMap = {}


def InitializeRedis():
    print('Redis: Initializing...')

    global redisClient
    global redisPubSub

    redisClient = redis.Redis(
        connection_pool=redis.ConnectionPool(
            host=environ.get('REDIS_HOST'),
            port=environ.get('REDIS_PORT'),
            password=environ.get('REDIS_PASSWORD'),
            db=environ.get('REDIS_DATABASE'),
            max_connections=16)
    )

    print('Redis: Test for connection')
    if redisClient.ping():
        print('Redis: Succeded.')
    else:
        print('Redis: Couldn\'t establish a redis connection!')
        print('Exiting...')
        exit(1)

    print('Redis: Setup redis pub/sub')
    redisPubSub = redisClient.pubsub()

    redisPubSub.subscribe(**{'chimu:s:downloads': DownloadResponseHandler})

    redisPubSub.run_in_thread(sleep_time=0.001, daemon=True)


async def Request(key: str, obj: any):
    time_current = time.time()
    time_deadline = time_current + 15

    id = str(uuid.uuid4())

    obj['_ID'] = id
    input_data = json.dumps(obj)

    redisClient.publish(f'chimu:{key}', input_data)

    while time_current < time_deadline:
        res = downloadMap.get(id)
        if res != None:
            return res

        time_current = time.time()

    return None


#############
# Downloads #
#############
def DownloadResponseHandler(rmsg):
    global downloadMap

    data = json.loads(rmsg['data'])

    downloadMap[data['_ID']] = data


async def RequestDownload(set_id: int, no_video: bool):
    return await Request(f'downloads', {
        'SetId': set_id,
        'NoVideo': no_video
    })
