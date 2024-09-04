"""
This module downloads content from a specified URL, computes its MD5 hash,
and saves both the content and the hash to files.

Dependencies:
- requests: For downloading the content from the URL.
- hashlib: For computing the MD5 hash of the content.

Constants:
- API_URL: URL from which to download the content.
- FILENAME: File where the downloaded content will be saved.
- CHUNK_SIZE: Size of the chunks to read from the response.
- OUTPUT: File where the MD5 hash of the content will be saved.
"""

import requests
import hashlib

API_URL = "https://www.jenkins.io/"
FILENAME = "fullresponse.txt"
CHUNK_SIZE = 100
OUTPUT = "fullcheck.txt"

def download_file(url, filename, chunk_size):
    """
    Downloads content from a URL and saves it to a file.

    Parameters:
    url (str): The URL to download content from.
    filename (str): The path to the file where the content will be saved.
    chunk_size (int): The size of chunks to read from the response.
    """
    response = requests.get(url)
    with open(filename, 'wb') as fd:
        for chunk in response.iter_content(chunk_size):
            fd.write(chunk)

def compute_md5_hash(filename, chunk_size):
    """
    Computes the MD5 hash of the content in a file.

    Parameters:
    filename (str): The path to the file whose MD5 hash is to be computed.
    chunk_size (int): The size of chunks to read from the file.

    Returns:
    str: The hexadecimal MD5 hash of the file content.
    """
    m = hashlib.md5()
    with open(filename, 'rb') as fd:
        for chunk in iter(lambda: fd.read(chunk_size), b""):
            m.update(chunk)
    return m.hexdigest()

def main():
    """
    Main function to download content, compute its MD5 hash, and save the hash to a file.
    """
    download_file(API_URL, FILENAME, CHUNK_SIZE)
    md5_hash = compute_md5_hash(FILENAME, CHUNK_SIZE)
    print("MD5 Hash:", md5_hash)
    with open(OUTPUT, 'w') as fd:
        fd.write(md5_hash)

if __name__ == "__main__":
    main()
