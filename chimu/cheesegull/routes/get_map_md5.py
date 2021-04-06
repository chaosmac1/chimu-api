import datadog

from starlette.responses import JSONResponse
from starlette.requests import Request

from chimu.shared.utils.digit import isDigit
from chimu.shared.utils.mysql import GetDatabaseConnection


async def get_map_md5(request: Request):
    datadog.statsd.increment('chimu.api.v1.get_map',
                             tags=["version:1", "application:web"])

    map_md5 = request.path_params['map_md5']
    if len(map_md5) != 32:
        return JSONResponse(None)

    with GetDatabaseConnection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            'SELECT * FROM Beatmaps WHERE FileMD5 = ? LIMIT 1', (map_md5,))

        for bm in cursor:
            return JSONResponse(
                {
                    'BeatmapID': bm[0],
                    'ParentSetID': bm[1],
                    'DiffName': bm[2],
                    'FileMD5': bm[3],
                    'Mode': bm[4],
                    'BPM': bm[5],
                    'AR': bm[6],
                    'OD': bm[7],
                    'CS': bm[8],
                    'HP': bm[9],
                    'TotalLength': bm[10],
                    'HitLength': bm[11],
                    'Playcount': bm[12],
                    'Passcount': bm[13],
                    'MaxCombo': bm[14],
                    'DifficultyRating': bm[15],
                }
            )

    return JSONResponse(None, 404)
