#REQUIREMENTS: python script delete_user.py, user_information.py, install date time in python3
#in this script we delete all users in the entire company, 
#who have been suspended longer then 3 months

from __future__ import print_function

import os  # needed to access the computers folders
from datetime import datetime

import httplib2  # needed for http requests
from googleapiclient import discovery  # from google
from oauth2client import client  # from google
from oauth2client import tools  # from google
from oauth2client.file import Storage  # from google
from datetime import date
from dateutil.relativedelta import relativedelta
import user_information

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/appsactivity-python-quickstart.json
# scopes are necessary to define in which areas your script may work
#SCOPES = """https://www.googleapis.com/auth/activity https://www.googleapis.com/auth/admin.directory.group https://www.googleapis.com/auth/admin.directory.group.member https://www.googleapis.com/auth/admin.directory.user"""
SCOPES = 'https://www.googleapis.com/auth/admin.reports.audit.readonly https://www.googleapis.com/auth/admin.reports.usage.readonly'
CLIENT_SECRET_FILE = 'client_secret.json' #name of your secret file
APPLICATION_NAME = 'G Suite: Delete all suspended users suspended longer than 3 months'

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
                                   'credentials_reports.json')

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

def convert_google_date_to_python3_date(googleDate):
    date = datetime.strptime(googleDate[:10],'%Y-%m-%d').date()
    return date

def older_then_3_months(check_date):
    if date.today()+relativedelta(months=-3) > check_date:
        return True
    else:
        return False

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    #We have to change from directory_v1 to reports_v1, otherwise the service wont recognize activities
    service = discovery.build('admin', 'reports_v1', http=http)
    #https://developers.google.com/apis-explorer/#p/admin/reports_v1/
    activities = service.activities().list(userKey='<an email address of a user with admin rights>', applicationName='admin',eventName='SUSPEND_USER').execute()
    users = []
    print('The following users were suspended longer then 3 months ago: ')
    for i in range(0,len(activities['items'])):
        date = convert_google_date_to_python3_date(activities['items'][i]['id']['time'])
        if older_then_3_months(date):
            if user_information.user_exists(activities['items'][i]['events'][0]['parameters'][0]['value']):
                print(activities['items'][i]['events'][0]['parameters'][0]['value'])
                users.append(activities['items'][i]['events'][0]['parameters'][0]['value'])


    confirmation = input('Do you want to delete all of these users? Type yes and press enter: \n')
    if confirmation == 'yes':
        for i in range(0,len(users)):
            os.system('python3 delete_user.py -u ' + users[i])
            print(users[i]+' deleted')
    else:
        print('Input wasn\'t yes. No changes were made')


if __name__ == '__main__':
    main()