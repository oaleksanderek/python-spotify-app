from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_artist(token, arist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={arist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name was found...")
        return None
    return json_result[0]

def get_artist_top_songs(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


token = get_token()
result = search_artist(token, "Harry Styles")
artist_id = result["id"]
top_songs = get_artist_top_songs(token, artist_id)

# for i, song in enumerate(top_songs):
#     print(f"{i + 1}. {song['name']}")

top_songs_dict = {
    "name": [],
    "popularity": []
}
names = []
popularity = []
for song in top_songs:
    names.append(song["name"])
    popularity.append(song["popularity"])

top_songs_dict["name"] = names
top_songs_dict["popularity"] = popularity


for i, name in enumerate(top_songs_dict["name"]):
    print(f"{i + 1}. {name}, popularity = {top_songs_dict['popularity'][i]}")