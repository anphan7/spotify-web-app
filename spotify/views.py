from django.shortcuts import render, redirect
from .credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from rest_framework import  status
from requests import Request, post
from rest_framework.response import Response
from rest_framework.views import APIView
from .util import update_or_create_user_tokens, is_spotify_authenticated

class AuthURL(APIView):
    '''
        From the frontend, call this function -> take the url that returned -> redirect to the Spotify's authorization page
    '''
    def get(self, request, fornat=None):
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'

        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }).prepare().url

        return Response({'url': url}, status=status.HTTP_200_OK)

'''
    After the user finished authorizing, redirect user to the application:

'''
def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    # Send the request for the tokens
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    # Store the tokens
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    if not request.session.exists(request.session.session_key):
            request.session.create()

    update_or_create_user_tokens(request.session.session_key, access_token, token_type, expires_in, refresh_token)

    # Redirect back the user to the application
    return redirect('frontend:') # Redirect to the homepage


class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(self.request.session.session_key)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)
        