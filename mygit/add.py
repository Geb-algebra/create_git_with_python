import os
import hashlib
import glob
from util import *


# file_names = ["test/file_in_test.txt"]
file_names = glob.glob("**/*.txt", recursive=True)
print(file_names)
file_hash = {}
for file_name in file_names:
    text = read_file(file_name)
    hash = generate_hash(text)

    save_file(hash, text)
    file_hash[file_name] = hash

save_index(file_hash)
