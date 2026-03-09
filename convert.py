import requests
import json

sources = open("sources.txt").read().splitlines()

channels = []
id = 1

def detect(stream):
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

    r = requests.get(src)
    lines = r.text.splitlines()

    name = ""
    logo = ""

    for line in lines:

        if line.startswith("#EXTINF"):
            name = line.split(",")[-1]

            if 'tvg-logo="' in line:
                logo = line.split('tvg-logo="')[1].split('"')[0]
            else:
                logo = "https://upload.wikimedia.org/wikipedia/commons/7/75/Video_icon.svg"

        elif line.startswith("http"):

            channels.append({
                "id": str(id),
                "name": name,
                "logo": logo,
                "stream": line,
                "category": detect(line)
            })

            id += 1


with open("channels.json","w") as f:
    json.dump(channels,f,indent=2)

print("JSON updated")
