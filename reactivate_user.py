#REQUIREMENTS: script user_information.py
#This script reactivates a suspended user (not a deleted user!)
from __future__ import print_function
import httplib2 #needed for http requests
import os #needed to access the computers folders
import argparse

from googleapiclient import discovery # from google
from oauth2client import client # from google
from oauth2client import tools # from google
from oauth2client.file import Storage # from google
import user_information


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/appsactivity-python-quickstart.json
# scopes are necessary to define in which areas your script may work
SCOPES = 'https://www.googleapis.com/auth/activity https://www.googleapis.com/auth/admin.directory.group https://www.googleapis.com/auth/admin.directory.group.member https://www.googleapis.com/auth/admin.directory.user'
CLIENT_SECRET_FILE = 'client_secret.json' #name of your secret file
APPLICATION_NAME = 'Create User Script'

# This method basically just checks if a client secret is there and if not it creates another one
# through the OAuth flow method. The secret file needs to exist though, otherwise no credentials can get created!
def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
          os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'appsactivity-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    #should the upper generated credentials(=access token) should be invalid:
    if not credentials or credentials.invalid:
        #we generate a new one from the client secret
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
#You need to define the flags like this otherwise
        #Google will try to use your initial arguments as arguments
        #to create credentials
        flags = tools.argparser.parse_args('--auth_host_name localhost --logging_level INFO'.split())
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():
    """Shows basic usage of the G Suite Activity API.

    Creates a G Suite Activity API service object and
    outputs the recent activity in your Google Drive.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--user', help="The user you want to reactivate")
    args = parser.parse_args()

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    #Check the APIs under https://developers.google.com/api-client-library/python/apis/
    # then you'll see what kind of service you need to create.
    #Discovery.build comes from probably Google, Admin and directory_v1 is
    #found on googles page
    print(args.user)
    if user_information.user_exists(args.user):
        service = discovery.build('admin', 'directory_v1', http=http)
        response = service.users().update(userKey=args.user,
            body={
                "suspended": False
            })
        #sys.exit()
        response.execute()
        print(args.user+' successfully reactivated')
    else:
        print("Error: "+args.user+" doesn't seem to exist")

if __name__ == '__main__':
    main()
