import random
import multiprocessing as mt
import yt_dlp
import os
import time
url = "https://youtube.com/playlist?list=PLE6dlt5SQB8r5oagkd_cwA6FlhGLGlxef&si=4uiABxKjgXr5p41G"
ytdl_format_options = {
    'format': 'bestaudio/best',
    'audio-quality': 0,
    'extract-audio': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0',
    'concurrent-fragments': 2,
    'output': "%(playlist_index)02d - %(title)s.%(ext)s",
}


ytdl_format_options_no_down = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0',
    'skip-download' : True,
    'extract_flat': True,
    'output': "%(playlist_index)02d - %(title)s.%(ext)s",
}



def Down(query):
    try:
        youtube = yt_dlp.YoutubeDL(ytdl_format_options)
        data = youtube.extract_info(query[0])
        filename = youtube.prepare_filename(data)
    except:
        return None
    return filename


if __name__ == '__main__':
    t1 = time.time()
    youtube = yt_dlp.YoutubeDL(ytdl_format_options_no_down)
    data = youtube.extract_info(url, download=False)
    if 'entries' in data:
        data = data['entries']
    queriesraw = []
    for i in data:
        print(i)
        queriesraw.append(f"www.youtube.com/watch?v={i['id']}")

    import itertools as it
    queries = it.batched(queriesraw, int(len(queriesraw) / len(queriesraw)))
    queries = list(map(list, queries))
    with mt.Pool() as p:
        print(p.map(func=Down,iterable=queries))
    
    t2 = time.time()

    print(t2 - t1)






