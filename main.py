from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import Button

import sys


from transformers import BertTokenizer, AutoModelForCausalLM, TextGenerationPipeline   

tokenizer = BertTokenizer.from_pretrained("gpt2-base")
model = AutoModelForCausalLM.from_pretrained("gpt2-base")

generator = TextGenerationPipeline(model=model, tokenizer=tokenizer, 
                                   max_new_tokens=100, 
                                   no_repeat_ngram_size=3, 
                                   do_sample=True, top_k=50, top_p=0.95, temperature=0.9)


class WriteWithTransformers():
    def __init__(self,):
        # Setup Variables
        self.appName = 'Wrtie with Transformer'
        self.nofileOpenedString = 'New File'

        self.currentFilePath = self.nofileOpenedString

        # Viable File Types, when opening and saving files.
        self.fileTypes = [("Text Files","*.txt")]


        # Tkinter Setup
        self.window = Tk()

        self.window.title(self.appName + " - " + self.currentFilePath)

        # Window Dimensions in Pixel
        self.window.geometry('700x400')

        # Set the first column to occupy 100% of the width
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        
        self.default_font = 15
        self.font_size = 15
        self.txt = scrolledtext.ScrolledText(self.window, font=("Helvetica", self.font_size))
        self.txt.grid(column=0, row=0, sticky='nsew')
        
        self.cache = ""
        self.txt.bind("<KeyRelease>", self.textchange)
        self.txt.bind("<Command-z>", self.redo)
        self.build()

    def fileDropDownHandeler(self, action):

        # Opening a File
        if action == "open":
            file = filedialog.askopenfilename(filetypes = self.fileTypes)
            self.window.title(self.appName + " - " + file)
            self.currentFilePath = file
            with open(file, 'r') as f:
                self.txt.delete(1.0,END)
                self.txt.insert(INSERT,f.read())

            # Making a new File
        elif action == "new":
            self.currentFilePath = self.nofileOpenedString
            self.txt.delete(1.0,END)
            self.window.title(self.appName + " - " + self.currentFilePath)

        # Saving a file
        elif action == "save" or action == "saveAs":
            if self.currentFilePath == self.nofileOpenedString or action=='saveAs':
                self.currentFilePath = filedialog.asksaveasfilename(filetypes = self.fileTypes)
            with open(self.currentFilePath, 'w') as f:
                f.write(self.txt.get('1.0','end'))
            self.window.title(self.appName + " - " + self.currentFilePath)
            
    def font_size_handler(self, action):
        if action == "increase":
            self.font_size = self.font_size + 5
            self.txt.config(font=("Helvetica", self.font_size))
        elif action == "decrease":
            self.font_size = self.font_size - 5
            self.txt.config(font=("Helvetica", self.font_size))
        elif action == "reset":
            self.font_size = self.default_font
            self.txt.config(font=("Helvetica", self.default_font))

    def generate_text(self, action):
        text = self.txt.get('1.0','end')
        if text[-1] == "\n":
            text = text[:-1]
        generated = generator(text)
        self.txt.delete(1.0,END)
        self.txt.insert(INSERT,generated[0]['generated_text'].replace(" ",""))
          
    def textchange(self, event):
        if self.cache!= self.txt.get('1.0','end')[:-1]:
            self.cache = self.txt.get('1.0','end')[:-1]
            self.window.title(self.appName + " - *" + self.currentFilePath)
        
    def redo(self, event):
        self.txt.delete(1.0,END)
        self.txt.insert(INSERT,self.cache)
        
    def build(self):
        # Menu
        self.menu = Menu(self.window)
        # set tearoff to 0
        self.fileDropdown = Menu(self.menu, tearoff=False)
        # Add Commands and and their callbacks
        self.fileDropdown.add_command(label='New', 
                                      command=lambda: self.fileDropDownHandeler("new"))
        self.fileDropdown.add_command(label='Open', 
                                      command=lambda: self.fileDropDownHandeler("open"))
        # Adding a seperator between button types.
        self.fileDropdown.add_separator()
        self.fileDropdown.add_command(label='Save', 
                                      command=lambda: self.fileDropDownHandeler("save"))
        self.fileDropdown.add_command(label='Save as', 
                                      command=lambda: self.fileDropDownHandeler("saveAs"))
        self.menu.add_cascade(label='File', 
                              menu=self.fileDropdown)

        self.fileDropdown2 = Menu(self.menu, tearoff=False)
        self.fileDropdown2.add_command(label='Increase Font Size', command=lambda: self.font_size_handler("increase"))
        self.fileDropdown2.add_command(label='Decrease Font Size', command=lambda: self.font_size_handler("decrease"))
        self.fileDropdown2.add_command(label='Reset Font Size', command=lambda: self.font_size_handler("reset"))
        self.menu.add_cascade(label='Font', menu=self.fileDropdown2)

        self.generate_button = Button(self.window, text="Generate Text", command=lambda: self.generate_text("generate"))
        self.generate_button.grid(row=1,sticky=N+S+E+W)

        # Set Menu to be Main Menu
        self.window.config(menu=self.menu)
        
        
app = WriteWithTransformers()
app.window.mainloop()