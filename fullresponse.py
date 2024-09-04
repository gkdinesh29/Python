import requests
import hashlib

API_URL = "https://www.jenkins.io/"
FILENAME = "fullresponse.txt"
CHUNK_SIZE = 100
OUTPUT = "fullcheck.txt"

# Download content from the API URL and save it to a file
response = requests.get(API_URL)

with open(FILENAME, 'wb') as fd:
    for chunk in response.iter_content(CHUNK_SIZE):
        fd.write(chunk)

# Compute the MD5 hash of the downloaded file
m = hashlib.md5()
with open(FILENAME, 'rb') as fd:
    for chunk in iter(lambda: fd.read(CHUNK_SIZE), b""):
        m.update(chunk)

# Print the MD5 hash
print("MD5 Hash:", m.hexdigest())

# Write the MD5 hash to an output file
with open(OUTPUT, 'w') as fd:
    fd.write(m.hexdigest())
    
