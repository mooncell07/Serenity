from typing import Union

from hata import Embed
from aiohttp import ClientSession
from rfc3986.builder import URIBuilder


__all__ = ("TraceMoe",)


class SetTraceMoe:
    """
    Wtf is this
    """

    def __init__(self, content) -> None:
        cntnt = {}
        for i in content:
            cntnt[i] = (
                str(content[i]) if not isinstance(content[i], dict) else content[i]
            )
        self.__dict__.update(cntnt)


def convert(time: Union[float, int]) -> str:
    """
    converts time in seconds to human friendly format.
    """
    h = (time // 3600) % 24
    m = (time // 60) % 60
    s = time % 60
    return "%d:%02d:%02d" % (h, m, s)


class TraceMoe:
    """
    A class representing a TraceMoe. A minimal unfinished wrapper around trace.moe
    """

    __slots__ = ("BASE", "img", "color")

    def __init__(self, img) -> None:
        self.BASE: str = "api.trace.moe"
        self.img: str = img
        self.color: hex = 0x0000FF

    async def search(self, *, embedify=True) -> Union[Embed, dict]:
        """
        Makes an api call.
        """
        uri = URIBuilder(scheme="https", host=self.BASE, path="/search").add_query_from(
            {"anilistInfo": "", "url": self.img}
        )
        async with ClientSession() as session:
            async with session.get(uri.geturl()) as ret:
                con = await ret.json()
                return self._embedify(con) if embedify else con

    def _embedify(self, content: dict) -> Embed:  # Will paginate later...
        """
        Embedifies the response.
        """
        try:
            res = content["result"]
        except KeyError:
            return Embed(
                title="Error", description=content.get("error"), color=self.color
            )

        res = SetTraceMoe(res[0])
        anilist = res.anilist

        emb = Embed(
            title=str(anilist["title"].get("english")), color=self.color, url=res.video
        )

        emb.add_image(res.image)

        tm = list(map(lambda x: convert(float(x)), [res.__dict__["from"], res.to]))

        emb.add_field(
            name="Duration - ", value=f"from {tm[0]} to {tm[1]}.", inline=True
        )
        emb.add_field(
            name="Similarity - ", value=int(float(res.similarity) * 100), inline=True
        )
        emb.add_field(name="Episode - ", value=res.episode, inline=True)

        emb.add_field(name="NSFW? - ", value=anilist.get("isAdult"), inline=True)
        emb.add_field(name="ID - ", value=anilist.get("id"), inline=True)
        emb.add_field(name="MAL ID - ", value=anilist.get("idMal"), inline=True)

        return emb
