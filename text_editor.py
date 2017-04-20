# -*- coding: utf-8 -*
from  Tkinter import *
from tkFileDialog import *
from n_gram_lang_model import bigram_lm as lm

class Text_Editor(object):
    """
    Create text editor that interacts with the Language model to return predicted next word.
    Inserts word into text editor and returns a prediction of next words

    """
    def __init__(self, master):
        self.text = Text(master)
        self.text.bind('<Key>', self.callback)
        self.text.pack()
        self.text.focus()
        self.word = ''
        self.filename = None
        # Create instance of Language model
        self.language_model = lm('corpus')
        self.next_word = []
        self.previous_ten_words = []
        self.list_of_predictions = []

    def newFile(self):
        """
        creates new file
        :return:
        """
        self.filename = "Untitled"
        self.text.delete(0.0, END)

    def savefile(self):
        """
        saves file
        :return:
        """
        self.filename = "Untitled"
        t = self.text.get(0.0, END)
        f = open(self.filename, 'w')
        f.write(t)
        f.close()

    def save_as(self):
        """
        save file as
        :return:
        """
        f = asksaveasfile(mode="w", defaultextension='.txt')
        t = self.text.get(0.0, END)
        try:
            f.write(t.rstrip())
        except:
            "oops... Unable to save file..."

    def openFile(self):
        """
        open saved file
        :return:
        """
        f = askopenfile(mode = "r")
        t = f.read()
        self.text.delete(0.0, END)
        self.text.insert(0.0, t)

    # interact with language model
    def callback(self, event):
        """
        on keyboard event record charracter if space save as word.
        :param event:
        :return:
        """
        print('{k!r}'.format(k=event.char))
        character = '{k!r}'.format(k=event.char)
        if character[1] == ' ':
            self.save_ten_words()
            self.pop_list()
        elif(character[1].isalpha()):
            self.word += character[1]

    def pop_list(self):
        """
        populate the list with predicted next words
        :return:
        """
        self.next_word = []
        Word_Prediction_List.delete(0, END)
        if len(self.previous_ten_words) >= 2:
            self.next_word.extend(self.language_model.nextword(self.previous_ten_words[-1], self.previous_ten_words[-2]))
            print self.next_word
        if len(self.previous_ten_words) >= 1 or self.next_word == None:

            self.next_word.extend(self.language_model.nextword(self.previous_ten_words[-1]))
        nums = 0
        for word in self.next_word:
            if len(word) == 4:
                self.list_of_predictions.append(word[2])
                Word_Prediction_List.insert(nums, word[2])
            if len(word) == 3:
                self.list_of_predictions.append(word[1])
                Word_Prediction_List.insert(nums, word[1])
            nums += 1
        self.word = ''

    def save_ten_words(self):
        """
        saves the previous 10 words in prep for more advanced language models
        :return:
        """
        if len(self.previous_ten_words) <= 10:
            self.previous_ten_words.append(self.word)
        elif len(self.previous_ten_words) > 10:
            self.previous_ten_words.pop(0)
            self.previous_ten_words.append(self.word)


    def enters_chosen_word_from_ddl(self, event):
        """
        On selecting element from list enter into text and repopulate list with new predictions
        :param event:
        :return:
        """
        #### change for trigram
        self.text.insert(INSERT, ' ' + self.list_of_predictions[Word_Prediction_List.curselection()[0]])
        self.word = self.list_of_predictions[Word_Prediction_List.curselection()[0]]
        self.save_ten_words()
        self.list_of_predictions = []
        self.pop_list()


root = Tk()
text_editor = Text_Editor(root)

root.title("My python text editor")
root.minsize(width=400, height=400)
root.maxsize(width=800, height=800)
menubar = Menu(root)
filemenu = Menu(menubar)
filemenu.add_command(label="New", command=text_editor.newFile)
filemenu.add_command(label="Open", command=text_editor.openFile)
filemenu.add_command(label="Save", command=text_editor.savefile)
filemenu.add_command(label="Save as ...", command=text_editor.save_as)
filemenu.add_command(label="Quit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_separator()

Word_Prediction_List = Listbox(root, width=63, height=10)
Word_Prediction_List.bind('<<ListboxSelect>>', text_editor.enters_chosen_word_from_ddl)
Word_Prediction_List.place(x=32, y=90)

Word_Prediction_List.pack()
root.mainloop()
