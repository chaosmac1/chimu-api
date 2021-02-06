from chimu.v1.routes.search import search
from chimu.shared.utils.meili import InitializeMeili
from chimu.shared.utils.mysql import InitializeMySQL
from chimu.shared.utils.datadog import InitializeDatadog
from chimu.v1.routes.get_set import get_set
from chimu.v1.routes.get_map import get_map
from chimu.shared.utils.redis import InitializeRedis
from chimu.v1.routes.download import download_set
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
    Route('/api/v1/download/{set_id}', download_set),
    Route('/api/v1/map/{map_id}', get_map),
    Route('/api/v1/set/{set_id}', get_set),
    Route('/api/v1/search', search),
])
