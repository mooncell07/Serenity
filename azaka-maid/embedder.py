import textwrap

from azaka.objects import VN
from discord import Embed

__all__ = ("vn_to_embed",)


def vn_to_embed(vn: VN) -> Embed:
    desc = (
        textwrap.shorten(text=vn.description, width=300)
        if vn.description
        else "Not available."
    )
    embed = Embed(
        title=vn.title,
        description=desc,
        color=0xFF0000,
        url=f"https://www.wikidata.org/wiki/{vn.links.wikidata}"
        if vn.links.wikidata
        else None,
    )
    embed.set_thumbnail(url=vn.image)
    embed.add_field(name="id: ", value=vn.id, inline=True)
    embed.add_field(name="platforms: ", value=", ".join(vn.platforms), inline=True)
    embed.add_field(name="languages: ", value=", ".join(vn.languages), inline=True)
    embed.add_field(name="length: ", value=vn.length or "Not available.", inline=True)
    embed.add_field(
        name="original language: ", value=", ".join(vn.orig_lang), inline=True
    )
    embed.add_field(name="release date:", value=vn.released, inline=True)
    return embed
