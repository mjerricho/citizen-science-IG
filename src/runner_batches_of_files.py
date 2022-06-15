import os
import sys

from runner_batch_files import BatchRunner


class BatchesRunner:
    def __init__(self, src_path, dest_path, debug=False) -> None:
        self.debug = debug
        if self.debug:
            print('BatchesRunner started.')
        if not os.path.exists(src_path):
            raise Exception(f'Source {src_path} directory not found.')
        self.src_path = src_path
        if not os.path.exists(dest_path):
            os.mkdir(dest_path)
        self.dest_path = dest_path

    def run(self):
        for dir in os.listdir(self.src_path):
            batch_src_path = f'{self.src_path}/{dir}'
            if os.path.isdir(batch_src_path):
                if self.debug:
                    print(f'Looking at directory {dir}')
                self.BatchRunner = BatchRunner(batch_src_path, self.dest_path)
                if self.debug:
                    print(f'Running on source: {batch_src_path}')
                self.BatchRunner.run()
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
Invalid input: Not enough arguments.
USAGE: python3 src/runner_batches_file.py <src_dirpath> <dest_dirpath>''')
        sys.exit(1)
    src_path = sys.argv[1]
    dest_path = sys.argv[2]
    runner = BatchesRunner(src_path, dest_path, debug=False)
    runner.run()
