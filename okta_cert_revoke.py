#!/usr/bin/python3
#
# Copyright 2018-present, Okta Inc.
#
# Script to revoke client certificates per device #
# https://help.okta.com/en/prod/Content/Topics/Miscellaneous/Third-party%20Licenses/ 3rd%20Party%20Notices_Okta%20Password%20Sync%20Setup.pdf
#
# APIs used in this process are internal APIs and they are subject to changes without prior notice. #

import subprocess
import json

SERVER = 'https://<DOMAIN Here>.okta.com'
ORG_API_TOKEN = 'SSWS <Okta API Key Here>'
MAC_UDID = '<MAC UDID Here>'

def get_and_revoke_certs():
    url = '%s/api/v1/internal/devices/%s/credentials/keys' % (SERVER, MAC_UDID)
    print ('Getting certs for device: ' + str(MAC_UDID))
    response = subprocess.check_output(['curl', '-sS', '-X', 'GET', '-H', 'Authorization: ' + ORG_API_TOKEN, url])
    print ('Response: ' + str(response))
    data = json.loads(response)
    if not data:
        print ('No certs found')
        exit(0)
    for key in data:
        if 'kid' not in key:
            print ('Error response.')
            exit(1)
        revoke_cert(key['kid'])
        print ('Finished')

def revoke_cert(kid):
    url = '%s/api/v1/internal/devices/%s/keys/%s/lifecycle/revoke' % (SERVER, MAC_UDID, kid)
    print ('Revoking certificate: ' + str(kid))
    response = subprocess.check_output(['curl', '-sS', '-X', 'POST', '-H', 'Authorization: ' + ORG_API_TOKEN, url])
    print ('Response: ' + str(response))

def check_params():
    if not SERVER:
        print ("SERVER can't be empty, please populate org URL eg. https://&lt;org>.okta.com")
        exit(1)
    if not ORG_API_TOKEN:
        print ("ORG_API_TOKEN can't be empty, please assign API token eg. SSWS <API- Token>")
        exit(1)
    if not MAC_UDID:
        print ("MAC_UDID can't be empty, please assign macOS UDID")
        exit(1)

check_params()
get_and_revoke_certs()
