"""
This module provides functionality to download content from a URL,
compute its MD5 hash, and save both the content and the hash to files.

Dependencies:
- requests: For downloading the content from the URL.
- hashlib: For computing the MD5 hash of the content.

Constants:
- TIMEOUT: Timeout for network requests.
"""

import hashlib  # Standard library import
from dataclasses import dataclass  # Standard library import
import requests  # Third-party import

@dataclass
class Configuration:
    """
    A data class to hold configuration for file processing.

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
    timeout : int
        The timeout duration for network requests.
    """
    url: str
    filename: str
    chunk_size: int
    output: str
    timeout: int

class FileProcessor:
    """
    A class to handle downloading a file from a URL and computing its MD5 hash.

    Attributes
    ----------
    config : Configuration
        Configuration object containing all settings for processing files.
    """

    def __init__(self, config: Configuration):
        """
        Initializes the FileProcessor with a Configuration object.

        Parameters
        ----------
        config : Configuration
            The Configuration object containing all settings for processing files.
        """
        self.config = config

    def download_file(self):
        """
        Downloads content from the URL and saves it to a file.

        Uses the `requests` library to perform the HTTP GET request and save
        the content in chunks to the specified file. A timeout is applied
        to prevent hanging indefinitely.
        """
        try:
            response = requests.get(self.config.url, timeout=self.config.timeout)
            response.raise_for_status()  # Raises HTTPError for bad responses (4xx and 5xx)
            with open(self.config.filename, 'wb') as fd:
                for chunk in response.iter_content(self.config.chunk_size):
                    fd.write(chunk)
        except requests.RequestException as e:
            print(f"An error occurred: {e}")

    def compute_md5_hash(self) -> str:
        """
        Computes the MD5 hash of the content in the file.

        Returns
        -------
        str
            The hexadecimal MD5 hash of the file content.
        """
        m = hashlib.md5()
        with open(self.config.filename, 'rb') as fd:
            for chunk in iter(lambda: fd.read(self.config.chunk_size), b""):
                m.update(chunk)
        return m.hexdigest()

    def save_hash(self):
        """
        Saves the MD5 hash to the output file.

        Writes the computed MD5 hash to the specified output file.
        """
        md5_hash = self.compute_md5_hash()
        with open(self.config.output, 'w', encoding='utf-8') as fd:
            fd.write(md5_hash)
        print("MD5 Hash:", md5_hash)

def main():
    """
    Main function to execute the file download, hash computation, and hash saving.

    Creates an instance of FileProcessor with a Configuration object and performs
    the download, hash computation, and saving of the hash.
    """
    config = Configuration(
        url="https://www.jenkins.io/",
        filename="fullresponse.txt",
        chunk_size=100,
        output="fullcheck.txt",
        timeout=10
    )
    processor = FileProcessor(config)
    processor.download_file()
    processor.save_hash()

if __name__ == "__main__":
    main()
    
