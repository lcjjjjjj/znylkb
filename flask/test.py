import hashlib
import os

password = "11235813".encode('utf-8')

print(len(hashlib.sha256(password).hexdigest()))
print(hashlib.sha256(password).hexdigest())
print(os.path.join(os.path.abspath("."), "filecache"))