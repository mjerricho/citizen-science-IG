import sys

from modules.ExtractMetadata import ExtractMetadata

if __name__ == '__main__':
    '''
    Get the metadata of a single file.
    '''
    if len(sys.argv) < 2:
        print('''
Invalid input: Not enough arguments.
USAGE: python3 src/runner_single_file.py <filepath>''')
        sys.exit(1)
    print(f'{sys.argv[0]} started.')
    media_file = sys.argv[1]
    extract_metadata = ExtractMetadata(debug=False)
    metadata_raw = extract_metadata.get_metadata_raw(media_file)
    metadata_processed = extract_metadata.get_metadata_processed(metadata_raw)
    extract_metadata.print_metadata(metadata_processed)
    print(f'{sys.argv[0]} finished.')
