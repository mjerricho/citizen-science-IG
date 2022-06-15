import json
import logging
import os
import shutil
from pprint import pprint

import msal
import requests


class CitizenScienceUpload:
    def __init__(self, config, debug) -> None:
        '''
        Initialise a class that automatically uploads
        the data into Teams folder.
        '''
        # optional extensive debugging
        self.debug = debug
        # logging.basicConfig(level=logging.DEBUG)

        self.config = config
        if self.debug:
            pprint(config)

    def generate_headers(self):
        '''
        Given the configuration of app and storage space, get the
        access token to fil up the headers. Then, return the headers.
        '''
        # initialising the app
        authority = self.config['login_endpoint'] + self.config['tenant_id']
        if self.debug:
            print(f"Authority: {authority}")
        app = msal.ConfidentialClientApplication(
            self.config["client_id"],
            client_credential=self.config["client_secret"],
            authority=authority)

        # acquiring token
        result = None

        # check the cache to see if this end user has signed in before
        accounts = app.get_accounts(username=self.config["username"])
        if accounts:
            logging.info("Account, and possibly token, exists in cache.")
            result = app.acquire_token_silent(self.config["scope"],
                                              account=accounts[0])

        # Get new token from AAD
        if not result:
            logging.info("No suitable token exists in cache")
            result = app.acquire_token_by_username_password(
                        self.config["username"],
                        self.config["password"],
                        scopes=self.config["scope"])
            if self.debug:
                print(result)
                print("Done with logging in")

        # processing access token and checking API call
        headers = {'Authorization': 'Bearer ' + result['access_token']}
        if "access_token" in result:
            graph_data = requests.get(
                self.config["endpoint"],
                headers=headers).json()
            if self.debug:
                print("Graph API call result: %s"
                      % json.dumps(graph_data, indent=2))
            return headers
        else:
            print(result.get("error"))
            print(result.get("error_description"))
            print(result.get("correlation_id"))
            # Might need to manually give consent
            if 65001 in result.get("error_codes", []):
                print("Visit this to consent:",
                      app.get_authorization_request_url(self.config["scope"]))

    def zip_dir(self, rel_dir_path, output_filename):
        '''
        Given the path to a folder, this method will zip the folder
        under <output_filename>.zip.
        '''
        shutil.make_archive(output_filename, 'zip', rel_dir_path)

    def upload_file(self, rel_file_path, headers):
        '''
        Given the filename in the directory and the headers,
        the code will upload the file in to Teams Sharepoint/Onedrive.
        input:
            rel_file_path<str>: file name
            headers<dict>: headers received from generate_headers
        '''
        # reading file
        dir_path = os.getcwd()
        abs_file_path = dir_path + "/" + rel_file_path
        if not os.path.exists(abs_file_path):
            raise Exception(f'Source {abs_file_path} not found.')

        # getting file
        with open(abs_file_path, 'rb') as upload:
            file_size = os.path.getsize(abs_file_path)
            media_content = upload.read()
            if self.debug:
                print("file found")
            request_body = {
                'item': {
                    '@microsoft.graph.conflictBehavior': 'replace',
                    'description': 'a large file',
                    'name': rel_file_path,
                }
            }

            # create upload sesion
            if self.debug:
                print("Creating upload session")
            upload_session_endpoint = f'{self.config["endpoint"]}/drives/{self.config["drive_id"]}/items/{self.config["item_id"]}:/{rel_file_path}:/createUploadSession'
            if self.debug:
                print(upload_session_endpoint)
            response_upload_session = requests.post(
                upload_session_endpoint,
                headers=headers,
                json=request_body["item"]
            )
            if self.debug:
                pprint(response_upload_session.json())

            try:
                if self.debug:
                    pprint(response_upload_session.json())
                upload_url = response_upload_session.json()['uploadUrl']
                if self.debug:
                    print("upload url: " + upload_url)
                    print("File size: " + str(file_size))
                param = {
                    'Content-Length': str(file_size),
                    'Content-Range': f"bytes 0-{str(file_size - 1)}/{str(file_size)}"
                    }
                response_upload_status = requests.put(upload_url,
                                                      data=media_content,
                                                      headers=param)
                print(f'File uploaded: {abs_file_path}')
                if self.debug:
                    pprint(response_upload_status.reason)
            except Exception as e:
                print(e)
