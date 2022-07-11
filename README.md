# citizen-science-IG
This project aims to build a Citizen Science methodology for researchers and data collectors to efficiently and quickly gather photo and video observations of a certain subject. We will be using Instagram as the main platform for data collection due to its popularity and accessibility among users and robust scraper tool for developers. For the case where you already have a repository of data, we also provide a metadata extractor tool to quickly summarise important information. Once you have acquired the observations and metadata needed, we provide an example of how the data gathered can be stored automatically into Microsoft OneDrive under a Microsoft tenant organisation.

Please note that the Instagram scraping and metadata extractor tool would be applicable to all users, but the automatic cloud storage would differ significantly for each user. It is advisable to consult your organisation IT team before you start uploading data into cloud storage. This document will be structured according to the following:
1. [Package Installation](#package-installation)
2. [Instagram data collection](#instagram-data-collection) 
3. [Manual metadata extraction](#manual-metadata-extraction)
4. [Automatic upload to cloud storage](#automatic-upload-to-cloud-storage)
5. [Credits](#credit)
   
## Package installation
The required python packages are included in [requirements.txt](requirements.txt). Please make sure that you carry out the instructions correctly.
### Setting up virtual environment(optional)
1. Run `python3 -m venv .venv`.
2. Run `source .venv/bin/activate` to activate the virtual environment. This command needs to be run **before every session**.

### Installing packages
1. Run `pip install -r requirements.txt`.
   
### Installing ffmpeg
The `requirements.txt` install the python wrapper for interacting with ffmpeg but it does not install the source code. To install ffmpeg source code, follow the instructions from https://www.ffmpeg.org/download.html. `ffmpeg` is used to extract metadata from existing repository.
1. Download the Source Code.
2. Unzip the file.
3. Execute `./ffmpeg/configure`. If you are using an Apple product, you might need to open it twice, as ffmpeg is not by an identified developer.
4. Check if you have `ffmpeg` installed by running `ffmpeg` in the command line. It should return a text along this line: `ffmpeg version N-105288-g45e45a6060 Copyright (c) 2000-2022 the FFmpeg developers`.

## Instagram data collection
The [Instagram Data Collection](src/modules/IGScrape.py) is a fast, effective, and low-cost solution for crowdsourcing more observations and raising awareness on a certain subject through social media. As a data collector, you have to [setup](#setup) the program and make sure that participants are aware of the participation [requirements](#requirements). As a participant, you have to **post** the observation with the **necessary hashtags** on a **public account**.
### Setup
1. Create a new dispensable Instagram account solely for scraping for safety reasons. It is also advisable that you create a new dispensable email account for this project for the sign up process.
2. [Required if you want to uses the Command Line] Duplicate the `config_ig_to_duplicate.json` as `config_ig.json` and fill it up with the necessary information.
3. Make sure that the Instagram account that you use works by logging in yourself. Clear all setting configurations and other administration process.

### Requirements
1. Make sure that participants post their observation with geotag on.
2. Run the [Setup](###Setup) in the command line.
3. Update the `Runner_IG_scrape.py` file to either check or download the posts.

### Methodology
1. The `IGScrape.py` is well-documented with comments to explain how it works. Do check the implementation for better understanding of the class
2. Initialising the `IGScrape` class would require arguments to set how many days worth of observation to check/download form Instagram, the hashtag to look for, and the result directory/path. It initialises the `Instaloader` instance for IG scraping and set the target directory for download.
3. The `scrape_data` method is to scrape IG using the hashtag given in the IGScrape initialisation. User also needs to specify the number of posts limit and whether one wants to download the post, given that the post has geodata. It will iterate through each post until the post limit or no more post left to scrape or the user's Keyboard Interrupt. The user can also chooses to:
   1. Download the posts, which be downloaded in the result directory during the initialisation stage.
   2. Save the summary data of the locations, which will be saved under the name `summary.csv` in the result directory.

### Scraping
If you choose to use the [command line](src/runner_IG_scrape.py), run `python3 src/runner_IG_scrape.py <hashtag> <number of observation days> <maximum number of posts to look at> <directory to store results> <path to config file>`.

If you prefer to use the [GUI](scrape_gui.py), run `python3 scrape_gui.py`.

### Limitations
1. Instaloader is an open-source library, so there might be occassions when the module would stop working due to changes in Instagram API or permissioning. In our testing case, there were times when the program would fail its scraping process due to unexpected reasons but only to work again after a couple of days. If you find a bug or have an idea for improvement, please report it to [Instaloader issues Github page](https://github.com/instaloader/instaloader/issues). Make sure that you comply to the reporting guidelines.
2. The data gathered is per Instagram post instead of per video in the post.

### Alternative Solution
You can also choose to work directly with [Instagram API](https://developers.facebook.com/docs/instagram), which would require you to set up a Business or Creator account under [Instagram Professionals](https://help.instagram.com/502981923235522) and an approved app. However, since our main focus of this project was to show a new method that makes Citizen Science more accessible and appealing to the masses, we decided to use Instaloader to skip the permissioning process. Using the [Instagram API](https://developers.facebook.com/docs/instagram) would require us to create a fully functioning app that complies with Instagram's image and guidelines.

We recognise that there is a lot of layers involved if we want to use Instagram API, such as creating a business account and registering the app. It also requires the user to be present to authenticate the account for scraping, which adds friction to the scraping process.

### Resources
1. Instaloader: https://instaloader.github.io
2. Common errors: https://instaloader.github.io/troubleshooting.html
3. Reporting issues: https://github.com/instaloader/instaloader/issues
4. Instagram API: https://developers.facebook.com/docs/instagram
5. Getting access tokens to use Instagram API: https://www.youtube.com/watch?v=dEDKOcPuXlU&ab_channel=JustinStolpe
6. Examples of using the Instagram Graph API: https://github.com/jstolpe/blog_code/tree/master/instagram_graph_api

## Manual metadata extraction
Given that you already have data of observations, we also have provided the tools for metadata extraction.

### Setup
1. Name the observation files accordingly based on its location of observation.
2. Adapt the ExtractMetadata attribute (`self.abbr_to_geodata`) to the naming convention that you use. Please note that the `region` column in the metadata extracted is tied to the abbreviations and corresponding geodata used.
   1. The keys are the abbreviations according to the naming convention.
   2. The values are the (latitude, longitude) in that order.
3. To change the metadata to be extracted:
   1. Check if the metadata desired is within the metadata by using the `runner_single_file.py`.
   2. Edit the enumerated metadata (`Md`) at the top of `ExtractMetadata.py`.
   3. Get the metadata desired in `get_metadata_processed`, set it as value to the enumerated metadata defined, and return it as a dictionary.
4. The video formats accomodated for the `runner_batch_files.py` are rather limited. Edit if necessary.

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
Run `python3 runner_citsci_upload.py <path to config.json> <path_to_folder_to_upload>`.

### Resources
1. About Microsoft Graph: https://docs.microsoft.com/en-us/graph/overview
2. About Graph Explorer: https://developer.microsoft.com/en-us/graph/graph-explorer
3. About upload sessions: https://docs.microsoft.com/en-us/graph/api/driveitem-createuploadsession?view=graph-rest-1.0
4. Getting response upload sesion: https://stackoverflow.com/questions/60402838/how-to-perform-a-resumable-upload-to-a-sharepoint-site-not-root-subfolder-usin
5. About permission names: https://docs.microsoft.com/en-us/graph/permissions-reference
6. Constraints on username and password flow: https://github.com/AzureAD/microsoft-authentication-library-for-python/wiki/Username-Password-Authentication

## Automating task
Scraping is repetitive task that can be automated. The current [runner file](src/runner_IG_scrape.py) is designed to scrape resources from 7 days ago on default, so you can choose to build a program that runs the script weekly. Please refer to these resources and adjust accordingly.
1. For windows user: https://towardsdatascience.com/automate-your-python-scripts-with-task-scheduler-661d0a40b279
2. For MacOS or Linus user: https://betterprogramming.pub/https-medium-com-ratik96-scheduling-jobs-with-crontab-on-macos-add5a8b26c30
   1. To help with setting up Cron: https://crontab.guru/#0_0_\*_*_1

## Credit
- Marcellinus Jerricho (marcellinus.jerricho@u.yale-nus.edu.sg)
- Philip Johns (philip.johns@yale-nus.edu.sg)
- Jeremy Osborn (osborn.jeremy@gmail.com)
- Anand Kumar (anandkumar@u.yale-nus.edu.sg)
