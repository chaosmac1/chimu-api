from starlette.responses import JSONResponse

ERR_CODE_OK = 0

# Download Errors
ERR_CODE_INT_ERROR = 101
ERR_CODE_KEY_REQUIRED = 102
ERR_CODE_STATE_NOT_SET = 103
ERR_CODE_BEATMAP_NOT_FOUND = 104
ERR_CODE_BEATMAP_UNAVAILABLE = 105
ERR_CODE_NO_SEARCH_RESULTS = 106

def Success(data = [ ]):
    return Error(200, ERR_CODE_OK, '', data)

def Error(status_code, error_code, msg, data = [ ]):
    return JSONResponse(
    { 
        'code': error_code,
        'message': msg,
        'data': data
    }, status_code)
