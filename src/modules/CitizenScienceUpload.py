import json
import logging
import os
from pprint import pprint

import msal
import requests


class CitizenScienceUpload:
    def __init__(self, config, debug) -> None:
        '''
        Initialise a class that gets assists in uploading
        the data into Teams folder.

        You can find the other permission names from this document
        https://docs.microsoft.com/en-us/graph/permissions-reference
        You can find more Microsoft Graph API endpoints from Graph Explorer
        https://developer.microsoft.com/en-us/graph/graph-explorer

        You can then run this sample with a JSON configuration file:

            python sample.py config.json <filename>
        '''
        # optional extensive debugging
        self.debug = debug
        # logging.basicConfig(level=logging.DEBUG)

        # getting configuration variables
        self.config = config
        if debug: pprint(config)

    def generate_headers(self):
        '''
        Given the configuration of app and storage space, get the
        access token to fil up the headers. Then, return the 
        headers.
        '''
        # initialising the app
        authority = self.config['login_endpoint'] + self.config['tenant_id']
        if self.debug: print(f"Authority: {authority}")
        app = msal.ConfidentialClientApplication(
            self.config["client_id"], 
            client_credential=self.config["client_secret"], 
            authority=authority
            )

        # acquiring token
        result = None

        # check the cache to see if this end user has signed in before
        accounts = app.get_accounts(username=self.config["username"])
        if accounts:
            logging.info("Account(s) exists in cache, probably with token too. Let's try.")
            result = app.acquire_token_silent(self.config["scope"], account=accounts[0])

        if not result:
            logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
            # See this page for constraints of Username Password Flow.
            # https://github.com/AzureAD/microsoft-authentication-library-for-python/wiki/Username-Password-Authentication
            result = app.acquire_token_by_username_password(
                self.config["username"], self.config["password"], scopes=self.config["scope"])
            if self.debug: 
                print(result)
                print("Done with logging in")

        # processing access token and checking API call
        headers={'Authorization': 'Bearer ' + result['access_token']}
        if "access_token" in result:
            graph_data = requests.get(
                self.config["endpoint"],
                headers=headers).json()
            if self.debug: print("Graph API call result: %s" % json.dumps(graph_data, indent=2))
            return headers
        else:
            print(result.get("error"))
            print(result.get("error_description"))
            print(result.get("correlation_id")) 
            # Might need to manually give consent
            if 65001 in result.get("error_codes", []):
                print("Visit this to consent:", app.get_authorization_request_url(self.config["scope"]))

    def upload_file(self, file_name, headers):
        '''
        Given the filename in the directory and the headers,
        the code will upload the file in to Teams Sharepoint/Onedrive.
        '''
        # reading file
        dir_path = os.getcwd()
        file_path = dir_path + "/" + file_name
        if not os.path.exists(file_path):
            raise Exception(f'{file_name} is not found.')

        # getting file
        with open(file_path, 'rb') as upload:
            file_size = os.path.getsize(file_path)
            media_content = upload.read()
            if self.debug: print("file found")

            request_body = {
                'item': {
                    '@microsoft.graph.conflictBehavior': 'replace',
                    'description': 'a large file',
                    'name': file_name,
                }
            }

            # create upload sesion
            if self.debug: print("Creating upload session")
            upload_session_endpoint = self.config["endpoint"] + f'/drives/{self.config["drive_id"]}/items/{self.config["item_id"]}:/{file_name}:/createUploadSession'
            if self.debug: print(upload_session_endpoint)
            response_upload_session = requests.post(
                upload_session_endpoint,
                headers=headers,
                json=request_body["item"]
            )
            if self.debug: pprint(response_upload_session.json())

            # using the upload session
            try:
                if self.debug: pprint(response_upload_session.json())
                upload_url = response_upload_session.json()['uploadUrl']
                if self.debug: print("upload url: " + upload_url)
                print("------")
                print("FILE SIZE: " + str(file_size))
                param = {
                    'Content-Length': str(file_size), 
                    'Content-Range': f"bytes 0-{str(file_size - 1)}/{str(file_size)}"
                    }
                response_upload_status = requests.put(upload_url, data=media_content, headers=param)
                print(f'File uploaded: {file_path}')
                if self.debug: pprint(response_upload_status.reason)
            except Exception as e:
                print(e)
