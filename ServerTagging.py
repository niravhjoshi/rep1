##### Script to fetch tag information and Servers associated with the particular tag

import argparse
import SoftLayer
import sys

parser = argparse.ArgumentParser(description='Welcome !! This script is to fetch Server details based on Tagging')
parser.add_argument('-user',action='append', type=str,  help='Input for User name')
parser.add_argument('-apiKey',action='append', type=str,  help='Input for API Key')
parser.add_argument('-tag',action='append', type=str,  help='Input for tag name')
parser.add_argument('-fqdn',action='append', type=str,  help='Input for Device fqdn')

args = parser.parse_args()
apiUsername =  args.user[0]
apiKey = args.apiKey[0]
tagName =  args.tag[0]

#Only lower case tags are allowed to be set, hence only lower case should be searched 
tagName = tagName.lower()

if (args.fqdn):
    fqdn = args.fqdn[0]
else: 
	fqdn = ''

#Create client object to interact with API's
client = SoftLayer.Client(username=apiUsername, api_key=apiKey)

print "----------------------------------------------------------------------"
#Check if username and api authentication is working using try except
try:
	userId = client['Account'].getCurrentUser(mask='id')
	print "Authentication Success, Correct -user and -apiKey provided"
except SoftLayer.exceptions.SoftLayerAPIError as e:
	print "Incorrect -user or -apikey argument value provided"
	print e
except:
	print "Unexpected error occured"
	sys.exit(3) 
print "----------------------------------------------------------------------"

#tagData will contain the actual tagid of the tagName variable
tagData = client['Tag'].getTagByTagName(tagName,filter={'references':{'usrRecordId':userId}})

if (tagData):
    tagId = tagData[0]['id']
    print "\n\n ********   Server list with the tag name = " + tagName + "  ******** \n\n"
    #devices will contain the id of all the devices on which the required tag is present
    devices = client['Tag'].getReferences(id=tagId,mask='resourceTableId')
    for each in devices:
		#Using hardware service get the object with required id and only fetch the FQDN Property:value pair.
		try:
			devicefqdn=client['Hardware'].getObject(id=each['resourceTableId'],mask='fullyQualifiedDomainName')
		except :
			print "\n **** Given tag : " + tagName + " is not associated with any device of user " + apiUsername + " ****"
			sys.exit(3)
		if (fqdn == ''):
			print devicefqdn['fullyQualifiedDomainName']
		else:
			if (devicefqdn['fullyQualifiedDomainName'] in fqdn):
				print devicefqdn['fullyQualifiedDomainName']
else:
    print "\n **** Tag name is not present **** "
