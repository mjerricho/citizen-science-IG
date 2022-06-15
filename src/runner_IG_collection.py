import sys

from modules.IGDataCollection import IGDataCollection

if __name__ == '__main__':
    '''
    Scraping the videos with the specified hashtag from Instagram
    and downloading it to result directory in root.
    '''
    if len(sys.argv) < 3:
        print('''
Invalid input: Not enough inputs. USAGE:
python3 src/runner_IG_collection.py <hashtag> <number of observation days>.
''')
        sys.exit(1)
    hashtag = sys.argv[1]
    try:
        num_days_collect = int(sys.argv[2])
    except ValueError:
        print('''
Invalid input: The last input must be integer.
''')
    IGDC = IGDataCollection(hashtag=hashtag, num_days_collect=num_days_collect)
    IGDC.scrape_data(10, download=True, save_md=True)
