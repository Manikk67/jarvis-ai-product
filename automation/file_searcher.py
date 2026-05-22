import os

# ==========================================
# SEARCH FILES
# ==========================================

def search_files(filename, search_path="C:\\"):

    matches = []

    for root, dirs, files in os.walk(search_path):

        for file in files:

            if filename.lower() in file.lower():

                full_path = os.path.join(root, file)

                matches.append(full_path)

    return matches