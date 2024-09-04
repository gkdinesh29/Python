"""
This module provides functionality to download content from a URL,
compute its MD5 hash, and save both the content and the hash to files.

Dependencies:
- requests: For downloading the content from the URL.
- hashlib: For computing the MD5 hash of the content.

Constants:
- API_URL: URL from which to download the content.
- FILENAME: File where the downloaded content will be saved.
- CHUNK_SIZE: Size of the chunks to read from the response.
- OUTPUT: File where the MD5 hash of the content will be saved.
"""

import hashlib  # Standard library import
import requests  # Third-party import

API_URL = "https://www.jenkins.io/"
FILENAME = "fullresponse.txt"
CHUNK_SIZE = 100
OUTPUT = "fullcheck.txt"

class FileProcessor:
    """
    A class to handle downloading a file from a URL and computing its MD5 hash.

    Attributes
    ----------
    url : str
        The URL to download content from.
    filename : str
        The path to the file where the content will be saved.
    chunk_size : int
        The size of chunks to read from the response and file.
    output : str
        The path to the file where the MD5 hash will be saved.
    """

    def __init__(self, url, filename, chunk_size, output):
        """
        Initializes the FileProcessor with URL, filenames, chunk size, and output file.

        Parameters
        ----------
        url : str
            The URL to download content from.
        filename : str
            The path to the file where the content will be saved.
        chunk_size : int
            The size of chunks to read from the response and file.
        output : str
            The path to the file where the MD5 hash will be saved.
        """
        self.url = url
        self.filename = filename
        self.chunk_size = chunk_size
        self.output = output

    def download_file(self):
        """
        Downloads content from the URL and saves it to a file.

        Uses the `requests` library to perform the HTTP GET request and save
        the content in chunks to the specified file.
        """
        response = requests.get(self.url)
        with open(self.filename, 'wb') as fd:
            for chunk in response.iter_content(self.chunk_size):
                fd.write(chunk)

    def compute_md5_hash(self):
        """
        Computes the MD5 hash of the content in the file.

        Parameters
        ----------
        filename : str
            The path to the file whose MD5 hash is to be computed.
        chunk_size : int
            The size of chunks to read from the file.

        Returns
        -------
        str
            The hexadecimal MD5 hash of the file content.
        """
        m = hashlib.md5()
        with open(self.filename, 'rb') as fd:
            for chunk in iter(lambda: fd.read(self.chunk_size), b""):
                m.update(chunk)
        return m.hexdigest()

    def save_hash(self):
        """
        Saves the MD5 hash to the output file.

        Writes the computed MD5 hash to the specified output file.
        """
        md5_hash = self.compute_md5_hash()
        with open(self.output, 'w', encoding='utf-8') as fd:
            fd.write(md5_hash)
        print("MD5 Hash:", md5_hash)

def main():
    """
    Main function to execute the file download, hash computation, and hash saving.

    Creates an instance of FileProcessor and performs the download, hash
    computation, and saving of the hash.
    """
    processor = FileProcessor(API_URL, FILENAME, CHUNK_SIZE, OUTPUT)
    processor.download_file()
    processor.save_hash()

if __name__ == "__main__":
    main()
