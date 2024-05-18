from googleapiclient.discovery import build
import isodate
import os
def run(url):
    url =  url.split("&t")[0]
    print(url)
    api_key = None
    with open(f"{os.getcwd()}\key.txt", "r") as f:
        api_key = f.readlines()[3]
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(q=url,part='snippet,contentDetails',type='video')
    response = request.execute()
    return response['items']



url = "https://www.youtube.com/watch?v=sWtEYPva4A0&t=2086s"
url1 = "Relaxing Zelda Music with Campfire Ambience"

data = run(url)

data1 = run(url1)

import pprint


pp = pprint.PrettyPrinter()

title = data[0]["snippet"]["title"]
author = data[0]["snippet"]["channelTitle"]
id = data[0]["id"]["videoId"]
pp.pprint(data[0])
pp.pprint("-")
pp.pprint("-")
pp.pprint("-")
pp.pprint(data1[0])