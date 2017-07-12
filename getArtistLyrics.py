# John W. Miller
# 2017_0707

# Usage: python getArtistLyrics.py 'The Beatles'
# This is a branch test. From (song-and-artist-classes).

import sys
import re
import requests
import json
import urllib2
import socket
from bs4 import BeautifulSoup
import time

def load_credentials():
    lines = [line.rstrip('\n') for line in open('credentials.ini')]
    chars_to_strip = " \'\""
    for line in lines:
        if "client_id" in line:
            client_id = re.findall(r'[\"\']([^\"\']*)[\"\']', line)[0]
        if "client_secret" in line:
            client_secret = re.findall(r'[\"\']([^\"\']*)[\"\']', line)[0]
        #Currently only need access token to run, the other two perhaps for future implementation
        if "client_access_token" in line:
            client_access_token = re.findall(r'[\"\']([^\"\']*)[\"\']', line)[0]

    return client_id, client_secret, client_access_token

# Genius API credentials (available globally)
client_id, client_secret, client_access_token = load_credentials()
genius_url = "http://api.genius.com"
headers = {'Authorization': 'Bearer ' + client_access_token}

def search_genius(search_term):             
    querystring = "http://api.genius.com/search?q=" + urllib2.quote(search_term) + "&page=" + str(1)        
    request = urllib2.Request(querystring)
    request.add_header("Authorization", "Bearer " + client_access_token)   
    request.add_header("User-Agent", "curl/7.9.8 (i686-pc-linux-gnu) libcurl 7.9.8 (OpenSSL 0.9.6b) (ipv6 enabled)") #Must include user agent of some sort, otherwise 403 returned
    while True:
        try:
            response = urllib2.urlopen(request, timeout=4) #timeout set to 4 seconds; automatically retries if times out
            raw = response.read()
        except socket.timeout:
            print("Timeout raised and caught")
            continue
        break    

    return json.loads(raw)    

def get_song_and_artist_ids(song_title, artist_name):  
    json_obj = search_genius(song_title + " " + artist_name)
    body = json_obj["response"]["hits"]
    body = body[0] # Just keep the first hit (for now)
    song_api   = body['result']['api_path']
    artist_api = body['result']['primary_artist']['api_path']
    
    return song_api, artist_api

def get_genius_api_item(api_path):
    base_url = "http://api.genius.com"
    querystring = base_url + api_path      
    request = urllib2.Request(querystring)
    request.add_header("Authorization", "Bearer " + client_access_token)   
    request.add_header("User-Agent", "curl/7.9.8 (i686-pc-linux-gnu) libcurl 7.9.8 (OpenSSL 0.9.6b) (ipv6 enabled)") #Must include user agent of some sort, otherwise 403 returned
    while True:
        try:
            response = urllib2.urlopen(request, timeout=4) #timeout set to 4 seconds; automatically retries if times out
            raw = response.read()
        except socket.timeout:
            print("Timeout raised and caught")
            continue
        break

    return json.loads(raw)

def get_artist_song_ids(artist_name):
    obj = search_genius(artist_name)
    song_title = obj['response']['hits'][0]['result']['title']
    song_id, artist_id = get_song_and_artist_ids(song_title,artist_name)
    id_num = int(artist_id.split('/')[-1])

    # Okay, we have the artist API id, let's get a list of all of their songs on Genius
    all_song_ids = []
    page = 1
    print('\nGetting song IDs from Genius.com...')
    while True:
        # Access the Genius API to get artist's songs
        artist_api_path = artist_id + '/songs' + '?page=%d' % page
        json_obj = get_genius_api_item(artist_api_path)     
        songs = json_obj['response']['songs']
        
        # Only keep a song's API path if its primary artist is correct
        [all_song_ids.append(song['api_path']) for song in songs if song['primary_artist']['id'] == id_num]            

        # Break the loop if we're on the last page
        num_songs = len(songs)
        print("Found {0} possible songs on page {1}.".format(num_songs, page))    
        if json_obj['response']['next_page']==None:
            if page==1 & num_songs == 0:
                print("No results for: " + search_term)
            break              
        page += 1
        
    print('Total songs found: {0}.'.format(len(all_song_ids)))
    return all_song_ids

def scrape_lyrics_from_song_api(song_api_path):
    # Use BeautifulSoup to scrape lyrics off of a Genius song URL
    json_obj = get_genius_api_item(song_api_path)

    # Get the URL to the song lyrics
    path = json_obj['response']['song']['path']
    page_url = "http://genius.com" + path
    page = requests.get(page_url)    
    html = BeautifulSoup(page.text, "html.parser")
    [h.extract() for h in html('script')]        
    lyrics = html.find("div", class_="lyrics").get_text().encode('ascii','ignore').decode('ascii')
    lyrics = re.sub('\[.*\]','',lyrics) # Remove [Verse] and [Bridge] stuff
    lyrics = re.sub('\n{2}','',lyrics)  # Remove gaps between verses
    return str(lyrics)

def write_lyrics_to_file(lyrics,artist=''):   
    if artist!='':
        filename = 'Lyrics_{0}.txt'.format(artist.replace(' ',''))
    else:
        filename = "Lyrics.txt"
    with open(filename, "a") as text_file:
        text_file.write('\n' + lyrics)

def main(): 
    t = time.time()
    artist_name = sys.argv[1].translate(None,"\'\"")
    print('Starting search for {0} lyrics.'.format(artist_name))
    
    # Get list of Genius API IDs for all songs by artist
    all_song_ids = get_artist_song_ids(artist_name)

    # Write out a file containing the lyrics for all of the artist's songs
    print('\nWriting lyrics to file...')
    for i in range(len(all_song_ids)):
        print('Writing song {0} of {1}.'.format(i+1,len(all_song_ids)))
        lyrics = scrape_lyrics_from_song_api(all_song_ids[i])
        write_lyrics_to_file(lyrics,artist_name)

    print('Done. Total time: %0.1f minutes.' % ((time.time()-t)/60.0))

if __name__ == '__main__':
    main()
