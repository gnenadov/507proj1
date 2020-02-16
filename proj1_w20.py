#########################################
##### Name:       Gordon Nenadovic  #####
##### Uniqname:   gnenadov          #####
#########################################
import requests
import json
import webbrowser


class Media:

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", json=None):
        if json is None:
            self.title = title
            self.author = author
            self.release_year = release_year
            self.url = url
        else:
            try:
                self.title = json["collectionName"]
            except KeyError:
                self.title = json["trackName"]
            self.author = json["artistName"]
            self.release_year = json["releaseDate"].split('-')[0]
            try:
                self.url = json["collectionViewUrl"]
            except KeyError:
                self.url = json["trackViewUrl"]

    def info(self):
        return f"{self.title} by {self.author} ({self.release_year})"

    def length(self):
        return 0


# Other classes, functions, etc. should go here


class Song(Media):
    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL",
                 album="No Album", genre="No Genre", track_length=0, json=None):
        super().__init__(title, author, release_year, url, json)
        if json is None:
            self.album = album
            self.genre = genre
            self.track_length = track_length
        else:
            self.title = json["trackName"]
            self.album = json["collectionName"]
            self.genre = json["primaryGenreName"]
            self.track_length = json["trackTimeMillis"]

    def info(self):
        return f"{super().info()} [{self.genre}]"

    def length(self):
        return int(self.track_length / 1000)


class Movie(Media):
    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL",
                 rating="No Rating", movie_length=0, json=None):
        super().__init__(title, author, release_year, url, json)
        if json is None:
            self.rating = rating
            self.movie_length = movie_length
        else:
            self.title = json["trackName"]
            self.rating = json["contentAdvisoryRating"]
            self.movie_length = json["trackTimeMillis"]

    def info(self):
        return f"{super().info()} [{self.rating}]"

    def length(self):
        return int(self.movie_length / 60000)


baseurl = "https://itunes.apple.com/search"
response = requests.get(baseurl, params={"term": "a day to remember", "limit": 15}).json()


songs_list = []
movies_list = []
media_list = []


def api_search(response):
    '''

    :param response:
    :return:
    '''
    count = 0
    search_result = response["results"]
    for result in search_result:
        if "kind" in result:
            if result["kind"] == "song":
                count += 1
                song = Song(json=result)
                songs_list.append(str(count) + ' ' + song.info())
            elif result["kind"] == "feature-movie":
                count += 1
                movie = Movie(json=result)
                movies_list.append(str(count) + ' ' + movie.info())
            else:
                count += 1
                media = Media(json=result)
                media_list.append(str(count) + ' ' + media.info())

    print("SONGS\n")
    for entry in songs_list:
        print(entry + '\n')
    print("MOVIES\n")
    for entry in movies_list:
        print(entry + '\n')
    print("OTHER MEDIA\n")
    for entry in media_list:
        print(entry + '\n')


api_search(response)


if __name__ == "__main__":
    # your control code for Part 4 (interactive search) should go here
    pass
