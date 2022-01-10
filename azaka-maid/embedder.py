import textwrap
from azaka.objects import VN
from hata import Embed

__all__ = ("vn_to_embed",)


def vn_to_embed(vn: VN) -> Embed:
    desc = textwrap.shorten(text=vn.description, width=300) if vn.description else "Not available."
    embed = Embed(
        title=vn.title,
        description=desc,
        color=0xFF0000,
        url=f"https://www.wikidata.org/wiki/{vn.links.wikidata}"
        if vn.links.wikidata
        else None,
    )
    embed.add_thumbnail(url=vn.image)
    embed.add_field("id: ", vn.id, inline=True)
    embed.add_field("platforms: ", ", ".join(vn.platforms), inline=True)
    embed.add_field("languages: ", ", ".join(vn.languages), inline=True)
    embed.add_field("length: ", vn.length or "Not available.", inline=True)
    embed.add_field("original language: ", ", ".join(vn.orig_lang), inline=True)
    embed.add_field("release date:", vn.released, inline=True)
    return embed
