import datadog

from chimu.shared.utils.mysql import GetDatabaseConnection
from chimu.shared.utils.meili import SearchForBeatmap

from chimu.v1.error_codes import ERR_CODE_INT_ERROR, ERR_CODE_NO_SEARCH_RESULTS, Error, Success

from starlette.requests import Request
from starlette.responses import JSONResponse


def get_query_value(request: Request, name: str, default, is_int: bool = False, is_float: bool = False):
    v = default
    q = request.query_params.get(name)

    if q == None:
        return v

    if is_int:
        if not q.isdigit():
            return None
        else:
            v = int(q)
    elif is_float:
        if not q.isdigit():
            return None
        else:
            v = float(q)
    else:
        v = q

    return v


async def search(request: Request):
    datadog.statsd.increment('chimu.api.v1.search',
                             tags=["version:1", "application:web"])

    query = get_query_value(request, "query", "")
    amount = get_query_value(request, "amount", 100, True)
    if amount == None:
        return Error(401, ERR_CODE_INT_ERROR, f'Error: amount is not an int!')

    offset = get_query_value(request, "offset", 0, True)
    if offset == None:
        return Error(401, ERR_CODE_INT_ERROR, f'Error: offset is not an int!')

    rankedStatus = get_query_value(request, "status", -1, True)
    if rankedStatus == None:
        return Error(401, ERR_CODE_INT_ERROR, f'Error: rankedStatus is not an int!')

    playMode = get_query_value(request, "mode", -1, True)
    if playMode == None:
        return Error(401, ERR_CODE_INT_ERROR, f'Error: playMode is not an int!')

    if amount > 100:
        amount = 100

    beatmaps = SearchForBeatmap(query, amount, offset, rankedStatus, playMode)

    if len(beatmaps) <= 0:
        return Error(404, ERR_CODE_NO_SEARCH_RESULTS, 'Error: No search results!')

    with GetDatabaseConnection() as conn:
        cursor = conn.cursor()

        beatmapSetIds = ""
        for bm in beatmaps:
            beatmapSetIds += f"{bm['id']},"
        beatmapSetIds = beatmapSetIds.strip(',')

        cursor.execute(
            f"SELECT * FROM BeatmapSet WHERE SetId IN ({beatmapSetIds})")

        beatmapSetRaw = {}
        for set in cursor:
            beatmapSetRaw[set[0]] = {
                'SetID': set[0],
                'ChildrenBeatmaps': [],
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

        cursor.execute(
            f"SELECT * FROM Beatmaps WHERE ParentSetId IN ({beatmapSetIds})")

        for bm in cursor:
            set = beatmapSetRaw[bm[1]]

            set['ChildrenBeatmaps'].append(
                {
                    'BeatmapID': bm[0],
                    'ParentSetID': bm[1],
                    'DiffName': bm[2],
                    'FileMD5': bm[3],
                    'Mode': bm[4],
                    'BPM': round(bm[5]),
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

        beatmapSets = []
        for set in beatmapSetRaw.values():
            beatmapSets.append(set)

    return JSONResponse(beatmapSets)
