from chimu.shared.utils.digit import isDigit
import datadog

from chimu.v1.error_codes import ERR_CODE_BEATMAP_NOT_FOUND, ERR_CODE_INT_ERROR, Error, Success
from chimu.shared.utils.mysql import GetDatabaseConnection
from starlette.requests import Request


async def get_set(request: Request):
    datadog.statsd.increment('chimu.api.v1.get_set',
                             tags=["version:1", "application:web"])

    set_id = request.path_params['set_id']
    if not isDigit(set_id):
        return Error(401, ERR_CODE_INT_ERROR, f'Error: set_id is not an int!')
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
                    'BeatmapId': bm[0],
                    'ParentSetId': bm[1],
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
                    'OsuFile': bm[16],
                    'DownloadPath': f'/d/{bm[1]}'
                })

                beatmapSet = {
                    'SetId': set[0],
                    'ChildrenBeatmaps': children,
                    'RankedStatus': set[1],
                    'ApprovedDate': set[2].isoformat() if set[2] else '',
                    'LastUpdate': set[3].isoformat() if set[3] else '',
                    'LastChecked': set[4].isoformat() if set[4] else '',
                    'Artist': set[5],
                    'Title': set[6],
                    'Creator': set[7],
                    'Source': set[8],
                    'Tags': set[9],
                    'HasVideo': set[10] == 1,
                    'Genre': set[11],
                    'Language': set[12],
                    'Favourites': set[13],
                    'Disabled': set[14] == 1,
                }

                return Success(beatmapSet)

    return Error(404, ERR_CODE_BEATMAP_NOT_FOUND, 'Error: Beatmap set not found!')
