#!/usr/bin/env python
"""
Google Drive API initializer
Author: Colin Su <littleq0903@gmail.com>
"""
import httplib2
import os

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage

OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive' # OAuth scope
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob' # Redirect URI for installed apps

CLIENT_SECRET_FILE = 'credentials/client_secret.json'
CLIENT_CREDENTIAL_STORAGE_LOCATION = 'credentials/iyp_spider_credential'

def get_drive_service(credential_file=CLIENT_SECRET_FILE):
    """
    Returns a Google Drive service instance in order to make use of Google Drive API
    In the flow it will open a new browser window and guide you how to authenticate automatically
    """
    # Credentials
    credentialStorage = Storage(CLIENT_CREDENTIAL_STORAGE_LOCATION)
    credentials = credentialStorage.get()

    if not credentials:
        # OAuth authentication if no any credentials
        
        # determine client secrets
        flow = flow_from_clientsecrets(credential_file,
                scope=OAUTH_SCOPE,
                redirect_uri=REDIRECT_URI)

        # Step1
        authorizeUrl = flow.step1_get_authorize_url()
        print 'Go to the following link:\n%s' % authorizeUrl
        os.system('open "%s"' % authorizeUrl)
        authorizeCode = raw_input("Verification Code: ").strip()

        # Step2
        credentials = flow.step2_exchange(authorizeCode)

        # save credentials
        credentialStorage.put(credentials)

    # Build Drive Service Point
    http = httplib2.Http()
    http = credentials.authorize(http)

    return build('drive', 'v2', http=http)

def put_csv(file_path, title, description="", service=None):
    """
    Upload and convert csv file to spreadsheet on Drive
    """

    if not service:
        service = get_drive_service()

    mediaBody = MediaFileUpload(file_path, mimetype='text/csv')
    body = {
            'title': title,
            'description': description,
            'mimeType': 'text/csv'
            }

    request = service.files().insert(media_body=mediaBody, body=body, convert=True)
    response = request.execute()
    return response

if __name__ == '__main__':
    # Test fetching service client
    print get_drive_service()

    # Test upload csv
    csv_file = 'samples/sample.csv'
    put_csv(csv_file, "test")
