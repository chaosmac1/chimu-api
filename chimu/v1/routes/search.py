import datadog

from chimu.shared.utils.mysql import GetDatabaseConnection
from chimu.shared.utils.meili import SearchForBeatmap
from chimu.v1.error_codes import ERR_CODE_INT_ERROR, ERR_CODE_NO_SEARCH_RESULTS, Error, Success
from starlette.requests import Request


def get_query_value(request: Request, name: str, default, is_int: bool = False, is_float: bool = False):
    v = default
    q = request.query_params.get(name)

    if q == None:
        return v

    if is_int:
        if not q.lstrip('-').isdigit():
            return None
        else:
            v = int(q)
    elif is_float:
        if not q.lstrip('-').isdigit():
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

    rankedStatus = get_query_value(request, "status", -5, True)
    if rankedStatus == None:
        return Error(401, ERR_CODE_INT_ERROR, f'Error: status is not an int!')

    playMode = get_query_value(request, "mode", -1, True)
    if playMode == None:
        return Error(401, ERR_CODE_INT_ERROR, f'Error: mode is not an int!')

    min_ar = get_query_value(request, "min_ar", -1, False, True)
    if rankedStatus == None:
        return Error(401, ERR_CODE_INT_ERROR, f'Error: min_ar is not an int!')

    max_ar = get_query_value(request, "max_ar", -1, False, True)
    if rankedStatus == None:
        return Error(401, ERR_CODE_INT_ERROR, f'Error: max_ar is not an int!')

    min_od = get_query_value(request, "min_od", -1, False, True)
    if rankedStatus == None:
        return Error(401, ERR_CODE_INT_ERROR, f'Error: min_od is not an int!')

    max_od = get_query_value(request, "max_od", -1, False, True)
    if rankedStatus == None:
        return Error(401, ERR_CODE_INT_ERROR, f'Error: max_od is not an int!')

    min_cs = get_query_value(request, "min_cs", -1, False, True)
    if rankedStatus == None:
        return Error(401, ERR_CODE_INT_ERROR, f'Error: min_cs is not an int!')

    max_cs = get_query_value(request, "max_cs", -1, False, True)
    if rankedStatus == None:
        return Error(401, ERR_CODE_INT_ERROR, f'Error: max_cs is not an int!')

    min_hp = get_query_value(request, "min_hp", -1, False, True)
    if rankedStatus == None:
        return Error(401, ERR_CODE_INT_ERROR, f'Error: min_hp is not an int!')

    max_hp = get_query_value(request, "max_hp", -1, False, True)
    if rankedStatus == None:
        return Error(401, ERR_CODE_INT_ERROR, f'Error: max_hp is not an int!')

    min_diff = get_query_value(request, "min_diff", -1, False, True)
    if rankedStatus == None:
        return Error(401, ERR_CODE_INT_ERROR, f'Error: min_diff is not an int!')

    max_diff = get_query_value(request, "max_diff", -1, False, True)
    if rankedStatus == None:
        return Error(401, ERR_CODE_INT_ERROR, f'Error: max_diff is not an int!')

    min_bpm = get_query_value(request, "min_bpm", -1, False, True)
    if rankedStatus == None:
        return Error(401, ERR_CODE_INT_ERROR, f'Error: min_bpm is not an int!')

    max_bpm = get_query_value(request, "max_bpm", -1, False, True)
    if rankedStatus == None:
        return Error(401, ERR_CODE_INT_ERROR, f'Error: max_bpm is not an int!')

    min_length = get_query_value(request, "min_length", -1, False, True)
    if rankedStatus == None:
        return Error(401, ERR_CODE_INT_ERROR, f'Error: min_length is not an int!')

    max_length = get_query_value(request, "max_length", -1, False, True)
    if rankedStatus == None:
        return Error(401, ERR_CODE_INT_ERROR, f'Error: max_length is not an int!')

    genre = get_query_value(request, "genre", -1, False)
    if rankedStatus == None:
        return Error(401, ERR_CODE_INT_ERROR, f'Error: genre is not an int!')

    language = get_query_value(request, "language", -1, False)
    if rankedStatus == None:
        return Error(401, ERR_CODE_INT_ERROR, f'Error: language is not an int!')

    if amount > 100:
        amount = 100

    beatmaps = SearchForBeatmap(query, amount, offset, rankedStatus, playMode,
                                min_ar, max_ar, min_od, max_od, min_cs, max_cs, min_hp, max_hp,
                                min_diff, max_diff, min_bpm, max_bpm, min_length, max_length,
                                genre, language)

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
                'SetId': set[0],
                'ChildrenBeatmaps': [],
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

        cursor.execute(
            f"SELECT * FROM Beatmaps WHERE ParentSetId IN ({beatmapSetIds})")

        for bm in cursor:
            set = beatmapSetRaw[bm[1]]

            set['ChildrenBeatmaps'].append(
                {
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
                }
            )

        beatmapSets = []
        for set in beatmapSetRaw.values():
            beatmapSets.append(set)

    return Success(beatmapSets)
