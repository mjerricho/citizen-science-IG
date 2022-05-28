import os
from pprint import pprint

import ffmpeg
import numpy as np
import regex as re


class ExtractMetadata:
    def __init__(self, debug=False) -> None:
        '''
        Initialise a class that contains the dictionary that maps the
        abbreviations to the geodata (latitude, longitude).
        The locations include:
            Ulu Pandan (UP)
            Jurong Lake (JLG)
            Singapore Botanical Gardens (SBG)
            Singapore River (SR)
            Pasir Ris (PR)
            Sungei Bulog (SB)
            Punggol
        Also, initialise an empty list to store all the metadata.
        '''
        self.debug = debug
        self.abbr_to_geodata = {
            "UP": np.array([1.3334, 103.7602]),
            "Pandan": np.array([1.3334, 103.7602]),
            "JLG": np.array([1.3418, 103.7282]),
            "SBG": np.array([1.3138, 103.8159]),
            "SR": np.array([1.2874, 103.8460]),
            "PR": np.array([1.3721, 103.9474]),
            "SB": np.array([1.4480, 103.7245]),
            "Punggol": np.array([1.3984, 103.9072]),
            "PRP": np.array([1.3984, 103.9072])
        }
        self.metadata = ("filepath", "creation_datetime", "latitude",
                         "longitude", "source", "region", "duration",
                         "res_width", "res_height")
        if self.debug:
            print("Extracting metadata initialised.")

    def get_metadata_raw(self, media_file: str) -> dict:
        '''
        Return the complete metadata from the video file.
        input:
            The path to the video of any format (.MOV, mp4).
        output:
            Dictionary of the metadata.
        '''
        if not os.path.exists(media_file):
            raise Exception(f'{media_file} not found.')
        return ffmpeg.probe(media_file)

    def get_creation_time(self, metadata: dict) -> str:
        '''
        Extract the creation time from the tags.
        input:
            raw metadata from get_raw_metadata <dict>
        output:
            String of date and time in the format YYYY-MM-DDThh:mm:ssTZD.
        '''
        return metadata['format']['tags'].get('creation_time', None)

    def get_closest_region(self, latitude: float, longitude: float) -> str:
        '''
        Get the region of the observation based on its geodata.
        input:
            latitude<float>
            longitude<float>
        output:
            region<str> based on the defined regions in self.abbr_to_geodata
        '''
        region = None
        abs_diff_geodata = None
        obs_geodata = np.array([latitude, longitude])
        for region_abbr in self.abbr_to_geodata.keys():
            diff = np.sum(np.abs(self.abbr_to_geodata[region_abbr] -
                                 obs_geodata))
            if abs_diff_geodata is None or diff < abs_diff_geodata:
                region = region_abbr
                abs_diff_geodata = diff
        return region

    def ret_float(self, value: str) -> float:
        return re.sub("[^0-9.]", "", value)

    def get_geodata(self, metadata: dict) -> "tuple[float, float, str]":
        '''
        Extract the location of the video from the tags, if any.
        The method checks if the video is taken from an Apple product.
        If not, then look at the file name and compare to abbreviations.
        The data "geodata_src" is either "extracted" or "derived".
        input:
            raw metadata from get_raw_metadata <dict>
        output:
            Tuple of the (latitude <float>, longitude<float>,
                          geodata_src<str>, region<str>).
            Return (None, None, None, None) if location is not found.
        '''
        metadata_format = metadata['format']
        # Video is taken from an Apple product with geotag
        if metadata_format['filename'][-4:] == ".MOV":
            location = metadata_format['tags']\
                .get("com.apple.quicktime.location.ISO6709", None)
            if location is not None:
                if self.debug:
                    print("splitting location")
                    print(location)
                location_split = location.split("+")
                if self.debug:
                    print(str(location_split))
                try:
                    latitude = float(self.ret_float(location_split[1]))
                    longitude = float(self.ret_float(location_split[2]))
                    region = self.get_closest_region(latitude, longitude)
                    return (latitude, longitude, "extracted", region)
                except TypeError:
                    return (None, None, None, None)
        # Video is taken from an Android or if there is no geotag
        for abbr in self.abbr_to_geodata.keys():
            if abbr in metadata_format['filename'][:-4]:
                location = self.abbr_to_geodata[abbr]
                return (location[0], location[1], "derived", abbr)
        return (None, None, None, None)

    def get_duration(self, metadata: dict) -> float:
        '''
        Get the duration of the video.
        input:
            raw metadata from get_raw_metadata <dict>
        output:
            duration <float>
        '''
        duration = metadata['format'].get('duration', None)
        ret_dur = float(duration) if duration is not None else None
        return ret_dur

    def get_resolution(self, metadata: dict) -> "tuple[int, int]":
        '''
        Get the resolution of the video.
        input:
            raw metadata from get_raw_metadata <dict>
        outputt:
            (width <int>, height<int>)
        '''
        if self.debug:
            pprint(metadata)
        i = 0
        coded_width = None
        coded_height = None
        while (i < len(metadata['streams']) and (coded_width is None)):
            coded_width = metadata['streams'][i].get('coded_width', None)
            coded_height = metadata['streams'][i].get('coded_height', None)
            i += 1
        ret_width = int(coded_width) if coded_width is not None else None
        ret_height = int(coded_height) if coded_height is not None else None
        return (ret_width, ret_height)

    def get_metadata_processed(self, metadata: dict) -> dict:
        '''
        Process raw metadata.
        input:
            raw metadata from get_raw_metadata <dict>
        ouput:
            dictionary of self.metadata, which includes
                filepath
                datetime
                latitude
                longitude
                geodata_src
                region
                duration
                res_width
                res_height
        '''
        latitude, longitude, geodata_src, region = self.get_geodata(metadata)
        res_width, res_height = self.get_resolution(metadata)
        return {
            self.metadata[0]: metadata['format'].get('filename', None),
            self.metadata[1]: self.get_creation_time(metadata),
            self.metadata[2]: latitude,
            self.metadata[3]: longitude,
            self.metadata[4]: geodata_src,
            self.metadata[5]: region,
            self.metadata[6]: self.get_duration(metadata),
            self.metadata[7]: res_width,
            self.metadata[8]: res_height
        }

    def print_metadata(self, metadata: dict):
        '''
        print the metadata in an easily readable way.
        '''
        pprint(metadata)
