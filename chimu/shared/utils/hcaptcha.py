import requests
import json

from datetime import timedelta
from os import environ

from chimu.shared.utils.redis import GetRedisClient


def VerifyHCaptchaAccessToken(accessToken: str) -> bool:
    redis = GetRedisClient()

    # If we already have that, lets just return True
    if redis.exists(f'chimu:hcaptcha:{accessToken}'):
        return True

    response = requests.post('https://hcaptcha.com/siteverify', data={
        'response': accessToken,
        'secret': environ.get('HCAPTCHA_SECRET'),
    })

    succeeded = json.loads(response.text)['success'] == True

    if succeeded:
        redis.setex(f'chimu:hcaptcha:{accessToken}', time=timedelta(
            hours=8), value='OwO, What\'s this super secret value')

    return succeeded
