from chimu.shared.utils.digit import isDigit
from chimu.shared.utils.redis import RequestDownload
from chimu.shared.utils.hcaptcha import VerifyHCaptchaAccessToken
from chimu.v1.error_codes import *
from starlette.responses import JSONResponse, RedirectResponse
from starlette.requests import Request


async def download_set(request: Request):
    set_id = request.path_params.get('set_id')
    #key = request.query_params.get('k')
    #state = request.query_params.get('s')
    no_video = request.query_params.get('n')

    #if key == None:
    #    return Error(403, ERR_CODE_KEY_REQUIRED, 'Error: key is not set!')
    #elif state == None:
    #    return Error(403, ERR_CODE_STATE_NOT_SET, 'Error: state is not set!')
    if not isDigit(set_id) or set_id == None:
        return Error(401, ERR_CODE_INT_ERROR, f'Error: {set_id} is not an int!')
    
    if no_video == None:
        no_video = 0

    #if state == 'hcaptcha':
    #    if not VerifyHCaptchaAccessToken(key):
    #        return Error(403, ERR_CODE_KEY_REQUIRED, 'Error: Invalid Key!')

    beatmap = await RequestDownload(set_id, no_video)
    if beatmap == None:
        return Error(404, ERR_CODE_BEATMAP_NOT_FOUND, f'Error: Beatmap not found!')

    if beatmap['IpfsHash'] == None or beatmap['IpfsHash'] == '':
        return Error(404, ERR_CODE_BEATMAP_UNAVAILABLE, f'Error: Beatmap unavailable!')

    return RedirectResponse(f'https://ipfs.chimu.moe/ipfs/{beatmap["IpfsHash"]}?filename={beatmap["File"]}')

    #return Error(404, ERR_CODE_BEATMAP_NOT_FOUND, f'Error: Beatmap not found!')
