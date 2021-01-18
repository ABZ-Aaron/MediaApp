import os

import sys

import tkinter as tk

from tkinter import messagebox, filedialog, ttk

from MediaClasses import *

class MainApp(tk.Frame):
    """Represents the graphical user interface.

       This class includes a library object and playlist object. Methods
       of these objects are invoked via the GUI.

       Attributes in constructor:
            library: Library object to store and manipulate library items.
            playlist: Playlist object to store and manipulate playlist items.
            master: The root window.
    """

    def __init__(self, library, playlist, master):
        super().__init__(master)
        master.title("Media App")
        self.pack(expand = True, fill = "both")
        
        # Initiate Library and Playlist upon opening of window and
        # return full current library and playlist.
        self.library = library
        self.playlist = playlist
        self.get_playlist = self.playlist.get_all_media()
        self.get_library = self.library.get_all_media()

        # Filter variable allows us to determine when filter is on or off.
        # This is used when adding to playlist or querying info.
        self.filter_on = False 

        # Widget Colours.
        self.viewer_colour = "alice blue"
        self.entry_colour = "Wheat1"

        # Create widgets for window.
        self.create_main_widgets()

        # This will load in a file upon opening of form and add media items from file
        # to main library view within the window. This assumes file structure remains the 
        # same as it was provided. User can save current library contents 
        # to this file upon quitting the application if save checkbox is selected.
        try:
            self.init_items = os.path.dirname(sys.argv[0])+'/init_library.csv'
            self.library.read_items_from_file(self.init_items)
            self.update_tree(self.get_library)
        except Exception:
            pass

    def create_main_widgets(self):
        """Sets up all application widgets
        
           Some widget parameters are stored in dictionaries and set up
           via loops. To alter these widets, additional paramaters can 
           added to dictionary values
        """
        # Set style of the form.
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", background = self.viewer_colour, 
                        fieldbackground = self.viewer_colour, 
                        borderwidth = 10, highlightthickness = 5,
                        font = (None, 8))

        # String and Integer variable storage.
        self.filter_text = tk.StringVar()
        self.features_name = tk.StringVar()
        self.filter_var = tk.IntVar(); self.filter_names = ("Language", "Format")
        self.media_type_var = tk.IntVar() ; self.types = ("Song", "Video")
        self.move_to_position = tk.IntVar()
        self.filter_label_text = tk.StringVar()
        self.save_var = tk.IntVar()

        # Set up headers for window areas.
        self.library_label = tk.Label(self, text = "LIBRARY", font=("Comic Sans MS", 26))
        self.library_label.grid(row = 0, column = 0, columnspan = 2, sticky = "nsew", padx = 6, pady = 6)
        self.playlist_label = tk.Label(self, text = "PLAYLIST", font=("Comic Sans MS", 26))   
        self.playlist_label.grid(row = 0, column = 9, sticky = "nsew", padx = 6, pady = 6)  

        # Format - text : [row, column, variable, value]
        radiobuttons = {                        
                        "Song" : [1, 1, self.media_type_var, 0],
                        "Video" : [2, 1, self.media_type_var, 1],
                        "Language" : [4, 1, self.filter_var, 0],
                        "Format" : [5, 1, self.filter_var, 1]
                        }
                
        # Format - text : [row, column, command, rowspan]
        window_buttons = {                        
                          "Add Media" : [1, 0, self.add_media_click, 2],
                          "Filter" : [3, 0, self.filter_button_click, 3],
                          "File Read" : [8, 0, self.read_from_file_click, None],
                          "File Write" : [9, 0, self.write_to_file_button_click, None],
                          "Has Artist" : [10, 0, self.features_artist_button_click, None],
                          "Item Info" : [11, 0, self.get_info_library_click, None],
                          "Refresh" : [7, 0, lambda: self.update_tree(self.get_library), None],
                          "Quit" : [12, 0, self.quit_window_click, None],
                          "Add to Playlist" : [1, 9, self.add_to_playlist_click, None],
                          "Remove Song" : [2, 9, self.remove_from_playlist_click, None],
                          "Playlist Length" : [3, 9, self.return_playlist_length_click, None],
                          "Song Information" : [4, 9, self.get_info_playlist_click, None],
                          "Move To Index" : [5, 9, self.move_media_click, None],
                          "Remove Item" : [6, 0, self.remove_from_library_click, None]
                         }

        # Set up Buttons, Entries, and RadioButtons for window.
        for key, value in window_buttons.items():
            button = tk.Button(self, text = key, command = value[2])
            button.grid(row = value[0], column = value[1], rowspan = value[3], 
                        sticky = "nsew", padx = 6, pady = 6)
        
        for key, value in radiobuttons.items():
            radiobutton = tk.Radiobutton(self, text = key, variable = value[2], value = value[3])
            radiobutton.grid(row = value[0], column = value[1], sticky = "w", padx = (0, 6))


        # Set up entry fields.
        self.move_media_entry = tk.Entry(self, textvariable = self.move_to_position, 
                                         justify = "center", bg = self.entry_colour, 
                                         relief = "ridge")
        self.move_media_entry.grid(row = 6, column = 9)


        self.feautures_artist_entry = tk.Entry(self, textvariable = self.features_name, width = 10, 
                                               justify = "center", bg = self.entry_colour, 
                                               relief = "ridge")
        self.feautures_artist_entry.grid(row = 10, column = 1)


        self.filter_entry = tk.Entry(self, textvariable = self.filter_text, width = 10, 
                                     justify = "center", bg = self.entry_colour, 
                                     relief = "ridge")
        self.filter_entry.grid(row = 3, column = 1)

        # Set up library view widgets.
        tree_titles = ("Title", "Format", "Language", "Length", 
                       "Performers", "Director", "Actors")

        self.tree = ttk.Treeview(self)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_view_select)
        self.tree.grid(row = 1, column = 2, columnspan = 5, rowspan = 13, 
                       sticky = "nsew", pady = 6, padx = 6)
        self.tree["columns"] = tree_titles
        self.tree.column("#0", width = 50)
        self.tree.heading("#0", text = "Pos")
        for index in range(len(tree_titles)):
            self.tree.column(index, width = 90, anchor = "center")
            self.tree.heading(index, text = tree_titles[index])
        
        # Set up save on exit check button.
        self.save_checkbutton = tk.Checkbutton(self, text = "Save on Exit", variable = self.save_var, value = None)
        self.save_checkbutton.grid(row = 12, column = 1)

        # Set up filter label for library view.
        self.show_filter_label = tk.Label(self, textvariable = self.filter_label_text)
        self.show_filter_label.grid(row = 0, column = 2, sticky = "sw")
        self.filter_label_text.set("Filter Off")

        # Set up message label for playlist view.
        self.playlist_message = tk.Label(self, text = "Your Playlist View!")
        self.playlist_message.config(font = ('Comic Sans MS', 14, 'italic'))
        self.playlist_message.grid(sticky = "ew", row = 7, column = 9, padx = 6, pady = (15, 0))

        # Set up playlist view to visualise songs in playlist.
        self.playlist_box = tk.Listbox(self, selectmode = tk.SINGLE, bg = self.viewer_colour) 
        self.playlist_box.grid(row = 8, column = 9, rowspan = 7, sticky = "nsew", 
                               padx = 6, pady = (0, 6))

        # Configue columns and rows of main window.
        # When expanding window, widgets should expand with it.
        for row in range(14):
            self.grid_rowconfigure(row, weight=1)
        for col in range(6):
            self.grid_columnconfigure(col, weight=1)

    def add_media_click(self):
        """Initiates creation and set up of new window

           Method creates new window, disables background window, and 
           calls Method to set up widgets. Purpose of new window is to 
           add new media items to library view.
        """
        self.media_window = tk.Toplevel(self.master)
        self.media_window.title("Add Media")
        self.media_window.grab_set()
        self.add_media_widgets()

    def add_media_widgets(self):
        """Adds widgets to media window

           Method determines media type based on which radio button is currently on.
           Method uses this information to set relevant entry boxes / labels in window.
        """
        self.object_type = self.types[self.media_type_var.get()]

        type_field = "Type"
        title_field = "Title"
        format_field = "Format"
        language_field = "Language"
        length_field = "Length"
        performers_field = "Performers (Mike,Ben,Dan)"
        director_field = "Director"
        actors_field = "Actors (Mike,Ben,Dan)"

        # Set field titles. These are used to generate relevant entry boxes.
        if self.object_type == "Song":
            fields = (type_field, title_field, format_field, language_field, 
                      length_field, performers_field)

        elif self.object_type == "Video":
            fields = (type_field, title_field, format_field, language_field, 
                      length_field, director_field, actors_field)

        # Create entry fields dependent on type of media.
        self.entries = {}
        self.fields = fields[1:]
        for attr in self.fields:
            frame = tk.Frame(self.media_window)
            frame.pack(side = "top", fill = "x", padx=5, pady=5)
            label = tk.Label(frame, width = 20, text = attr, anchor = 'w')
            entry = tk.Entry(frame)
            label.pack(side = "left")
            entry.pack(side = "left", fill = "x", expand = True)
            self.entries[attr] = entry

        # Add relevant buttons to media window.
        self.add_button = tk.Button(self.media_window, text = "Add", command = self.add_media_item_click)
        self.quit_button = tk.Button(self.media_window, text = "Exit", command = self.quit_media_window)
        self.quit_button.pack(padx = 5, pady = 5, side = "right")
        self.add_button.pack(padx = 5, pady = 5, side = "right")

    def read_from_file_click(self):
        """Read from selected CSV file
        
           Method prompts user to select a csv file. If selected, and valid, calls library's 
           read_items_from_file method. Once complete and items are added to library, library view
           is refreshed to accommodate new items.
        """
        file_name = filedialog.askopenfilename(title = "Select File", filetypes = (("CSV Files","*.csv"),))
        if not file_name:
            return

        try:
            read_file_error = self.library.read_items_from_file(file_name)
        except:
            messagebox.showerror("Problem", "Issue reading file. Please ensure CSV "
                                 "is in correct format as specified in user guide."); return
            
        self.update_tree(self.get_library)
        self.set_filter(False)
 
    def write_to_file_button_click(self):
        """Writes library view items to specified CSV file.
        
           Method prompts specify a CSV file, then calls library's write_items_to_file
           method in order to save all library view items down.
        """
        file_name = filedialog.asksaveasfilename(title = "Select file",filetypes = (("CSV Files","*.csv"),), 
                                             defaultextension= "csv")
        if not file_name:
            return

        self.library.write_items_to_file(file_name)
        
    def features_artist_button_click(self):
        """Checks if specified artist features in library view media item.
        
           Method takes user entry, determines what items is selected from library 
           view, and invokes media item method to determine whether user entry is found
           assoicated with media item.
        """
        user_entry = self.features_name.get()

        if user_entry == "":
            messagebox.showerror("Problem", "You have not entered anything into "
                                 "the entry box. Please try again."); return

        try:
            media_item = self.get_item_from_library_view()
        except AttributeError:
            messagebox.showerror("Problem", "Please ensure you have selected an item "
                                "from the library view"); return

        artist_in_media = media_item.get_media_with_artist(user_entry)

        if artist_in_media:
            text = f"The media '{media_item.get_media_title()}' features the artist '{user_entry}'"
        else: 
            text = f"The media '{media_item.get_media_title()}' does not feature the artist '{user_entry}'"

        messagebox.showinfo("Output of Query", text)
        self.feautures_artist_entry.delete(0, 'end')
    
    def filter_button_click(self):
        """Filters library view by format or language.
    
           Method determines what filter type is selected (language or format), what user
           would like to filter by, and invokes library method to return filtered collection.
           This collection is used to update tree.
        """   
        self.filter_type = self.filter_names[self.filter_var.get()]
        filter_pattern = self.filter_text.get()

        if filter_pattern == "":
            messagebox.showerror("Problem", "You have not entered anything into "
                                 "the entry box. Please try again."); return

        # Return relevant filter list.
        if self.filter_type == "Language":
            self.filter_list = self.library.get_media_of_language(filter_pattern)

        elif self.filter_type == "Format":
            self.filter_list = self.library.get_media_of_format(filter_pattern)

        self.update_tree(self.filter_list)
        self.set_filter(True, self.filter_type, filter_pattern)

    def get_info_library_click(self):
        """Show details associated with selected item from library view.
    
           Method determines what media item is selected in the library view,
           and returns its string method.
        """   
        try:
            media_item = self.get_item_from_library_view()
        except Exception:
            messagebox.showerror("Problem", "Please ensure you have selected an item "
                                "from the library view"); return

        messagebox.showinfo("Info", f"{media_item.get_class_name()}\n\n"
                                    f"{str(media_item)}")

    def update_tree(self, media_collection):
        """Update library view with relevant media items.

           Method deletes all items within the library view, before re-adding
           media items from specified collection. Method will either add items from the main
           library collection, or a returned filter collection.
    
           Main Args:
                media_collection = This will either be the main collection from the library 
                                   object or collection returned if filter is set to ON.
        """   
        self.tree.delete(*self.tree.get_children())

        for index, media_item in enumerate(media_collection):
            obj_type = media_item.get_class_name()

            if obj_type == "Song":
                performers = ",".join(media_item.get_performer_names())
                self.tree.insert("", "end", text = index, 
                                values = (media_item.get_media_title(), media_item.get_media_format(), 
                                          media_item.get_media_language(), media_item.get_play_length(), 
                                          performers, "---", "---"))

            elif obj_type == "Video":
                actors = ",".join(media_item.get_actors())
                self.tree.insert("", "end", text = index, 
                                values = (media_item.get_media_title(), media_item.get_media_format(), 
                                          media_item.get_media_language(), media_item.get_play_length(), 
                                          "---", media_item.get_director_name(), actors))

        if media_collection == self.get_library:
            self.set_filter(False)
        self.filter_entry.delete(0, 'end')

    def configure_media_object(self):
        """Take user entries from media window and create media object.
    
           Method takes user entries from media window & returns media object.
           Method returns None if user exits at any point.
        """   
        user_entries = [self.entries[field].get() for field in self.fields]
        no_empty_entries = all(user_entries)

        if not no_empty_entries:
            ok_cancel_box = messagebox.askokcancel("Problem", "One or more entry fields "
                                                    "is blank. Try again?")

            if ok_cancel_box:
                return 
            else:
                self.quit_media_window()
                return

        title = user_entries[0]
        media_format = user_entries[1]
        language = user_entries[2]

        try:
            length = int(user_entries[3])
        except ValueError:
            ok_cancel_box = messagebox.askokcancel("Problem", "Please enter an integer "
                                                    "into the length box. Try again?")

            if ok_cancel_box:
                return
            else:
                self.quit_media_window()
                return
            
        if self.object_type == "Song":
            performers = user_entries[4]
            performers = performers.split(",")
            media_object = Song(title, media_format, language, length, performers)

        elif self.object_type == "Video":
            director = user_entries[4]
            actors = user_entries[5]
            actors = actors.split(",")
            media_object = Video(title, media_format, language, length, director, actors)

        return media_object

    def add_media_item_click(self):
        """Calls methods to configure media object, add to library collection, and update tree.
    
           Method calls a series of methods to update tree, before quitting the window.
        """  
        media_object = self.configure_media_object()
        if not media_object:
            return
        self.library.add_media(media_object)
        self.update_tree(self.get_library)
        self.set_filter(False)
        self.quit_media_window()
        
    def move_media_click(self):
        """Move media item to specified index in playlist collection
    
           Method gets position specified by user, the index of the selected
           playlist item, and calls a playlist method to move item in playlist collection 
           to specified location.
        """  
        try:
            move_to_position = self.move_to_position.get()
            index_of_item = self.playlist_box.curselection()[0]

        except IndexError:
            messagebox.showerror("Problem", "Please ensure you have selected "
                                 "a playlist item."); return

        except Exception:
            messagebox.showerror("Problem", "Please ensure you have entered "
                                 "an integer into entry box."); return
            
        if move_to_position < 0 or move_to_position >= len(self.get_playlist):
            messagebox.showerror("Problem", "The position you've entered is out of "
                                 "bounds. Try again!"); return

        self.playlist.move_song(index_of_item, move_to_position)
        self.refresh_playlist()

    def get_info_playlist_click(self):
        """Reveal information associated with playlist item.

           Method reveals string representation of 
           currently selected media item, or returns None
        """  
        try:
            index_of_song = self.playlist_box.curselection()[0]
        except IndexError:
            messagebox.showerror("Problem", "Please ensure you have selected "
                                 "a playlist item."); return

        info = str(self.get_playlist[index_of_song])
        messagebox.showinfo("Info", info)

    def remove_from_playlist_click(self):
        """Remove media based on position specified in playlist view.

           Method determines index of selected playlist item, and
           removes playlist item from playlist collection and updates playlist view.
        """  
        try:
            index_of_song = self.playlist_box.curselection()[0]
        except IndexError:
            messagebox.showerror("Problem", "Please ensure you have selected "
                                 "a playlist item."); return

        self.playlist.remove_song(index_of_song)   
        self.refresh_playlist() 

    def remove_from_library_click(self):
        """Remove media based on position specified in library view.

           Method determines index of selected library item, and
           removes library item from library collection and updates library view.
        """  
        try:
            if self.filter_on:
                messagebox.showerror("Problem", "Please clear filter using the Refresh button before "
                                     "removing library item.")
                return
            else:
                removed_item = self.library.remove_media(self.tree_view_selection)
                messagebox.showinfo("Info", f"'{removed_item.get_media_title()}' has been removed!")
                self.update_tree(self.get_library)
                return
        except Exception:
            messagebox.showerror("Problem", "Please ensure you have selected a library item to remove")
        
    def return_playlist_length_click(self):
        """Reveals the runtime length of the playlist.

           Method invokes playlist method to determine how many seconds
           there are in the playlist overall.
        """  
        runtime = self.playlist.get_playlist_runtime()

        if len(self.get_playlist) == 0:
            messagebox.showinfo("Info", "Your playlist is empty. Try adding some songs!")
        else:
            messagebox.showinfo("Info", f"Your playlist is {runtime} seconds long!")
    
    def add_to_playlist_click(self):
        """Add a selected library song to the playlist.

           Method take selected library view item and invokes playlist method
           to add media item. Selected media item in library view must be of 
           object type Song.
        """  
        try:
            media_item = self.get_item_from_library_view()
        except AttributeError:
            messagebox.showerror("Problem", "Please ensure you have selected an item "
                                "from the library view"); return

        if media_item.get_class_name() == "Video":
            messagebox.showerror("Problem", "You cannot add videos to playlist. Try adding a song!"); return

        self.playlist.add_song(media_item)
        self.refresh_playlist()

    def get_item_from_library_view(self):
        """Get item from library view based on selection.
        
           Checks if a filter is currently set or not in the library view. 
           Once index position of the item is selected is determined, it's 
           used pull the item from the source list at that index. Any issues and 
           exception is returned.
        """
        try:
            if self.filter_on:
                media_item = self.filter_list[self.tree_view_selection]
            else:
                media_item = self.get_library[self.tree_view_selection]
            return media_item
        except:
            raise Exception

    def refresh_playlist(self):
        """Refresh the Playlist view with the most up-to-date playlist collection.

           Method deletes all playlist view items, and re-adds them from the playlist
           collection.
        """  
        self.playlist_box.delete(0, tk.END)
        for index, item in enumerate(self.get_playlist):
            self.playlist_box.insert(tk.END, f" {index}: {item.get_media_title()}")

    def set_filter(self, option, filter_type = None, filter_pattern = None):
        """Updates filter label and toggles filter variable on / off
        
           Updating filter label allows end user to see if filter is on or off.
           Filter variable is used so other methods can determine whether filter is on / off
           and know which list to pull from when manipulating library view.

           Main Args:
                option: Boolean value. True == Filter on. False == Filter off.
                filter_type: The type of filter set.
                filter_pattern: What filter value passed by user.
        """
        if (option == True) and (filter_type != None) and (filter_pattern != None):
            text = f"Filter ON. Filtered by {filter_type}: {filter_pattern}"
        elif option == False:
            text = "Filter OFF"
        self.filter_on = option; 
        self.filter_label_text.set(text)
    
    def on_tree_view_select(self, event):
        """Return selected item position in library view.

           Method sets the index of item selected in library view.
        """  
        for item in self.tree.selection():
            self.tree_view_selection = self.tree.item(item, "text")

    def quit_window_click(self):
        """Close the main window down.
        
           Method is used to destroy the main window. Method will also attempt to save contents of library
           if checkbox is selected before closing.
        """
        if self.save_var.get() == 1:
            try:
                self.library.write_items_to_file(self.init_items)
                message = "Any new changes made have been saved!"
                messagebox.showinfo("Success", message)
            except Exception:
                message = "Issue saving file. Window will close."
                file_save_issue = messagebox.showerror("Problem", message)
        self.master.destroy()

    def quit_media_window(self):
        """Quit media window.

           Method allows the use of the main window, and quits 
           media window.
        """
        self.media_window.grab_release()
        self.media_window.destroy()

# Initialise library and playlist.
library = Library()
playlist = PlayList()

# Start the app.
root = tk.Tk()
MainApp(library, playlist, root)
root.mainloop()