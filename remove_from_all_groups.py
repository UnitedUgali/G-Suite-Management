#REQUIREMENTS: script user_information.py, remove_from_group.py
#This script removes a user from all groups
from __future__ import print_function
import httplib2 #needed for http requests
import os #needed to access the computers folders
import sys #needed to pass arguments and options to the script at startup
import argparse
import user_information

from googleapiclient import discovery # from google
from oauth2client import client # from google
from oauth2client import tools # from google
from oauth2client.file import Storage # from google
from user_information import user_exists
from remove_from_group import remove_from_group
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/appsactivity-python-quickstart.json
# scopes are necessary to define in which areas your script may work
SCOPES = 'https://www.googleapis.com/auth/activity https://www.googleapis.com/auth/admin.directory.group https://www.googleapis.com/auth/admin.directory.group.member https://www.googleapis.com/auth/admin.directory.user'
CLIENT_SECRET_FILE = 'client_secret.json' #name of your secret file
APPLICATION_NAME = 'G Suite: Remove a user from all groups'

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
    credential_dir = os.path.join(home_dir, '.credentials_for_groups')
    if not os.path.exists(credential_dir):
          os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'group_credentials.json')

    store = Storage(credential_path)
    credentials = store.get()
    #should the upper generated credentials(=access token) should be invalid:
    if not credentials or credentials.invalid:
        #we generate a new one from the client secret
        print("Somehow no credentials")
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        print("Flow created")
        flow.user_agent = APPLICATION_NAME
        print("agent created")
        # You need to define the flags like this otherwise
        # Google will try to use your initial arguments as arguments
        # to create credentials
        flags = tools.argparser.parse_args('--auth_host_name localhost --logging_level INFO'.split())
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Removes a user from all email groups"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--user', help='The user mail address')
    args = parser.parse_args()

    if not user_exists(args.user):
        print("Program cancelled. No changes were made")
        sys.exit()

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('admin', 'directory_v1', http=http)
    groups = user_information.get_all_groups_from(args.user,service)
    #response = service.groups().list(userKey=args.user)
    #group_json = response.execute()
    print(args.user+" removed from the following groups:")
    #in the following we're just extracting the group names out of the json object
    #and store it in a string array so we can later just fire the requests from a
    #clean and readable string array called "groups"
    try:
        for i in range(0, len(groups)):
            remove_from_group(args.user, groups[i],service)
    except KeyError:
        print(args.user+" wasn't part of any group. No changes were made")

if __name__ == '__main__':
    main()
