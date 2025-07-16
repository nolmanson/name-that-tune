

import spotipy
import spotipy.util as util
import json
import time
from jinja2 import Template
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

## Edit the configurations
SPOTIPY_CLIENT_ID =''
SPOTIPY_CLIENT_SECRET =''
SPOTIPY_REDIRECT_URI ='http://localhost/'
username = ''
scope = ''

seconds_between_songs = 60

# if len(sys.argv) > 1:
#     username = sys.argv[1]
# else:
#     print("Usage: %s username" % (sys.argv[0],))
#     sys.exit()

def main():
    with open("templates/html_template.html") as f_2:
        html_file = f_2.read()

    html = Template(html_file)
    auth_manager = 'Test'

    if auth_manager:
        sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope))


        #Starting the playlist if it isn't playing already
        try:
            results = sp.start_playback()
        except:
            pass

        previous_song = ""
        previous_song_url = ""
        current_song_url = ""
        starting_round = 0 ## the script will sometimes time out so this allows you to start in a later round

        #This is the script working
        for i in range(59):
            try:
                sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope))
                round = starting_round+i+1
                print("\n===================================\nBeginning of round: ", round)
                next_song = sp.next_track()
                test = sp.seek_track(position_ms=60000)


                time.sleep(1)
                test2 = sp.currently_playing()
                data1 = json.dumps(test2)
                data = json.loads(data1)
                song_duration = data["item"]["duration_ms"]
                current_song_url = data["item"]["album"]["images"][0]["url"]
                progress = round * 10
                progress = progress

                export = html.render(progress = progress,
                                     current_song_url = current_song_url,
                                     previous_song = previous_song,
                                     previous_song_url = previous_song_url,
                                     current_round = round
                                     )

                # write out html code that is ready to be used
                Html_code = open("static/image.html", "w")
                Html_code.write(export)
                Html_code.close()

                time.sleep(seconds_between_songs-1)

                previous_song = data["item"]["name"]
                previous_song_url = data["item"]["album"]["images"][0]["url"]
                print("\nSong played: ", previous_song)
            except: ##resetting the token. need to test this out

                auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                                                        client_secret=SPOTIPY_CLIENT_SECRET)

                sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope))
                round = starting_round + i + 1
                print("\n===================================\nBeginning of round: ", round)
                next_song = sp.next_track()
                test = sp.seek_track(position_ms=60000)

                time.sleep(1)
                test2 = sp.currently_playing()
                data1 = json.dumps(test2)
                data = json.loads(data1)
                song_duration = data["item"]["duration_ms"]
                current_song_url = data["item"]["album"]["images"][0]["url"]
                progress = round * 10
                progress = progress

                export = html.render(progress=progress,
                                     current_song_url=current_song_url,
                                     previous_song=previous_song,
                                     previous_song_url=previous_song_url,
                                     current_round=round)

                # write out html code that is ready to be used
                Html_code = open("static/image.html", "w")
                Html_code.write(export)
                Html_code.close()

                time.sleep(seconds_between_songs-1)

                previous_song = data["item"]["name"]
                previous_song_url = data["item"]["album"]["images"][0]["url"]
                print("\nSong played: ", previous_song)

    else:
        print("Can't get token for", username)


if __name__ == "__main__":
    main()