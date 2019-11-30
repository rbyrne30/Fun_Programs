import requests
import hashlib
from bs4 import BeautifulSoup
import sys

class Pwned(object):
    def __init__(self):
        self.api = "https://api.pwnedpasswords.com/range/"

    def check_password(self, password):
        """Checks whether a password has been pwned."""
        hashed = self.hash_sha1(password)
        prefix = hashed[:5]
        suffix = hashed[5:]
        hashes = self.list_hashes(prefix)
        parsed = self.parse_list_hashes(hashes)
        return parsed[suffix] if suffix in parsed else 0

    def hash_sha1(self, password):
        """Hashes a password with sha1 algorithm."""
        return hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

    def list_hashes(self, prefix):
        """Gets the list of hashes"""
        return BeautifulSoup(requests.get(self.api + prefix).content, 'html.parser').text

    def parse_list_hashes(self, content):
        """Returns a dictionary of prefix-suffix pairs from api content."""
        D = {}
        lines = content.split("\n")
        for line in lines:
            segs = line.strip().split(":")
            D[segs[0]] = segs[1]
        return D


if __name__ == "__main__":
    args = sys.argv

    if len(args) != 2:
        print("Invalid number of arguments :", sys.argv[0], "<password>")
        exit()

    password = args[1]
    p = Pwned()
    occurences = p.check_password(password)
    if occurences > 0:
        print("Password has been pwned! %d occurences." %occurences)
    else:
        print("Password has not been pwned.")
