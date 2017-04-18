# -*- coding: utf-8 -*
from  Tkinter import *
from tkFileDialog import *
from n_gram_lang_model import ngramlm as lm

class MyApp(object):
    def __init__(self, master):
        self.text = Text(master)
        self.text.bind('<Key>', self.callback)
        self.text.pack()
        self.text.focus()
        self.word = ''
        self.filename = None
        self.language_model = lm('corpus.txt')
        self.next_words = []


    def newFile(self):
        self.filename = "Untitled"
        self.text.delete(0.0, END)

    def savefile(self):
        self.filename = "Untitled"
        t = self.text.get(0.0, END)
        f = open(self.filename, 'w')
        f.write(t)
        f.close()

    def save_as(self):
        f = asksaveasfile(mode="w", defaultextension='.txt')
        t = self.text.get(0.0, END)
        try:
            f.write(t.rstrip())
        except:
            "oops... Unable to save file..."

    def openFile(self):
        f = askopenfile(mode = "r")
        t = f.read()
        self.text.delete(0.0, END)
        self.text.insert(0.0, t)

    # interact with language model
    def callback(self, event):
        print('{k!r}'.format(k=event.char))
        character = '{k!r}'.format(k=event.char)
        if character[1] == ' ':
            print self.word
            self.next_words = self.language_model.nextword(self.word)
            List1.delete(0, END)
            nums = 0
            for word in self.next_words:
                List1.insert(nums, word[1])
                nums += 1
            self.word = ''
        elif(character[1].isalpha()):
            self.word += character[1]

    def check_word_in_dictionary(self):
        """
        queries the dictionary for the previous word

        :return:
        """
        pass
    def drop_d_next_word_options(self):
        """
        gives a drop down list of possible next words
        :return:
        """
        pass
    def enters_chosen_word_from_ddl(self):
        pass
    def populatelist(self):
        nums = 1
        for word in self.next_words:
            List1.insert(nums, word[1])
            nums += 1

root = Tk()
app = MyApp(root)

root.title("My python text editor")
root.minsize(width=400, height=400)
root.maxsize(width=400, height=800)

menubar = Menu(root)
filemenu = Menu(menubar)
filemenu.add_command(label = "New", command=app.newFile)
filemenu.add_command(label = "Open", command=app.openFile)
filemenu.add_command(label = "Save", command=app.savefile)
filemenu.add_command(label = "Save as ...", command=app.save_as)
filemenu.add_command(label="Quit", command=root.quit)
menubar.add_cascade(label = "File", menu =filemenu)
filemenu.add_separator()

List1 = Listbox()
scrollbar = Scrollbar(List1, orient=VERTICAL)
List1.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=List1.yview)
app.populatelist()
List1.pack()
root.mainloop()

