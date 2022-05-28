import os
import sys

from runner_batch_files import BatchRunner


class BatchesRunner:
    def __init__(self, debug=False) -> None:
        self.debug = debug
        if self.debug:
            print(f'{sys.argv[0]} started.')

    def run(self, src_dir_path=sys.argv[1]):
        self.src_dir_path = src_dir_path
        for dir in os.listdir(self.src_dir_path):
            self.BatchRunner = BatchRunner()
            if self.debug:
                print(f'Looking at directory {dir}')
            batch_src_path = f'{self.src_dir_path}/{dir}'
            if self.debug:
                print(f'Running on path: {batch_src_path}')
            self.BatchRunner.run(batch_src_path)
            self.BatchRunner.write_file()
        if self.debug:
            print(f'{sys.argv[0]} Done.')


if __name__ == '__main__':
    '''
    Run through the files in the directory and collect all the metadatas.
    This script will run through the batches of videos and run
    BatchRunner on each batch.
    '''
    if len(sys.argv) < 3:
        print('''
USAGE: python3 src/runner_batches_file.py <src_dirpath> <dest_dirpath>''')
        sys.exit(1)
    runner = BatchesRunner()
    runner.run()
