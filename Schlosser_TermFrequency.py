# Jonathan Schlosser
# Assignment 5 Term Frequency
# INLS 560 Fall 2019
# April 1, 2020

# The purpose of this program is to calculate the term frequency for words in a file,
# to employ a GUI to ask the user for the file and search term, and to display the appropriate results.
# When running, the program should be able to take different terms and display the results. Also, there
# are a few error messages built into the program and a quit functionality.

# Notes: For this program, the file must be in the same directory and a text file. If not, there may be an error.

# Importing needed packages.
import tkinter, tkinter.filedialog
import string

# Defining the class for the GUI
class TermFrequencyGUI:
    def __init__(self):

        # Setting the background and a second level heading (the title being the first).
        bg_color = 'grey'
        head_2 = "Helvetica 18 bold"

        # Initiating the window and setting color and size properties.
        self.main_window = tkinter.Tk()
        self.main_window.geometry("500x500")
        self.main_window.configure(background=bg_color)

        # Create the title, file, search term, term frequency, quit, and annotation frames.
        self.title_frame = tkinter.Frame(self.main_window)
        self.file_name_frame = tkinter.Frame(self.main_window)
        self.search_term_frame = tkinter.Frame(self.main_window)
        self.term_frequency_frame = tkinter.Frame(self.main_window)
        self.quit_frame = tkinter.Frame(self.main_window)
        self.annotation_frame = tkinter.Frame(self.main_window)

        # Creating the text for the title and setting its font and background color properties.
        self.title = tkinter.Label(self.title_frame, text='Term Frequency Program',
                                   font="Helvetica 36 bold", background=bg_color)
        self.title.pack()

        # Changing the color of frames.
        self.file_name_frame.configure(background=bg_color)
        self.search_term_frame.configure(background=bg_color)
        self.term_frequency_frame.configure(background=bg_color)
        self.quit_frame.configure(background=bg_color)

        # Creating the 'Select a file' Button and file name Label widgets for the first frame
        # an then packing the widgets. Also, setting the font and background color properties.
        self.file_name_title = tkinter.Label(self.file_name_frame, text="File Selection:",
                                             font=head_2, background=bg_color)
        self.select_file_button = tkinter.Button(self.file_name_frame, text='Select a file',
                                                 command=self.select_file)
        self.file_name = tkinter.StringVar()
        self.file_name_label = tkinter.Label(self.file_name_frame, textvariable=self.file_name,
                                             font=head_2, background=bg_color)
        self.file_name_title.pack(side="top")
        self.select_file_button.pack(side="left", padx=30)
        self.file_name_label.pack(side='right')

        # Creating the 'Enter a search term' Label, and search term Entry widgets for the next frame
        # and packing the widgets. Also, setting the font and background color properties.
        self.search_term_label = tkinter.Label(self.search_term_frame, text='Enter a search term:',
                                               font=head_2, background=bg_color)
        self.search_term_entry = tkinter.Entry(self.search_term_frame, width=20)
        self.search_term_label.pack(side='left')
        self.search_term_entry.pack(side='right')

        # Creating the 'Calculate frequency' Button and the Label widget for results and
        # packing the widgets. Also, setting the font and background color properties.
        self.term_frequency_button = tkinter.Button(self.term_frequency_frame, text=' Calculate frequency ',
                                                    command=self.calculate_frequency)
        self.term_frequency = tkinter.StringVar()
        self.term_frequency_label = tkinter.Label(self.term_frequency_frame,
                                                  textvariable=self.term_frequency,
                                                  font=head_2, background=bg_color)
        self.term_frequency_button.pack(side='left', padx=30)
        self.term_frequency_label.pack(side='right')

        # Createing the 'quit' button to quit the program.
        self.quit_button = tkinter.Button(self.quit_frame, text="Quit",
                                          command=self.main_window.destroy)
        self.quit_button.pack()

        # Creating an annotation for the bottom of the window.
        self.annotation_label = tkinter.Label(self.annotation_frame, text="By Jonathan Schlosser \n For INLS 560",
                                              background=bg_color)
        self.annotation_label.pack()

        # Packing all the frames, adding padding, and putting the annotation frame at the bottom.
        self.title_frame.pack(pady=10)
        self.file_name_frame.pack(pady=20)
        self.search_term_frame.pack(pady=20)
        self.term_frequency_frame.pack(pady=20)
        self.quit_frame.pack(pady=20)
        self.annotation_frame.pack(side="bottom")

        tkinter.mainloop()  # Enter the tkinter main loop

    # Displaying the file dialog so the user can select the file to search.
    # Displays the file name, not the full path name.
    def select_file(self):
        try:
            filename = tkinter.filedialog.askopenfilename(initialdir=".")
            if filename == "":
                self.file_name.set("No file was selected.\n Please try again.")
            else:
                self.file_name.set(filename.split('/')[-1])
        except FileNotFoundError:
            self.file_name.set("No file was selected.\n Please try again.")

    # Calling the create_term_frequency_dictionary(filename) function to create a dictionary that
    # contains each word in the file and its frequency in the file, If the user's search term is in
    # the dictionary, the program displays the frequency; if not, it displays a 'not found' message
    def calculate_frequency(self):
        try:
            # Getting the filename.
            filename = self.file_name.get()

            # Calling the function to create the dictionary.
            term_frequency_dictionary = self.create_term_frequency_dictionary(filename)

            # Normalizing the search term entered by the users. This removes whitespaces
            # and changes the term to lowercase.
            searchterm = self.search_term_entry.get().strip().lower()  # normalize search term

            # If the search term is an empty string, display an error message.
            if searchterm == "":
                message = "No search term was entered.\n Please try again."
                self.term_frequency.set(message)
            else:
                # If the search term is in the dictionary, display the results.
                if searchterm in term_frequency_dictionary.keys():
                    self.term_frequency.set(
                        "'" + searchterm + "' occurs " + str(term_frequency_dictionary[searchterm]) + " times.")
                # If not, display an error message.
                else:
                    message = "'" + searchterm + "' was not found.\n Please try again."
                    self.term_frequency.set(message)
        except FileNotFoundError:
            self.file_name.set("No file was selected.\n Please try again.")

    # Creating a term frequency dictionary from the selected file.
    # Each word in the file is a key in the dictionary, and its frequency is its value.
    # The normalize_text function is used to normalize the words in the file.
    # This function creates a list of the normalized words from a line, and is used to create the dictionary.
    def create_term_frequency_dictionary(self, filename):
        # Initiating an empty dictionary and an empty list.
        term_frequency_dictionary = {}
        word_list = []

        # Opening the file.
        search_file = open(filename, 'r')

        # Employing the normalize_text function to clean up the text and to split it into words.
        # Returns a word list.
        for line in search_file:
            words = self.normalize_text(line)
            for word in words:
                word_list.append(word)

        # Counter for the terms in the word list.
        for word in word_list:
            if word not in term_frequency_dictionary:
                term_frequency_dictionary[word] = 1
            else:
                term_frequency_dictionary[word] += 1

        return term_frequency_dictionary

    # Creating a list of normalized words from a line of text.
    # Normalized words are lower case and contain no punctuation.
    # This function was not modified.
    def normalize_text(self, line_of_text):
        normalized_word_list = []
        line_of_text = line_of_text.strip()  # remove whitespace
        word_list = line_of_text.split()  # create list of words
        for word in word_list:
            normalized_word = word.strip(string.punctuation).lower()
            # if NOT an empty string, append to the list
            if normalized_word:
                normalized_word_list.append(normalized_word)
        return normalized_word_list

#Calling the GUI
TermFrequencyGUI()
