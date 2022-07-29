import os
import json
from threading import currentThread
import time
import spotipy
import json
import lyricsgenius as lg
import requests
from secrets import spotipy_client_id, spotipy_secret, spotipy_redirect_uri, genius_access_token


scope = 'user-read-currently-playing'

#Getting auth to user's spotify account
oauth_object = spotipy.SpotifyOAuth(client_id = spotipy_client_id,
                                    client_secret= spotipy_secret,
                                    redirect_uri= spotipy_redirect_uri,
                                    scope = scope
                                    )


#google will open up and we will copy and past the url to the terminal and received our access token
#print (oauth_object) 
token_dict = oauth_object.get_access_token()
token = token_dict['access_token']
#print (token_dict['access_token'])

#our spotify object
spotipy_object = spotipy.Spotify(auth=token)

#our genius object
genius_object = lg.Genius(genius_access_token)


while True:
        #Lets test whether the user is playing a song or not:
        playbackState = True
        while playbackState:
                try:
                        current = spotipy_object.currently_playing()
                        current_type = current['currently_playing_type']
                        if current_type == 'track' or current_type == 'ad':
                                playbackState =False
                except:
                        print("Please play a song for the lyrics to generate. Trying again in 20 seconds!")
                        time.sleep(20)
        #get the current song & and whether its a song or ad
        if current_type == 'track':
                #get artist and song name
                artist_name = current['item']['album']['artists'][0]['name'] #getting the keys for the dictionary
                song_title = current['item']['name']

                #get song lyrics from Genius API
                song = genius_object.search_song(title =song_title, artist =artist_name) #you don't need to put title= or artist=...can just add args to parameter
                lyrics = song.lyrics

                #JSON Format of Spotify Song(Optional):
                #print (json.dumps(current, sort_keys = False, indent =4))

                #get the song time and the time progress at which the song is being played at ie. 37s.
                length_ms = current['item']['duration_ms']
                progress_ms = current['progress_ms']
                timeLeft = int((length_ms - progress_ms)/1000)
                print ('time left:' , timeLeft)

                #print Lyrics!
                print (lyrics)
                time.sleep(timeLeft)
        elif current_type =='ad':
                print('Ad is curently playing. Lyric generator will continue in thirty seconds')
                time.sleep(30)
        
