import requests
import json
import re

sources = open("sources.txt").read().splitlines()

channels=[]
id=1

def detect_type(stream):

    if ".m3u8" in stream:
        return "HLS"

    if ".mpd" in stream:
        return "DASH"

    if ".mp4" in stream:
        return "MP4"

    if ".ts" in stream:
        return "TS"

    return "Live"


def is_alive(url):

    try:
        r=requests.head(url,timeout=5)
        return r.status_code<400
    except:
        return False


for src in sources:

    print("Loading:",src)

    r=requests.get(src)
    lines=r.text.splitlines()

    playlist_name=src.split("/")[-1].replace(".m3u","")

    name=""
    logo=""
    backup=""
    category=playlist_name

    for line in lines:

        if line.startswith("#EXTINF"):

            name=line.split(",")[-1]

            logo_match=re.search(r'tvg-logo="([^"]+)"',line)

            if logo_match:
                logo=logo_match.group(1)
            else:
                logo="https://upload.wikimedia.org/wikipedia/commons/7/75/Video_icon.svg"


        elif line.startswith("http"):

            stream=line.strip()

            if not is_alive(stream):
                continue

            channels.append({

                "id":str(id),
                "name":name,
                "logo":logo,
                "stream":stream,
                "category":category,
                "type":detect_type(stream)

            })

            id+=1


with open("channels.json","w") as f:

    json.dump(channels,f,indent=2)

print("Generated",len(channels),"channels")
