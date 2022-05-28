import json
import sys
import os

from modules.CitizenScienceUpload import CitizenScienceUpload

if __name__ == '__main__':
    config = json.load(open(sys.argv[1]))
    csu = CitizenScienceUpload(config, False)
    headers = csu.generate_headers()
    rel_file_path = sys.argv[2]
    if not os.path.exists(rel_file_path):
        raise Exception(f'Source {rel_file_path} not found.')
    csu.upload_file(rel_file_path, headers)
