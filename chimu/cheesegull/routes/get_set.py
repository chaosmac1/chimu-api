import datadog

from starlette.responses import JSONResponse
from starlette.requests import Request

from chimu.shared.utils.digit import isDigit
from chimu.shared.utils.mysql import GetDatabaseConnection


async def get_set(request: Request):
    datadog.statsd.increment('chimu.api.v1.get_set',
                             tags=["version:1", "application:web"])

    set_id = request.path_params['set_id']
    if not isDigit(set_id):
        return JSONResponse(None)
    set_id = int(set_id)

    with GetDatabaseConnection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            'SELECT * FROM BeatmapSet WHERE SetId = ? LIMIT 1', (set_id,))

        set = cursor.fetchall()

        beatmapSet = {}

        if cursor.rowcount > 0:
            set = set[0]

            # Fetch Children
            cursor.execute(
                'SELECT * FROM Beatmaps WHERE ParentSetId = ?', (set_id,))

            children = []
            for bm in cursor:
                children.append({
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
                })

                beatmapSet = {
                    'SetID': set[0],
                    'ChildrenBeatmaps': children,
                    'RankedStatus': set[1],
                    'ApprovedDate': set[2].isoformat() + "Z" if set[2] else '',
                    'LastUpdate': set[3].isoformat() + "Z" if set[3] else '',
                    'LastChecked': set[4].isoformat() + "Z" if set[4] else '',
                    'Artist': set[5],
                    'Title': set[6],
                    'Creator': set[7],
                    'Source': set[8],
                    'Tags': set[9],
                    'HasVideo': set[10] == 1,
                    'Genre': set[11],
                    'Language': set[12],
                    'Favourites': set[13],
                }

                return JSONResponse(beatmapSet)

    return JSONResponse(None)
