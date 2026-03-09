import requests
import json
import re

sources = open("sources.txt").read().splitlines()

channels=[]
id_counter=1

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


for src in sources:

    print("Loading:",src)

    try:
        r=requests.get(src,timeout=10)
        lines=r.text.splitlines()
    except:
        continue

    category=src.split("/")[-1].replace(".m3u","")

    name=""
    logo=""

    for line in lines:

        if line.startswith("#EXTINF"):

            name=line.split(",")[-1]

            logo_match=re.search(r'tvg-logo="([^"]+)"',line)

            if logo_match:
                logo=logo_match.group(1)
            else:
                logo="https://upload.wikimedia.org/wikipedia/commons/7/75/Video_icon.svg"

        elif line.startswith("http"):

            channels.append({

                "id":str(id_counter),
                "name":name,
                "logo":logo,
                "stream":line.strip(),
                "category":category,
                "type":detect_type(line)

            })

            id_counter+=1


with open("channels.json","w") as f:

    json.dump(channels,f,indent=2)

print("Generated",len(channels),"channels")
