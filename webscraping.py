import requests
import hashlib
import re
apiUrl = "https://www.jenkins.io/"
filename = "resbody.txt"
output ="checksum.txt"
response = requests.get( apiUrl )
content = response.text
stripped = re.sub('<[^<]+?>', '', content).encode('utf-8') ## remove tags and coleect body content and regex
with open(filename, 'wb') as fd:
    fd.write("".join([s for s in stripped.splitlines(True) if s.strip("\r\n")]))
m = hashlib.md5()
with open(output,'wb') as fd:
    fd.write(m.hexdigest())
