#in this script we create a user with the email address: #<surname>.<lastname>@<companydomain>.com

from __future__ import print_function
import httplib2 #needed for http requests
import os #needed to access the computers folders
import sys #needed to pass arguments and options to the script at startup

from googleapiclient import discovery # from google
from oauth2client import client # from google
from oauth2client import tools # from google
from oauth2client.file import Storage # from google
import argparse

#try:
#    import argparse
#    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
#except ImportError:
#    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/appsactivity-python-quickstart.json
# scopes are necessary to define in which areas your script may work
SCOPES = 'https://www.googleapis.com/auth/activity https://www.googleapis.com/auth/admin.directory.group https://www.googleapis.com/auth/admin.directory.group.member https://www.googleapis.com/auth/admin.directory.user'
CLIENT_SECRET_FILE = 'client_secret.json' #name of your secret file
APPLICATION_NAME = 'G Suite: Create User'

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

#This method creates out of a user name consisting of at least two or more words (surname, optional middle names, last name)
#an array with surname at 0, optional middle names at 1 and last name at 2
def sanitize_arguments(string):
    #checks the input arguments and returns a string array
    #0: first name
    #1: middle name, can be empty!
    #2: last name
    name = string.split()
    if len(name)<2:
        print('Error: A user needs at least a first name and a last name. ')
        sys.exit('A user needs at least a first name and a last name')
    firstName = ""
    middleName=""
    if len(name)>2:
        for i in range(1, len(name)-1): 
            middleName += name[i]+" "
    firstName = name[0]
    lastName = name[len(name)-1]
    print("First Name: "+firstName)
    if middleName:
        print("Middle Name:"+middleName)
    print("Last Name: "+lastName)
    name[0] = firstName
    name[1] = " "+middleName
    if len(name)<3:
        name.append(lastName)
    else:
        name[2]=lastName

    return name

#at the company unit <Your company>
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-un', '--username', help="""The users full name address you want to create.\n
                                                     Please write the name like the following \'name\'""")
    args = parser.parse_args()
    name = sanitize_arguments(args.username)
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    #Check the APIs under https://developers.google.com/api-client-library/python/apis/
    # then you'll see what kind of service you need to create.
    #Discovery.build comes from probably Google, Admin and directory_v1 is
    #found on googles page
    service = discovery.build('admin', 'directory_v1', http=http)
    response = service.users().insert(
        body={
            'primaryEmail': name[0]+'.'+name[2]+'@<your_company_domain>.com',
            'name': {
                'givenName': name[0]+name[1],
                'familyName': name[2],
            },
            'orgUnitPath': '/<Your Company>',
            'password': '<a predefined password>'
        })
    #sys.exit()
    response.execute()
    print("User "+str(name)+" created. Primary email address: "+name[0]+"."+name[2]+"@<your_company_domain>.com")

if __name__ == '__main__':
    main()
