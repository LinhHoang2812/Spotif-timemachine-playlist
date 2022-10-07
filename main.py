from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

Client_ID= os.environ["CLIENT_ID"]
Client_Secret= os.environ["CLIENT_SECRET"]
Direct_Uri = os.environ["DIRECT_URI"]


###Scraping songs from Billboard###
date =input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

url = f"https://www.billboard.com/charts/hot-100/{date}/"
response = requests.get(url= url)
website = response.text

soup = BeautifulSoup(website, "html.parser")
first_song = soup.find(name="h3",id="title-of-a-story",class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet").getText()[14:].split("\t")[0]
song_titles = soup.find_all(name="h3",id="title-of-a-story",class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")
songs_list= [song.getText()[14:].split("\t")[0] for song in song_titles]
songs_list.insert(0,first_song)

print(songs_list)

with open("song_playlist.txt","w") as file:
    for song in songs_list:
        file.write(f"{song}\n")

###Authorization on Spotify####

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=Client_ID,
                                               client_secret=Client_Secret,
                                               redirect_uri=Direct_Uri,
                                               scope= "playlist-modify-private",
                                               show_dialog= True,
                                               cache_path="token.txt"))

user_id =sp.current_user()["id"]

###Search for songs on Spotify####

uri_song =[]
for song in songs_list:
    try:
        response = sp.search(q=f"{song}", type="track",limit=1)
        uri_song.append(response["tracks"]["items"][0]["uri"])
    except IndexError:
        print(f"Song {song} not found on Spotify")




print(uri_song)

###Add songs to playlist###

my_playlist = sp.user_playlist_create(user=user_id,
                                      name=f"{date} Billboard top 100",
                                      public=False)
my_playlist_id=my_playlist["id"]


sp.user_playlist_add_tracks(user=user_id,
                                  playlist_id=my_playlist_id,
                                  tracks=uri_song)


