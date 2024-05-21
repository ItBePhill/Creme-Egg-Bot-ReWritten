from googleapiclient.discovery import build
import isodate
import pprint
pp = pprint.PrettyPrinter()
from googleapiclient.discovery import build
song = {
    "Title": None,
    "Channel": None,
    "Duration": None,
    "Thumbnail": None,
    "URL": None
}
api_key = open("key.txt", "r").readlines()[3]
youtube = build('youtube', 'v3', developerKey=api_key)

request = youtube.search().list(
    q="The Summoning Sleep Token",
    part="id",
    type="video"
)
response = request.execute()
print(response["items"][0]["id"]["videoId"])
request2 = youtube.videos().list(
    id=response["items"][0]["id"]["videoId"],
    part="snippet,contentDetails"
)
response2 = request2.execute()
song["Title"] = response2['snippet']['title']
song["Channel"] = response2['snippet']['channelTitle']
song["Thumbnail"] = response2['snippet']['thumbnails']['default']['url']
song["Duration"] = response2['contentDetails']['duration']
song["URL"] = f"https://www.youtube.com/watch?v={response2['id']}"

pp.pprint(song)