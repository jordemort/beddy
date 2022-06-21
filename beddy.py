import json
import os

import httpx
from blacksheep import Application, JSONContent, Request, Response

IFRAMELY_API_KEY = os.environ["IFRAMELY_API_KEY"]
IFRAMELY_ENDPOINT = "https://iframe.ly/api/oembed"

app = Application()


@app.route("/oembed")
async def oembed(o: Request):
    params = o.query
    params["api_key"] = [IFRAMELY_API_KEY]

    async with httpx.AsyncClient() as client:
        req = await client.get(IFRAMELY_ENDPOINT, params=params)  # type: ignore
        res = Response(req.status_code, content=JSONContent(json.loads(req.content)))
        # for k, v in req.headers.items():
        #    if k.strip().lower() in ("content-length", "content-type"):
        #        continue
        #    res.add_header(k.encode("utf-8"), v.encode("utf-8"))
        return res
