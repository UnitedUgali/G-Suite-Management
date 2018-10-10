#this script provides several methods, which provide each a list of email addresses
#of users
from __future__ import print_function
import httplib2 #needed for http requests
import os #needed to access the computers folders

from googleapiclient import discovery # from google
from googleapiclient.errors import HttpError
from oauth2client import client # from google
from oauth2client import tools # from google
from oauth2client.file import Storage # from google

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/appsactivity-python-quickstart.json
# scopes are necessary to define in which areas your script may work
SCOPES = 'https://www.googleapis.com/auth/activity https://www.googleapis.com/auth/admin.directory.group https://www.googleapis.com/auth/admin.directory.group.member https://www.googleapis.com/auth/admin.directory.user'
CLIENT_SECRET_FILE = 'client_secret.json' #name of your secret file
APPLICATION_NAME = 'G Suite: This file contains various methods providing you information about users'

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
                                   'credentials.json')

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
        #You need to define the flags like this otherwise
        #Google will try to use your initial arguments as arguments
        #to create credentials
        flags = tools.argparser.parse_args('--auth_host_name localhost --logging_level INFO'.split())
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

#checks if a user exists
def user_exists(user):
    if not user:
        print("user_exists.py: User name is empty!")
        return False
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('admin', 'directory_v1', http=http)

    try:
        response = service.users().get(userKey=user).execute()
    except HttpError as err:
        #print("user_exists.py: User " + user + " not found!")
        return False

    return True

#this method returns all suspended users from all company units in g suite
def get_suspended_users_from_all_companies():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('admin', 'directory_v1', http=http)
    #my_customer is a default value for a query to list all users
    response = service.users().list(customer='my_customer', query='isSuspended=True' ).execute()
    #print(response)
    users = [""]
    for i in range(0,len(response['users'])):
        users.append(response['users'][i]['primaryEmail'])
    users.pop(0)
    return users

def get_all_groups_from(user, service):
    try:
        groups_json = service.groups().list(userKey=user).execute()
    except HttpError:
        print('Service not valid, could not retreive groups')
    groups = ['']
    try:
        for i in range(0, len(groups_json['groups'])):
            groups.append(groups_json['groups'][i]['email'])
    except KeyError:
        print(user + " wasn't part of any group. No change made.")

    groups.pop(0)
    if groups != '':
        return groups
    else:
        return None
#returns all users from a specific company unit
def get_all_users(company):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('admin', 'directory_v1', http=http)
    if(company):
        try:
            response = service.users().list(customer='my_customer', query='orgUnitId='+company).execute()
        except HttpError:
            print("Company "+company+" doesn't seem to exist")
            return None
    else:
        response = service.users().list(customer='my_customer').execute()
    users = [""]
    for i in range(0,len(response['users'])):
        users.append(response['users'][i]['primaryEmail'])
    users.pop(0)
    return users


def get_all_active_users(company):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('admin', 'directory_v1', http=http)
    if(company):
        try:
            response = service.users().list(customer='my_customer', query='isSuspended=False orgUnitId='+company).execute()
        except HttpError:
            print("Company "+company+" doesn't seem to exist")
            return None
    else:
        response = service.users().list(customer='my_customer',query='isSuspended=False').execute()
    users = [""]
    for i in range(0,len(response['users'])):
        users.append(response['users'][i]['primaryEmail'])
    users.pop(0)
    return users
