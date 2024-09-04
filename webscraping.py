"""
This script fetches HTML content from a URL, removes the HTML tags,
saves the clean text to a file, and then calculates and stores its MD5 checksum.
"""

import re
import hashlib
import requests

API_URL = "https://www.jenkins.io/"
FILENAME = "resbody.txt"
OUTPUT = "checksum.txt"
TIMEOUT = 10  # Timeout for the request in seconds

# Fetch content from the URL with a timeout
response = requests.get(API_URL, timeout=TIMEOUT)
content = response.text

# Remove HTML tags
stripped = re.sub('<[^<]+?>', '', content)

# Write stripped content to the file
with open(FILENAME, 'w', encoding='utf-8') as fd:
    fd.write("".join(
        [s for s in stripped.splitlines(True) if s.strip("\r\n")]
    ))

# Calculate the MD5 checksum
m = hashlib.md5()
with open(FILENAME, 'rb') as fd:
    m.update(fd.read())

# Write the checksum to the output file
with open(OUTPUT, 'w') as fd:
    fd.write(m.hexdigest())
