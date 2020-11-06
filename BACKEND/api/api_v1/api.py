from fastapi import APIRouter

from api.api_v1.endpoints import user,country,channel,shop,sim,login,url,tag

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(sim.router, prefix="/sim", tags=["sim"])
api_router.include_router(url.router, prefix="/url", tags=["url"])
api_router.include_router(tag.router, prefix="/tag", tags=["tag"])
api_router.include_router(user.router, prefix="/users", tags=["user"])
api_router.include_router(country.router, prefix="/country", tags=["country"])
api_router.include_router(channel.router, prefix="/channel", tags=["channel"])
api_router.include_router(shop.router, prefix="/shop", tags=["shop"])


