#https://stemgeeks.net/hive-163521/@makerhacks/ipfs-in-python
#https://github.com/Vourhey/pinatapy
import os
import requests
from pinatapy import PinataPy
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

# Connect to the IPFS cloud service
pinata_api_key=str(os.environ.get('API_KEY'))
pinata_secret_api_key=str(os.environ.get('API_SECRET'))
pinata = PinataPy(pinata_api_key,pinata_secret_api_key)

def uploadFile(pathToFile):
    # Upload the file
    result = pinata.pin_file_to_ipfs(pathToFile)

    # Should return the CID (unique identifier) of the file
    print(result)
    return result

# Anything waiting to be done?
def jobsWaiting():
    print(pinata.pin_jobs())

# List of items we have pinned so far
def uploadedDataSets():
    print(pinata.pin_list())

# Total data in use
def totalData():
    print(pinata.user_pinned_data_total())

# Get our pinned item
def getDataSet(result):
    gateway="https://gateway.pinata.cloud/ipfs/"
    #gateway="https://ipfs.io/ipfs/"
    print(requests.get(url=gateway+result['IpfsHash']).text)
    print(gateway+result['IpfsHash'])

result = uploadFile(".\Backend\IPFS\dataset.json")
getDataSet(result)