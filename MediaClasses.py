import ast

import csv

class Library:
    """Represents a library to store video and song items

       This class includes a collection to store media objects

       Attributes in constructor:
            media_list: An ordered collection type (list) to store all objects
       Class attribute:
            FIELDS: A set used to specify titles for writing and reading from files
    """

    FIELDS = ('Type', 'Media Title', 'Media Format', 'Media Language',
            'Play Length', 'Performer Names', 'Director Name', 'Actors')

    def __init__(self):
        self._media_list = []

    def add_media(self, media):
        """Adds media item to library collection.
        
           Media item should be a Song or Video class object.

           Main Args:
                media: The Song or Video object to be added.
        """
        self._media_list.append(media)

    def remove_media(self, position):
        """Remove item for Library collection 

           Main Args:
                position: The index in library collection to remove item from
        """
        removed_item = self._media_list.pop(position)
        return removed_item

    def reformat_items(self, item):
        """Converts item from string to list by evaluating the expression

           Item should be emptry or of string format, with the intention of evaluating
           to a list type.

           Main Args:
                item: The item to evaluate
        """
        if item != "":
            return ast.literal_eval(item)
        return item

    def read_items_from_file(self, file_name):
        """Import Media from specified file and add to library collection
        
           File should be an existing specified file of correct format
           & structure specified by guidelines. Function reads all items from
           file row by row, generates relevant objects, and appends these to 
           library collection.

           Main Args:
                file_name: File where data will be loaded from
        """
        with open(file_name, "r") as f:
            input_file = csv.DictReader(f)
            for row in input_file:

                media_type = row[Library.FIELDS[0]]
                media_title = row[Library.FIELDS[1]]
                media_format = row[Library.FIELDS[2]]
                media_language = row[Library.FIELDS[3]]
                play_length = int(row[Library.FIELDS[4]])
                performer_names = row[Library.FIELDS[5]]
                director_name = row[Library.FIELDS[6]]
                actors = row[Library.FIELDS[7]]
                performer_names = self.reformat_items(performer_names)
                actors = self.reformat_items(actors)

                if media_type == "Song":
                    media_object = Song(media_title, media_format, media_language, 
                                        play_length, performer_names)
                                        
                elif media_type == "Video":
                    media_object = Video(media_title, media_format, media_language, 
                                         play_length, director_name, actors)

                self.add_media(media_object)

    def write_items_to_file(self, file_name):
        """Write all items in library to specified file
        
           File should be of CSV format. Function converts objects from
           library collection to dictionary before saving down to CSV.

           Main Args:
                file_name: File where data from library collection will be saved
        """
        objects = []
        for obj in self._media_list:
            object_dictionary = obj.to_dict()
            objects.append(object_dictionary)

        with open(file_name, 'w') as f:
            writer = csv.DictWriter(f, fieldnames = Library.FIELDS)
            writer.writeheader()
            for obj in objects:
                writer.writerow(obj)

    def get_all_media(self):
        """Return all media items"""
        return self._media_list
    
    def get_media_of_language(self, search_string):
        """Return media with specified language

           This will search each object within library collection for specified
           string under the language attribute and return all matching instances
        
           Main Args:
                search_string: String which will be searched for
        """
        language_filter = [media for media in self._media_list 
                          if media.get_media_language().lower() == search_string.lower()]
        return language_filter

    def get_media_of_format(self, search_string):
        """Return media with specified format
           
           This will search each object within library collection for specified
           string under the format attribute and return all matching instances
        
           Main Args:
                search_string: String which will be searched for
        """
        format_filter = [media for media in self._media_list
                        if media.get_media_format().lower() == search_string.lower()]
        return format_filter
    
class PlayList:
    """Represents a playlist to store video and song items

       This class includes a collection to store song objects

       Attributes in constructor:
            play_list: An ordered collection type (list) to store all song objects
    """
    
    def __init__(self):
        self._play_list = []

    def get_all_media(self):
        """Return all media items from playlist"""
        return self._play_list
     
    def get_playlist_runtime(self):
        """Returns full runtime of playlist collection

           Function sums the length attribute of all song objects
           within the playlist collection
        """
        play_list_runtime = 0
        for song in self._play_list:
            play_list_runtime += song._play_length
        return play_list_runtime
    
    def add_song(self, media):
        """Add media item to playlist collection

           Function will add media item to end of collection. Media
           item should be a song object

           Main Args:
                media: song object intialised through the Song class
        """
        self._play_list.append(media)

    def move_song(self, from_position, to_position):
        """Move song at given position to new position in playlist collection

           Arguments should be of type integer and within the bounds of the playlist collection

           Main Args:
                from_position: Index of item in playlist collection which needs moved
                to_position: Index in playlist collection where item should be inserted
        """
        self._play_list.insert(to_position, self._play_list.pop(from_position))

    def remove_song(self, index):
        """Remove media item from playlist collection
           
           Argument should be of type integer and within the bounds of the playlist collection

           Main Args:
                index: Item at this index in playlist collection will be removed from collection
        """
        self._play_list.pop(index)
    
class MediaItem:
    """Represents a media item (Song or Video)

       Attributes in constructor (including those from child classes):
            media_title: The title of the media object (string)
            media_format: The format of the media object (string) e.g. MP3, DVD
            media_language: The format of media language (string) e.g. French, English
            play_length: The format of media length (integer)
            director_name: The director of the media item (string)
            actors: The actors within the media item (list)
            performer_names: The performers within the media item (list)
    """

    def __init__(self, media_title, media_format, media_language, play_length):
        self._media_title = media_title
        self._media_format = media_format
        self._media_language = media_language
        self._play_length = play_length
    
    def get_media_with_artist(self, name):
        """Returns a boolean value indicating whether passed name has any involvement
           in the media item. 
           
           What fields will be searched is dependent on object type
        """
        return False
    
    def get_media_title(self):
        """Returns media title"""
        return self._media_title

    def get_media_format(self):
        """Returns media format"""
        return self._media_format

    def get_media_language(self):
        """Returns media language"""
        return self._media_language

    def get_play_length(self):
        """Returns media length"""
        return self._play_length

    def get_class_name(self):
        """Returns the name of current class"""
        return self.__class__.__name__ 

    def to_dict(self):
        """Returns an attributes dictionary

           This dictionary stores each attribute for the media item classes along with a title.
           This is used to write items to a file.
        """
        return {Library.FIELDS[0] : self.__class__.__name__, 
                Library.FIELDS[1] : self._media_title, 
                Library.FIELDS[2] : self._media_format, 
                Library.FIELDS[3] : self._media_language, 
                Library.FIELDS[4] : self._play_length}

    def __str__(self):
        return (f"Title: {self._media_title}\n"
                f"Format: {self._media_format}\n"
                f"Language: {self._media_language}\n"
                f"Length: {self._play_length}\n")
        
class Video(MediaItem):
    """Represents a video item

       Attributes in constructor:
            director_name: The director of the media item (string)
            actors: The actors within the media item (list)
    """

    def __init__(self, media_title, media_format, media_language, play_length, director_name, actors):
        super().__init__(media_title, media_format, media_language, play_length)    
        self._director_name = director_name
        self._actors = actors

    def get_media_with_artist(self, name):
        """Returns a boolean value indicating whether passed name has any involvement
           in the media item. 
           
           Function will search the actors within the video object, along with the director using 
           the name parameter, and return True or False if found or not found respectively.
        """
        if (name.upper() in (name.upper() for name in self._actors)) or \
           (name.upper() == self._director_name.upper()):
            return True
        return False

    def get_director_name(self):
        """Returns director name"""
        return self._director_name

    def get_actors(self):
        """Returns actors"""
        return self._actors

    def to_dict(self):
        master_dict = super().to_dict()
        master_dict.update({Library.FIELDS[6] : self._director_name, 
                            Library.FIELDS[7] : self._actors})
        return master_dict

    def __str__(self):
        return (f"{super().__str__()}"
                f"Director: {self._director_name}\n"
                f"Actors: {self._actors}\n")
    
class Song(MediaItem):
    """Represents a Song item

       Attributes in constructor:
                performer_names: The performers within the media item (list)
    """
    
    def __init__(self, media_title, media_format, media_language, play_length, performer_names):
        super().__init__(media_title, media_format, media_language, play_length)
        self._performer_names = performer_names

    def get_media_with_artist(self, name):
        """Returns a boolean value indicating whether passed name has any involvement
           in the media item. 
           
           Function will search the performers within the video object, and return 
           True or False if found or not found respectively.
        """
        if name.upper() in (name.upper() for name in self._performer_names):
            return True
        return False
    
    def get_performer_names(self):
        """Returns performer names"""
        return self._performer_names
    
    def to_dict(self):
        master_dict = super().to_dict()
        master_dict.update({Library.FIELDS[5] : self._performer_names})
        return master_dict

    def __str__(self):
        return (f"{super().__str__()}"
                f"Performers: {self._performer_names}\n")
