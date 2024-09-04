import requests
import hashlib
apiUrl = "https://www.jenkins.io/"
filename = "fullresponse.txt"
chunk_size = 100
output ="fullcheck.txt"
response = requests.get( apiUrl )

with open(filename, 'wb') as fd:
    for chunk in response.iter_content(chunk_size):
        fd.write(chunk)
m = hashlib.md5()
print(m)
print(m.hexdigest())
with open(output,'wb') as fd:
    fd.write(m.hexdigest())
    
