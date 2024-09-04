import requests
import hashlib

apiUrl = "https://www.jenkins.io/"
filename = "fullresponse.txt"
chunk_size = 100
output = "fullcheck.txt"

# Download content from the API URL and save it to a file
response = requests.get(apiUrl)

with open(filename, 'wb') as fd:
    for chunk in response.iter_content(chunk_size):
        fd.write(chunk)

# Compute the MD5 hash of the downloaded file
m = hashlib.md5()
with open(filename, 'rb') as fd:
    for chunk in iter(lambda: fd.read(chunk_size), b""):
        m.update(chunk)

# Print the MD5 hash
print("MD5 Hash:", m.hexdigest())

# Write the MD5 hash to an output file
with open(output, 'w') as fd:
    fd.write(m.hexdigest())

    
