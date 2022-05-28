import csv
import os
import sys

from modules.ExtractMetadata import ExtractMetadata


class BatchRunner:
    def __init__(self, src_path, dest_path, debug=False) -> None:
        '''
        Initialise a class that will extract the metadata from files
        in a directory.
        '''
        self.debug = debug
        if self.debug:
            print('BatchRunner started.')
        if not os.path.exists(src_path):
            raise Exception(f'Source {src_path} directory not found.')
        self.src_path = src_path
        if not os.path.exists(dest_path):
            os.mkdir(dest_path)
        self.dest_path = dest_path
        self.files = []
        self.metadatas = []
        self.EM = ExtractMetadata(debug=False)

    def run(self):
        '''
        run through the files in the directory and collect all the metadatas.
        '''
        self.src_name = os.path.basename(self.src_path)
        # Add more video format if necessary
        for file in os.listdir(self.src_path):
            if file.endswith(('.MOV', '.mp4', '.MP4', 'mov')):
                if self.debug:
                    print(f"Looking at {file}.")
                try:
                    file_path = f"{self.src_path}/{file}"
                    metadata_raw = self.EM.get_metadata_raw(file_path)
                    self.metadatas\
                        .append(self.EM.get_metadata_processed(metadata_raw))
                except Exception:
                    print(f"{file_path} extraction failed.")
                    continue

    def write_file(self):
        '''
        write the metadatas collected into a csv file in the
        destination directory.
        '''
        filename = f'{self.dest_path}/{self.src_name}.csv'
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.EM.metadata)
            writer.writeheader()
            writer.writerows(self.metadatas)
        print(f'File saved as {filename}.')


if __name__ == '__main__':
    '''
    This script will run through a folder of videos and extract all the
    self.metadatas specified in ExtractMetadata
    '''
    if len(sys.argv) < 3:
        print('''
Invalid input: Not enough arguments.
USAGE: python3 src/runner_batch_files.py <src_dirpath> <dest_dirpath>''')
        sys.exit(1)
    src_path = sys.argv[1]
    dest_path = sys.argv[2]
    runner = BatchRunner(src_path, dest_path, debug=False)
    runner.run()
    runner.write_file()
