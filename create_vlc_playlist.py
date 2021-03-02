import xml.etree.ElementTree as xml
import os


class Playlist:
    """Build xml playlist."""

    def __init__(self):
        # Defines basic tree structure.
        self.playlist = xml.Element("playlist")
        self.tree = xml.ElementTree(self.playlist)
        self.playlist.set("xmlns", "http://xspf.org/ns/0/")
        self.playlist.set("xmlns:vlc", "http://www.songlan.org/vlc/playlist/ns/0/")
        self.playlist.set("version", "1")

        self.title = xml.Element("title")
        self.playlist.append(self.title)
        self.title.text = "Playlist"

        self.trackList = xml.Element("trackList")
        self.playlist.append(self.trackList)

    def add_track(self, path):
        # Add tracks to xml tree (within trackList).
        track = xml.Element("track")
        location = xml.Element("location")
        location.text = path
        track.append(location)
        self.trackList.append(track)

    def get_playlist(self):
        # Return complete playlist with tracks.
        return self.playlist


class Songs:
    """Manage songs to be added to the playlist."""

    def __init__(self):
        pass

    def edit_paths(self, song_files):
        # Add path and prefix to files as required in vlc playlist file.
        for index in range(len(song_files)):
            song_files[index] = ("file:///" + os.path.join(song_files[index])).replace(
                "\\", "/"
            )
        return song_files


def create_playlist(song_files, music_dir):

    playlist = Playlist()
    songs = Songs()

    song_paths = songs.edit_paths(song_files)

    for path in song_paths:
        playlist.add_track(path)

    playlist_xml = playlist.get_playlist()
    with open(os.join(os.expanduser(music_dir), "songs.xspf"), "w") as mf:
        mf.write(xml.tostring(playlist_xml).decode("utf-8"))
