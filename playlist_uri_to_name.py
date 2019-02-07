{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 53,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import sys\n",
    "import spotipy\n",
    "import os\n",
    "from spotipy.oauth2 import SpotifyClientCredentials\n",
    "from xlrd import open_workbook, cellname\n",
    "import requests\n",
    "import csv\n",
    "import time\n",
    "from tqdm import tqdm"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 54,
   "metadata": {},
   "outputs": [],
   "source": [
    "#spotify client\n",
    "SPOTIPY_CLIENT_ID = 'INSERT CLIENT ID'\n",
    "SPOTIPY_CLIENT_SECRET = 'INSERT CLIENT SECRET'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 55,
   "metadata": {},
   "outputs": [],
   "source": [
    "client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)\n",
    "sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 56,
   "metadata": {},
   "outputs": [],
   "source": [
    "#verifying credentials and returning access token\n",
    "grant_type = 'client_credentials'\n",
    "\n",
    "#Request based on Client Credentials Flow from https://developer.spotify.com/web-api/authorization-guide/\n",
    "\n",
    "#Request body parameter: grant_type Value: Required. Set it to client_credentials\n",
    "body_params = {'grant_type' : grant_type}\n",
    "\n",
    "url='https://accounts.spotify.com/api/token'\n",
    "\n",
    "response=requests.post(url, data=body_params, auth = (SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)) \n",
    "access_token = response.json()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 57,
   "metadata": {},
   "outputs": [
    
   ],
   "source": [
    "#import excel\n",
    "df = pd.read_excel(r'FILE NAME', sheet_name = 1)\n",
    "data = pd.DataFrame(df, columns = ['Name', 'URI'])\n",
    "check = data.to_dict('records')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 58,
   "metadata": {},
   "outputs": [],
   "source": [
    "#list of accepted and unaccepted URIs\n",
    "accepted_uri = []\n",
    "unaccepted_uri = []"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 59,
   "metadata": {},
   "outputs": [
   ],
   "source": [
    "#clean up URI and request data\n",
    "client = spotify_client = spotipy.Spotify(access_token[\"access_token\"])\n",
    "uri_final = []\n",
    "\n",
    "for i in tqdm(len(check)): ##progress back\n",
    "    for row in check:\n",
    "        try:\n",
    "            playlist_user = row[\"URI\"].split(':')[2]\n",
    "            uri = row[\"URI\"]\n",
    "            playlist_data = client.user_playlist(user=playlist_user, playlist_id = uri)\n",
    "            small_list = []\n",
    "            small_list.append(playlist_data[\"name\"])\n",
    "            small_list.append(uri)\n",
    "            uri_final.append(small_list)\n",
    "        except:\n",
    "            print \"ERROR: \" + uri\n",
    "            small_list = []\n",
    "            small_list.append(\"NULL\")\n",
    "            small_list.append(uri)\n",
    "            uri_final.append(small_list)\n",
    "            unaccepted_uri.append(uri)\n",
    "        \n",
    "print \"DONE\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 48,
   "metadata": {},
   "outputs": [
   ],
   "source": [
    "#replace name in csv\n",
    "with open('uri_with_name.csv', mode='w') as new_file:\n",
    "    name_writer = csv.writer(new_file, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)\n",
    "    for row in uri_final:\n",
    "        artist = row[0].encode('utf-8')\n",
    "        uri = row[1].encode('utf-8')\n",
    "        name_writer.writerow([artist, uri])\n",
    "    new_file.close()\n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 51,
   "metadata": {},
   "outputs": [],
   "source": [
    "with open('unaccepted_uri.txt', mode='w') as f:\n",
    "    name_writer = csv.writer(f, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)\n",
    "    for row in unaccepted_uri:\n",
    "        f.write(row + \"\\n\")\n",
    "    f.close()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 2",
   "language": "python",
   "name": "python2"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 2
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython2",
   "version": "2.7.15"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
