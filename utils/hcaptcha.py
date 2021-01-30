import requests
import json

from os import environ


def VerifyHCaptchaAccessToken(accessToken: str) -> bool:
    response = requests.post('https://hcaptcha.com/siteverify', data={
        'response': accessToken,
        'secret': environ.get('HCAPTCHA_SECRET'),
    })

    return json.loads(response.text)['success'] == True
