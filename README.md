# G Suite Management
This repository contains scripts in Python 3 to perform specific mostly user related tasks in G Suite.
You need to have an API access and a client_secret.json file stored in the same folder as the repository. From there you can execute each script by itself using its mandatory options, which are documented in the -help flags. The method 'get_credentials' is at the moment implemented in every script because in a few occasions the scopes vary. With more time one could certainly simplify some things. 
Important: Some scripts depend on each other, as descriped in the head of the script! Make sure you've downloaded all or the  ones needed.

You need to install:
For the google api client:
1. pip3 install --upgrade google-api-python-client
2. pip3 install oauth2client
3. pip3 install httplib2
4. pip3 install python-dateutil

and get Oauth2 Credentials from here https://console.developers.google.com.
Name the file client_secret.json or adapt the filename in the code.
