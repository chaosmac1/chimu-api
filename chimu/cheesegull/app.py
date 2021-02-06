from chimu.shared.utils.meili import InitializeMeili
from chimu.shared.utils.mysql import InitializeMySQL
from chimu.shared.utils.datadog import InitializeDatadog
from chimu.shared.utils.redis import InitializeRedis

from chimu.cheesegull.routes.get_map import get_map
from chimu.cheesegull.routes.get_set import get_set
from chimu.cheesegull.routes.search import search

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from dotenv import load_dotenv

load_dotenv()
InitializeRedis()
InitializeMySQL()
InitializeMeili()
InitializeDatadog()


async def homepage(request):
    return JSONResponse({'hello': 'world'})

app = Starlette(routes=[
    Route('/', homepage),
    Route('/api/cheesegull/b/{map_id}', get_map),
    Route('/api/cheesegull/b/{set_id}', get_set),
    Route('/api/cheesegull/search', search),
])
