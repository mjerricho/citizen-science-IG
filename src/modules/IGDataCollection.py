import csv
import os
from datetime import datetime, timedelta
from pprint import pprint

import instaloader


class IGDataCollection:
    def __init__(self, num_days_collect=1,
                 hashtag="sgotterproject",
                 result_dir="result",
                 debug=False) -> None:
        '''
        Make sure to read the README.md and carry out the set up instructions
        before using this class. This class collects the useful information
        from environment to use the instaloader API.

        The downloaded posts can be found at
        {result_dir}/{hashtag}/{today's date}.

        By default, the class collects data from yesterday to today and store
        it in the "result" directory.

        Input:
            num_days_collect<int>:
                The number of days (including today) to observe/record.
            hashtag<str>: The hashtag that filter the posts search.
            result_dir<str>: The directory to keep downloaded posts.
        '''
        self.debug = debug
        self.until = datetime.today()
        self.since = self.until - timedelta(days=num_days_collect)
        self.today = self.until.strftime("%d_%m_%Y")
        self.hashtag = hashtag
        self.download_target = f"{result_dir}/{self.hashtag}/{self.today}"
        fp = "{date_utc}_UTC_{profile}"
        self.L = instaloader.Instaloader(dirname_pattern=self.download_target,
                                         filename_pattern=fp,
                                         download_videos=True,
                                         download_video_thumbnails=False,
                                         download_comments=False)

        self.IG_username = os.environ.get('IG_USERNAME')
        self.IG_password = os.environ.get('IG_PASSWORD')
        if self.debug:
            print("Logging in.")
        self.L.login(self.IG_username, self.IG_password)
        if self.debug:
            print("Login success.")

    def fbo(self, variable):
        '''
        This method is used a fallback operation for inputting the variable
        of the post into dictionary in scrape_data.
        '''
        try:
            if variable:
                return variable
        except NameError:
            return None

    def scrape_data(self, max_num=10, download=True, save_md=False):
        '''
        Given the hashtag in the initialisation process, this
        function scrapes the instagram posts with that hashtag.
        The user must specify whether they want download the data
        and save the metadata summary.

        NOTE: Feel free to edit the metadatas to be saved in this method.
        The post properties can be found here:
        https://instaloader.github.io/module/structures.html#posts

        input:
            max_num<int>: Maximum number of posts to observe
            download<bool>: Enable downloading the post into result
            save_md<bool>: Enable saving the summary of the posts with location
        '''
        if self.debug:
            print("scrape_data called.")
        self.L_hashtag = instaloader.Hashtag.from_name(self.L.context,
                                                       self.hashtag)
        print(f"Looking for posts with hashtag: {self.hashtag}")
        print(f"Directory download target: {self.download_target}.")
        print("REMINDER: Press ctrl+c to stop scraping process early.")
        print("If the user chose to save the metadata in the argument,",
              "the program will save the metadata automatically after",
              "interrupted.")
        num = 1
        mds = []
        try:
            for post in self.L_hashtag.get_posts_resumable():
                if ((post.date > self.since and post.date < self.until)
                   and post.location):
                    print(f"Checking post #{str(num)}")
                    if self.debug:
                        print(f'''
Location found in post #{str(num)}.
ID: {post.location.id} | lat: {post.location.lat} | long: {post.location.lng}
''')
                    format = "%Y-%m-%d_%H-%M-%S"
                    postDate = post.date_utc.strftime(format)
                    postID = f"{postDate}_UTC_{post.profile}"
                    mds.append({"postID": self.fbo(postID),
                                "postDate": self.fbo(postDate),
                                "locationID": self.fbo(post.location.id),
                                "latitude": self.fbo(post.location.lat),
                                "longitude": self.fbo(post.location.lng),
                                "locationName": self.fbo(post.location.name),
                                "locationURL": self.fbo(post.location.slug),
                                "shortcode": self.fbo(post.shortcode),
                                "mediaURL": self.fbo(post.url),
                                "isVideo": self.fbo(post.is_video),
                                "videoDuration": self.fbo(post.video_duration),
                                "hashtag": self.fbo(self.hashtag),
                                "caption": self.fbo(post.caption),
                                "captionHashtags": self.fbo(post.caption_hashtags)})
                    if download:
                        self.L.download_post(post, target="#hashtag")
                        print(f'''\
Post #{str(num)} with Post ID: {postID} downloaded.
''')
                num += 1
                if num > max_num:
                    break
        except KeyboardInterrupt:
            pass
        if self.debug:
            print("Metadata:")
            for md in mds:
                pprint(md)
        if save_md:
            try:
                cols = mds[0].keys()
                with open(f"{self.download_target}/{self.today}_summary.csv",
                          "w", newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=cols)
                    writer.writeheader()
                    writer.writerows(mds)
                print("SAVED: Metadata saved as",
                      f"{self.download_target}/summary.csv.")
            except IndexError:
                print("ERROR: No posts found, so no metada saved.")
