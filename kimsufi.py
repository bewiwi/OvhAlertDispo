__author__ = 'bewiwi'
import requests
import os
import ConfigParser

config = ConfigParser.ConfigParser()
config.read(['kimsufi.conf'])
serv = config.get('DEFAULT','serv').split(',')
command = config.get('DEFAULT','command')

#Get INFO
url='https://ws.ovh.com/dedicated/r2/ws.dispatcher/getAvailability2'
headers = {'content-type': 'application/json'}
r = requests.get(url, headers=headers)
rep = r.json()

#Check Dispo
message=''
servers=''
one_serv_avaible=False
for r in rep['answer']['availability']:
    if r['reference'] not in serv:
        continue

    for zone in r['zones']:
        if zone['availability'] != 'unavailable':
            one_serv_avaible=True
            #%serveurs%
            if servers != '':
                servers+=','
            servers+=r['reference']

            #%message%
            if message != '':
                message+='\n'
            message+="Serveur : %s, Time : %s, Datacenter : %s" % (r['reference'],zone['availability'],zone['zone'])

if not one_serv_avaible:
    exit(0)

#Exec Command
print message
print servers

command = command.replace('%message%',message)
command = command.replace('%servers%',servers)
print command

os.system(command)