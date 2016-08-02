import argparse
import SoftLayer

parser = argparse.ArgumentParser(description='Welcome !! This script is to fetch Server details based on Tagging')
parser.add_argument('-user',action='append', type=str,  help='Input for User name')
parser.add_argument('-apiKey',action='append', type=str,  help='Input for API Key')
parser.add_argument('-tag',action='append', type=str,  help='Input for tag name')
parser.add_argument('-fqdn',action='append', type=str,  help='Input for Device fqdn')

# if the any of the above argument is passed, then there should also be a value associated with it
# if there is no value associated, python itself throws error.
# So we need not check if an value has been passed with argument

args = parser.parse_args()
apiUsername =  args.user[0]
apiKey = args.apiKey[0]
tagName =  args.tag[0]

# fqdn is an optional argument, and may not be passed each the time script is executed.
# so we need to check first if it has been passed beafore saving its value
if (args.fqdn):
	fqdn = args.fqdn[0]
else:
	fqdn = ''


#Create client object
client = SoftLayer.Client(username=apiUsername, api_key=apiKey)

#Check if username and api authentication is working using try except
try:
	userId = client['Account'].getCurrentUser(mask='id')
except SoftLayer.exceptions.SoftLayerAPIError as e:
	print "Incorrect -user or -apikey argument value provided"
	print e
except:
	print "Unexpected error occured"
	sys.exit(3) 


# Fetch id and name of all the servers belonging to user 
serverIds = client['Account'].getHardware(mask='id,fullyQualifiedDomainName')
#print serverIds


if (fqdn == ''): # If no FQDN is passed, operation is applied to all devices under a user
	for each in serverIds:
		try:
			setTag = client['Tag'].setTags(tagName,'HARDWARE',each['id'],'lll')
		except e:
			print e
			print setTag
			print "Unexpected error"
			sys.exit(3)
		if (setTag and tagName == ''): #if tagName is null, then all tags are removed from  the device
			print "\n **** Tags are removed successfully on Device " + each['fullyQualifiedDomainName'] + "  **** \n"
		else:	#if tagName contains a value , then it is added in the device
			print "\n **** Tags are added successfully on Device " + each['fullyQualifiedDomainName'] + " **** \n"
else: # If FQDN is passed, 
	for each in serverIds:
		if (each['fullyQualifiedDomainName'] in fqdn or each['fullyQualifiedDomainName'] == fqdn): #tag is added to required fqdn
			try:
				setTag = client['Tag'].setTags(tagName,'HARDWARE',each['id'],'lll')
			except e:
				print e
				print setTag
				print "Unexpected error"
			if (setTag and tagName == ''):#tag is added to required fqdn
				print "\n **** Tags are removed successfully on Device " + each['fullyQualifiedDomainName'] + "  **** \n"
			else:#tag is removed from device
				print "\n **** Tags are added successfully on Device " + each['fullyQualifiedDomainName'] + " **** \n"








