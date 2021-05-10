# -*- coding: utf-8 -*-

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaFileUpload

import data

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def upload():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret_1051216375102-go4rrjng7a54nknrt0p2eh2ubfm7bo7i.apps.googleusercontent.com.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.thumbnails().set(
        videoId=data.video_id,
        media_body=MediaFileUpload(data.export_filename)
    )
    response = request.execute()
    print(response)
