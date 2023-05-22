from multiprocessing import Process
from pytube import Playlist
from pytube import YouTube
from pathlib import Path
import json
import GUI
import os


"""
Automated startup program that automatically downloads songs from saved playlist, downloading newly added songs
and uploading them to the cloud for extra redunancy

"""


class App:
    def __init__(self):
        """
            Runs folder_intergrity() to ensure the Configured Music folder exists ensuring that if any
            errors are encountered they are properly logged. Their will likely be more functions in this
            in the future
            :return:
         """
        self.a = []

         # Notifies user through GUI that program has started
        # Checks if any folders are missing
        try:
            self.folder_intergrity()

        except FileNotFoundError:
            # If routine doesn't work
            print("File not found, file repaired")
            quit()

        else:
            # If routine works
            print("Routine finished")
            #GUI.Startup_Notifer("YTD Notifer","Message")
            self.get_links()

    def folder_intergrity(self):  # Complete
        """
        Attempts to create "Music" folder if one doesn't exist, if one does exist
        it simply won't create a file, alternatively I was going to create a whole
        function that checks if it exists, but this one line of code does it without issue

        Note: Testing may be needed
        :return:
        """
        # Creates music folder, if one does exist it doesn't create a duplicate
        Path("Music").mkdir(parents=True, exist_ok=True)

    def get_links(self):  # Complete
        """
        Gets links from within Data.json by opening it and then parsing it
        Then getting the dictionary values by .values and finally iterating through the
        .json list getting each individually link one by one
        :return:
        """
        # Gets links within Data.json file for downloading
        with open("Data.json") as data:
            file_contents = data.read()  # Reads Data.json

        parsed_data = json.loads(file_contents)  # Converts json to dictionary
        x = parsed_data.values()  # Gets values within dictionary
        for Playlist_values in x:  # Iterates through dictionary
            print("PV:", Playlist_values)
            self.song_check(Playlist_values)  # Calls song_check to begin downloading process for URL
            # Playlist_values variable = Current Playlist URL

    def song_check(self, url: str):  # URL = Playlist URL
        """
        Creates list from Downloaded songs already downloaded and creates another list
        from songs within Playlist and gets a list of missing songs and then puts those
        missing songs into a list

        *For Download_Music() - > For downloading missing songs a for-loop program checks if current
        song matches to Missing song list, by checking its title*

        Note: Look for ways to optimize as it could be slow (Possibly)
           - Use Multiprocessing to organize Playlist_URL_Songs and Parsed_URL_Songs at the same time
        :param url:
        :return:
        """

        self.Currently_Downloaded_Songs = []  # Songs currently downloaded
        self.Playlist_URL_Songs = []  # Songs within the actual Playlist
        parsed_playlist_url = Playlist(url)  # Converts Playlist URL to Playlist Obj to interact

        def downloaded_songs(pl_url):
            """
            Adds currently downloaded song to a list, that being
            Currently_Downloaded_Songs to compare to songs within the actual playlist
            :return:
            """
            self.amount_of_downloaded_songs = 0
            for dir_check in os.listdir(f"Music/{pl_url.title}"):  # Goes through Music directory for current songs
                self.amount_of_downloaded_songs+=1
                parsed_string = dir_check.replace(".mp4", "")  # Removes .mp4 from text
                print(f"DS:{parsed_string}")
                self.Currently_Downloaded_Songs.append(parsed_string)  # Adds Current songs to list
            print(f"Downloaded Songs: {self.amount_of_downloaded_songs}")


        def url_songs():
            self.amount_of_songs_in_playlist = 0
            for ab in parsed_playlist_url.video_urls:
                self.amount_of_songs_in_playlist+=1
                cv = YouTube(ab)
                print(f"URL_S:{cv.title}")
                self.Playlist_URL_Songs.append(cv.title)
            print(f"URL Songs {self.amount_of_songs_in_playlist}")


        p = Process(target=downloaded_songs(parsed_playlist_url))
        p.start()  # Starts Downloaded_Songs Function
        p2 = Process(target=url_songs())
        # Ensures both function run at the same time

        p2.start()  #  Starts URL_Songs() Function
        p.join()
        p2.join()
        # the join means wait until it finished

        #result = set(self.Currently_Downloaded_Songs) - set(self.Playlist_URL_Songs)
        self.missing_songs = list(set(self.Playlist_URL_Songs).difference(self.Currently_Downloaded_Songs))
        print(len(self.missing_songs))
       # print(f"Missing Songs: {self.missing_songs}")

        # Every song that is missing from the download list

        self.download_music(url, self.missing_songs)

    def download_music(self, playlist_url: str, missing_songs: list):  # Complete NEEDS OPTIMIZATION
        print('Download Music Starting!')
        """
        Downloads music from the selected Playlist, being "Current_Playlist"
        Uses for-loop to individually go through iterate through every song in the Playlist
        Downloading them each loop

        Notes: Look for a faster way to download, to slow for large Playlists.
        :param playlist_url:
        :param missing_songs:
        :return:
        """

        # Downloads songs from Playlist';;'''
        current_playlist = Playlist(playlist_url)  # Sets which playlist will currently be downloaded
        try:
            os.mkdir(f"Music/{current_playlist.title}")
        except:
            pass

        for video in current_playlist.videos:  # Downloads song
            if video.title in missing_songs:
                # If song is missing
                try:
                    print(f"Downloading {video.title}")
                    video.streams.filter(file_extension='mp4', only_audio=True).first().download(
                        output_path=f"Music/{current_playlist.title}")
                except:
                    print("cim laude")
            else:
                #  If song is not missed
                print(f"{video.title} Skipping")


if __name__ == '__main__':
    App()
