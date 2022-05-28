import csv
import os
import sys

from modules.ExtractMetadata import ExtractMetadata


class BatchRunner:
    def __init__(self, debug=False) -> None:
        '''
        Initialise a class that will extract the metadata from files
        in a directory.
        '''
        self.debug = debug
        if self.debug:
            print(f'{sys.argv[0]} started.')
        self.dest_path = sys.argv[2]
        self.files = []
        self.metadatas = []
        self.extract_metadata = ExtractMetadata()

    def run(self, src_path=sys.argv[1]):
        '''
        run through the files in the directory and collect all the metadatas
        input:
            src_path<string>: the source directory
        '''
        self.src_path = src_path
        self.src_name = self.src_path.split(sep="/")[-1]
        # Add more video format if necessary
        for file in os.listdir(self.src_path):
            if file.endswith(('.MOV', '.mp4', '.MP4', 'mov')):
                if self.debug:
                    print(f'{file} added.')
                self.files.append(file)

        for file in self.files:
            if self.debug:
                print(f"Looking at {file}.")
            try:
                metadata_raw = self.extract_metadata\
                                   .get_metadata_raw(f"{self.src_path}/{file}")
                self.metadatas\
                    .append(self.extract_metadata
                                .get_metadata_processed(metadata_raw))
            except Exception:
                print(f"{file} extraction failed.")
                continue

    def write_file(self):
        '''
        write the metadatas collected into a csv file in the
        destination directory.
        '''
        filename = f'{self.dest_path}/{self.src_name}.csv'
        with open(filename, 'w',
                  newline='') as f:
            writer = csv.DictWriter(f,
                                    fieldnames=self.extract_metadata.metadata)
            writer.writeheader()
            writer.writerows(self.metadatas)
        if self.debug:
            print(f'{sys.argv[0]} finished.')
        print(f'file saved as {filename}.')


if __name__ == '__main__':
    '''
    This script will run through a folder of videos and extract all the
    self.metadatas specified in ExtractMetadata
    '''
    if len(sys.argv) < 3:
        print('''
USAGE: python3 src/runner_batch_files.py <src_dirpath> <dest_dirpath>''')
        sys.exit(1)
    runner = BatchRunner()
    runner.run()
    runner.write_file()
