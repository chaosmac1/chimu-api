import meilisearch

from os import environ

meiliClient: meilisearch.Client
meiliIndex: meilisearch.index.Index


def InitializeMeili():
    print('MeiliSearch: Initializing...')

    client = meilisearch.Client(environ.get(
        'MEILI_HOST'), environ.get('MEILI_KEY'))

    try:
        print('MeiliSearch: Test for connection')
        client.health()
    except meilisearch.errors.MeiliSearchCommunicationError as e:
        print(f'Meilisearch: Failed to connect: {e}')
        print('Exiting...')
        exit(1)

    index = client.index(environ.get('MEILI_INDEX'))

    global meiliClient
    global meiliIndex

    meiliClient = client
    meiliIndex = index

    print('MeiliSearch: Success')


def SearchForBeatmap(query: str, amount: int, offset: int,
                     rankedStatus: int = -1, mode: int = -1,
                     min_ar: float = -1, max_ar: float = -1, min_od: float = -1, max_od: float = -1,
                     min_cs: float = -1, max_cs: float = -1, min_hp: float = -1, max_hp: float = -1,
                     min_diff: float = -1, max_diff: float = -1,
                     min_bpm: float = -1, max_bpm: float = -1,
                     min_length: int = -1, max_length: int = -1,
                     genre: int = -1, language: int = -1):

    filterQuery = ""
    if mode != -1:
        filterQuery += f"mode = {mode} "

    if rankedStatus != -5:
        if filterQuery != "":
            filterQuery += " AND "

        if rankedStatus == 1 or rankedStatus == 2:
            filterQuery += "(rankedStatus = 1 OR rankedStatus = 2) "
        else:
            filterQuery += f"rankedStatus = {rankedStatus} "

    # AR
    if filterQuery != "" and min_ar != -1:
        filterQuery += f"AND ar >= {min_ar} "
    elif filterQuery == "" and min_ar != -1:
        filterQuery += f"ar >= {min_ar} "

    if filterQuery != "" and max_ar != -1:
        filterQuery += f"AND ar <= {max_ar} "
    elif filterQuery == "" and max_ar != -1:
        filterQuery += f"ar <= {max_ar} "

    # OD
    if filterQuery != "" and min_od != -1:
        filterQuery += f"AND od >= {min_od} "
    elif filterQuery == "" and min_od != -1:
        filterQuery += f"od >= {min_od} "

    if filterQuery != "" and max_od != -1:
        filterQuery += f"AND od <= {max_od} "
    elif filterQuery == "" and max_od != -1:
        filterQuery += f"od <= {max_od} "

    # CS
    if filterQuery != "" and min_cs != -1:
        filterQuery += f"AND cs >= {min_cs} "
    elif filterQuery == "" and min_cs != -1:
        filterQuery += f"cs >= {min_cs} "

    if filterQuery != "" and max_cs != -1:
        filterQuery += f"AND cs <= {max_cs} "
    elif filterQuery == "" and max_cs != -1:
        filterQuery += f"cs <= {max_cs} "

    # HP
    if filterQuery != "" and min_hp != -1:
        filterQuery += f"AND hp >= {min_hp} "
    elif filterQuery == "" and min_hp != -1:
        filterQuery += f"hp >= {min_hp} "

    if filterQuery != "" and max_hp != -1:
        filterQuery += f"AND hp <= {max_hp} "
    elif filterQuery == "" and max_hp != -1:
        filterQuery += f"hp <= {max_hp} "

    # Diff
    if filterQuery != "" and min_diff != -1:
        filterQuery += f"AND difficultyRating >= {min_diff} "
    elif filterQuery == "" and min_diff != -1:
        filterQuery += f"difficultyRating >= {min_diff} "

    if filterQuery != "" and max_diff != -1:
        filterQuery += f"AND difficultyRating <= {max_diff} "
    elif filterQuery == "" and max_diff != -1:
        filterQuery += f"difficultyRating <= {max_diff} "

    # Bpm
    if filterQuery != "" and min_bpm != -1:
        filterQuery += f"AND bpm >= {min_bpm} "
    elif filterQuery == "" and min_bpm != -1:
        filterQuery += f"bpm >= {min_bpm} "

    if filterQuery != "" and max_bpm != -1:
        filterQuery += f"AND bpm <= {max_bpm} "
    elif filterQuery == "" and max_bpm != -1:
        filterQuery += f"bpm <= {max_bpm} "

    # Length
    if filterQuery != "" and min_length != -1:
        filterQuery += f"AND totalLength >= {min_length} "
    elif filterQuery == "" and min_length != -1:
        filterQuery += f"totalLength >= {min_length} "

    if filterQuery != "" and max_length != -1:
        filterQuery += f"AND totalLength <= {max_length} "
    elif filterQuery == "" and max_length != -1:
        filterQuery += f"totalLength <= {max_length} "

    if filterQuery != "" and genre != -1:
        filterQuery += f"AND genre = {genre} "
    elif filterQuery == "" and genre != -1:
        filterQuery += f"genre = {genre} "

    if filterQuery != "" and language != -1:
        filterQuery += f"AND language = {language} "
    elif filterQuery == "" and language != -1:
        filterQuery += f"language = {language} "

    if filterQuery == "":
        filterQuery = None

    result = meiliIndex.search(query,
                               {
                                   'attributesToHighlight': ["title", "artist", "tags", "creator", "diffName"],
                                   'limit': amount,
                                   'offset': offset,
                                   'filters': filterQuery,
                                   'matches': True
                               })

    return result['hits']
