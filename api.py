import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd


#definimos credenciales


client_id = 'b6841f7c97974c8aacbdf448dae8677f'
client_secret = 'bc15cade85bc41f88d451fbb2c832eff'
redirect_uri = 'http://localhost:8888/callback/'
scope = 'user-read-private'

#utilizamos spotipy para interactuar con la API de spotify para buscar cancciones
# obtener listas de reproduccion, reproducir musica, etc

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret = client_secret,
        redirect_uri=redirect_uri,
        scope=scope
    )
)

#buscamos un artista por su nombre
artist_input = st.text_input('Escribe tu artista:' )
artist = artist_input
results = sp.search(q = f'artist:{artist}', type='artist')

#obtenemos el ID del primer artista en los resultados
if not results['artists']['items']:
    print('No se encuentra disponible el artista.')

else:
    artist_id = results['artists']['items'][0]['id'] #nos muestra el id del artista buscado

    #obtenemos todos los albumes del artista
    albums = sp.artist_albums(
        artist_id,
        album_type='album',
        limit=50
    )

    artist_info = sp.artist(artist_id)
    followers_count = artist_info['followers']['total']  # Número de seguidores


    
    #lista para almaceenar todas las canciones y albumes
    all_songs = []

    #iteramos para recorrer cada album de la lista
    for album in albums['items']:
        #album_image_url = album['images'][0]['url'] if album['images'] else None
        songs = sp.album_tracks(album['id'])['items']
        for song in songs:
            song_info = sp.track(song['id'])
            all_songs.append(
                {
                    'album':album['name'],
                    'release_date':album['release_date'],
                    'songs': song['name'],
                    'song_duration': song['duration_ms'] / 1000,
                    'followers': followers_count,
                    'popularity_song': song_info['popularity']
                    
                    
                }
            )

albums = pd.DataFrame(all_songs)

if not artist == '':
    st.dataframe(albums)