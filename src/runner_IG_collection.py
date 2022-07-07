import sys
import os
import json

from modules.IGDataCollection import IGDataCollection

if __name__ == '__main__':
    '''
    Scraping the videos with the specified hashtag from Instagram
    and downloading it to result directory in root.
    '''
    if len(sys.argv) < 5:
        print('''
Invalid input: Not enough inputs. USAGE:
python3 src/runner_IG_collection.py <hashtag> <number of observation days> <maximum number of posts to look at> <directory to store results> <path to config file>.
''')
        sys.exit(1)
    hashtag = sys.argv[1]
    try:
        num_days_collect = int(sys.argv[2])
    except ValueError:
        print('''
Invalid input: The number of observation days must be integer.
''')
    result_dir = sys.argv[4]
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    config_path = sys.argv[5]
    if not os.path.exists(config_path):
        raise Exception("Config file does not exist.")
    with open(config_path) as config_file:
        config_data = json.load(config_file)
    IGDC = IGDataCollection(username=config_data['username'], password=config_data['password'], hashtag=hashtag, num_days_collect=num_days_collect, result_dir=result_dir)
    max_num_observation = sys.argv[3]
    IGDC.scrape_data(max_num_observation, download=True, save_md=True)
