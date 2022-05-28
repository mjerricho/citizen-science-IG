import json
import sys

from modules.CitizenScienceUpload import CitizenScienceUpload

if __name__ == '__main__':
    config = json.load(open(sys.argv[1]))
    csu = CitizenScienceUpload(config, False)
    headers = csu.generate_headers()
    csu.upload_file(sys.argv[2], headers)
