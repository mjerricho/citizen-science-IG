import json
import sys
import os

from modules.CitizenScienceUpload import CitizenScienceUpload

if __name__ == '__main__':
    '''
    This runner will zip the designated folder and upload it to Teams.
    '''
    if len(sys.argv) < 3:
        print('''
Invalid input: Not enough inputs. USAGE:
python3 src/runner_citsci_upload.py <path_to_config> <path_to_folder_to_upload>
''')
    config = json.load(open(sys.argv[1]))
    csu = CitizenScienceUpload(config, False)
    headers = csu.generate_headers()
    rel_dir_path = sys.argv[2]
    if not os.path.exists(rel_dir_path):
        raise Exception(f'Source {rel_dir_path} not found.')
    csu.zip_dir(rel_dir_path, rel_dir_path)
    csu.upload_file(f'{rel_dir_path}.zip', headers)
