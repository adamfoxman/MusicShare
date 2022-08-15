import nextcord

stream_platforms = {
    'amazonMusic': 'Amazon Music',
    'appleMusic': 'Apple Music',
    'deezer': 'Deezer',
    'soundcloud': 'SoundCloud',
    'spotify': 'Spotify',
    'tidal': 'Tidal',
    'youtubeMusic': 'YouTube Music',
}

buy_platforms = {
    'itunes': 'iTunes',
    'amazonStore': 'Amazon'
}


def _shorten_summary(summary: str) -> str:
    first_paragraph = summary.split('\n')[0]
    #  find markdown link in summary
    link_start = summary.find('<a href="')
    link_end = summary.find('">')
    link = summary[link_start+9:link_end]
    #  find title of link
    title_start = summary.find('">')
    title_end = summary.find('</a>')
    title = summary[title_start+2:title_end]
    #  return first paragraph and link and title
    return first_paragraph + f' [{title}]({link})'


def _get_link_strings(links: dict) -> (str, str, str):
    s = ''
    b = ''
    w = ''
    for platform, link in links.items():
        if platform in stream_platforms:
            if s != '':
                s += ' | '
            s += f'[{stream_platforms[platform]}]({link})'
        elif platform in buy_platforms:
            if b != '':
                b += ' | '
            b += f'[{buy_platforms[platform]}]({link})'
        else:
            if w != '':
                w += ' | '
            w += f'[{platform.capitalize()}]({link})'
    return s, b, w


def generate_lite_embed(artist: str, title: str, cover_art: str, url: str):
    embed = nextcord.Embed(
        title=f"{artist} - {title}",
        description=f"[Click here]({url}) to listen",
        color=0x00FF00
    )
    embed.set_thumbnail(url=cover_art)
    return embed


def generate_embed(artist: str, title: str, cover_art: str, song_info: dict, links: dict):
    embed = nextcord.Embed(
        title=f"{artist} - {title}",
        description=f'From {song_info["album"] if "album" in song_info else "Unknown"}',
        color=0x00FF00
    )
    embed.set_thumbnail(url=cover_art)
    if song_info['summary'] != '':
        embed.add_field(name="Summary", value=_shorten_summary(song_info['summary']), inline=False)
    if 'tags' in song_info and song_info['tags'] is not []:
        embed.set_footer(text=f"Tags: {', '.join(song_info['tags'])}")

    stream, buy, watch = _get_link_strings(links)
    if stream != '':
        embed.add_field(name="Stream", value=stream, inline=False)
    if buy != '':
        embed.add_field(name="Buy", value=buy, inline=False)
    if watch != '':
        embed.add_field(name="Watch", value=watch, inline=False)

    return embed