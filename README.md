# citizen-science-ync
This project aims to set up a citizen science platform for the public to upload their videos on animals observation. The data gathered will initially be stored locally, but it can also be automatically stored in a designated cloud storage. In this project, we provide an example of how the data gathered can be stored automatically into Microsoft OneDrive under a Microsoft tenant organisation. Please note that the metadata extraction and Instagram scraping would be applicable to all users, but the automatic cloud storage would differ significantly for each user.

## Package installation
### Setting up virtual environment(optional)
1. Run `python3 -m venv .venv`.
2. Run `source .venv/bin/activate`.

### Installing packages
1. Run `pip install -r requirements.txt`.
   
### installing ffmpeg
The `requirements.txt` install the python wrapper for interacting with ffmpeg but it does not install the source code. To install ffmpeg source code, follow the instructions from https://www.ffmpeg.org/download.html.
1. Download the Source Code.
2. Unzip the file.
3. Execute `./ffmpeg/configure`.
   1. If you are using an Apple product, you might need to open it twice, as ffmpeg is not by an identified developer.

## Instagram data collection
### Setup
1. Create an Instagram account solely for scraping for safety reason.
2. Make sure to export your IG username and password before every session as:
   1. `export IG_USERNAME=<your-IG-usename>`
   2. `export IG_PASSWORD=<your-IG-password`
   3. `CERT_PATH=$(python -m certifi)`
   4. `export SSL_CERT_FILE=${CERT_PATH}`
   5. `export REQUESTS_CA_BUNDLE=${CERT_PATH}`
3. Make sure that the Instagram account that you use works by logging in yourself. Clear all setting configurations and other administration process.

### Project Requirements
1. Make sure that participants post their observation with geotag on.
2. Run the Setup[###Setup] in the command line.
3. Update the `Runner_IG_collection.py` file to either check or download the posts.

### Methodology
1. The `IGDataCollection.py` is well-documented with comments to explain how it works. Do check the implementation for better understanding of the class
2. Initialising the `IGDataCollection` class would require arguments to set how many days worth of observation to check/download form Instagram, the hashtag to look for, and the result directory/path. It initialises the `Instaloader` instance for IG scraping and set the target directory for download.
3. The `scrape_data` method is to scrape IG using the hashtag given in the IGDataCollection initialisation. User also needs to specify the number of posts limit and whether one wants to download the post, given that the post has geodata. It will iterate through each post until the post limit or no more post left to scrape or the user's Keyboard Interrupt. The user can also chooses to:
   1. Download the posts, which be downloaded in the result directory during the initialisation stage.
   2. Save the summary data of the locations, which will be saved under the name `summary.csv` in the result directory.

### Scraping
Run `python3 src/runner_IG_collection.py <hashtag> <number of observation days>`.

### Resources
1. Instaloader: https://instaloader.github.io

## Manual metadata extraction
Given that you already have data of observations, we also have provided the tools for metadata extraction.

### Setup
1. Name the observation files accordingly based on its location of observation.
2. Adapt the ExtractMetadata attribute (`self.abbr_to_geodata`) to the naming convention that you use.
   1. The keys are the abbreviations according to the naming convention.
   2. The values are the (latitude, longitude) in that order.

### Extracting
1. Extracting a single file and print out the result:
   1. Run `python3 src/runner_single_file.py <filepath>`.
2. Extracting a batch of files in a directory:
   1. Run `python3 src/runner_batch_file.py <src_dirpath> <dest_dirpath>`.
3. Extracting a batch of batches of files in a directory:
   1. Run `python3 src/runner_batch_file.py <src_dirpath> <dest_dirpath>`.

### Troubleshooting
Each file format has different metadata structure. If there are errors, the class methods are most likely accessing the wrong values in the dictionary. Hence, you need to tweak the code so that it can access the right information. To do this, we suggest that you:
1. Use `ExtractMetadata.get_metadata_raw` on a single file to see the metadata structure.
2. Update the remaining methods accordingly.
This is going to be a **very common problem**, as we have not tested this program on all the file format.

## Automatic upload to cloud storage
This script complements the citizen science project. After users have uploaded their videos onto Instagram, we will scrape, collect and summarise the videos from Instagram. This script was written to automatically upload the data gathered into Microsoft Teams using the Microsoft Graph API.

### Assumptions
1. Each upload is less than 400mb.
2. The developer has requested permission from the tenant to develop an application and received the necessary information as shown in `config.json`. 

### Set up
1. Duplicate the `config_dummy.json`, name it `config.json`, and fill up the necessary information.
   1. `client_id` and `client_secret` are given by your administrator (institution/organisation).
   2. `tenant_id`, `team_id`, and `channel_id` can be obtained from Teams application by getting the link to the Teams.
   3. `drive_id` and `item_id` can be obtained from these APIS
      1. "https://graph.microsoft.com/v1.0/groups/{ team_id }/drive"
      2. "https://graph.microsoft.com/v1.0/groups/{ team_id }/drive/items/root/children"  

### Running the script
Run `python3 runner_citsci_upload.py <path to config.json> <path to file>`.

### Resources
1. About Microsoft Graph: https://docs.microsoft.com/en-us/graph/overview
2. About Graph Explorer: https://developer.microsoft.com/en-us/graph/graph-explorer
3. About upload sessions: https://docs.microsoft.com/en-us/graph/api/driveitem-createuploadsession?view=graph-rest-1.0
4. Getting response upload sesion: https://stackoverflow.com/questions/60402838/how-to-perform-a-resumable-upload-to-a-sharepoint-site-not-root-subfolder-usin

## Credit
Marcellinus Jerricho (marcellinus.jerricho@u.yale-nus.edu.sg)
Philip John (philip.johns@yale-nus.edu.sg)
Jeremy Osborn (osborn.jeremy@gmail.com)
