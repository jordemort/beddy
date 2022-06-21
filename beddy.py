import os

import httpx
from blacksheep import Application, Content, Request, Response

IFRAMELY_API_KEY = os.environ["IFRAMELY_API_KEY"]
IFRAMELY_ENDPOINT = "https://iframe.ly/api/oembed"

app = Application()


@app.router.get("/oembed")
async def oembed(o: Request):
    params = o.query
    params["api_key"] = [IFRAMELY_API_KEY]

    async with httpx.AsyncClient() as client:
        r = await client.get(IFRAMELY_ENDPOINT, params=params)  # type: ignore
        return Response(
            r.status_code,
            content=Content(r.headers["content-type"].encode("utf-8"), r.content),
        )
