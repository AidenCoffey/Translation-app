from tkinter import *
import googletrans
from googletrans import Translator
import textblob
from tkinter import ttk, messagebox
import threading 
from threading import Thread
import math

#sets up the page with title and size of the page and defines what the page is
page = Tk() 
page.title("Translator")
page.geometry("1440x1080")

#call this definition to make the code for the translation defintion to work
translator = Translator()

#this translation definition makes the code print in the tree
def translation(word, index):
    retranslated_word = translator.translate(word, src=to_language_key, dest=from_language_key)
    retranslated_words_array[index] = retranslated_word

#This transaltion definition is the big one that has the processing speed and evreything involved
def translate_it():
    #delete any previous translations
    finish.delete(1.0,END)
    try:
        #This sets the key for our input value and language so that we are able to hold our stuff
        for key, value in languages.items():
            if (value == language_choice.get()):
                global from_language_key
                from_language_key = key
        
        #This sets the key for our output value and language so that we are able to hold our stuff
        for key, value in languages.items():
            if (value == translated_choice.get()):
                global to_language_key
                to_language_key = key
        
        #save the starting text into a global for the swap button to work
        global original_text
        original_text = start.get(1.0, END)

        #turns the origional text into a text blob and saves them to be used in the translator function to show line by line how it works
        words = textblob.TextBlob(start.get(1.0, END))
        
        #translates text from each word and saves the variable
        words = words.translate(from_language_key, to_language_key)

        #output translated text into the big transalion box
        finish.insert(1.0, words)

#This is now the end of the simple transaltion the next stuff is about speed and how to be percice with direct transaltion

        #saves the transalated words that we got from above into its own array
        translated_words_array = words.split()

#this information is about the speed of the translation

        #sets the number of threads to determine how fast or slow the program will be

        num_threads = 3
        twa = len(translated_words_array)

        #globalizes RTA so that it can be used in the def translation
        global retranslated_words_array
        retranslated_words_array = [""] * twa

        #create a list of each individual word that is being imputted to be used to compare
        translated_words_array = words.split()

        # says that is you are only translating one word or 2 it will set the num thread to that number so that it doesnt break
        if num_threads > twa:
            num_threads = twa
        
        #Initializes the threads list to be the same length as translated words array without using an .append()
        threads = [""] * len(translated_words_array)

#this is where we are using the code to actually translate the information back from the language we selected into 
        
        #Creates a thread object called thread for each word in the TWA that executes translation()
        #thread is then saved to the threads[list] at a position based on index, or how many times the for loop has ran
        for index, i in enumerate(translated_words_array):
            thread = threading.Thread(target=lambda: translation(i, index))
            threads[index] = thread
            threads[index].start()
        
        #this code is to print the words learned into the tree 
        soup = math.ceil(twa/num_threads)
        startingpoint = 0
        counter = 0
        for i in range(num_threads):
            thread = threading.Thread(target=lambda: translation(translated_words_array[startingpoint: soup], startingpoint))
            threads[counter] = thread
            threads[counter].start()
            startingpoint = soup
            soup += soup
            counter += 1 

        #Ensures that every thread in threads has finished before attempting to use any results from a thread
        for j in threads:
            j.join()

        #sets the spaceing and end print for what language is being inputted and outputted in the heading of the tree
        cols = (from_language_key, to_language_key)
        for index, col in enumerate(cols):
            tree.heading(index, text=col)

        #sets the base information for the tree
        tree.grid(row=5, column=2, columnspan=1)

        #Sets the insert for what langauge you are printing but in CAPS so that you can tell what language is what
        tree.insert("", "end", values=(from_language_key.upper(),to_language_key.upper()))
        
        #This is our actual words being outputted
        for i in range(len(retranslated_words_array)):
            tree.insert("", "end", values=(retranslated_words_array[i].text, translated_words_array[i]))
        
        #this is a blank space to seperate
        tree.insert("","end")
      
        #this is straight forward it is just updating the desciption label
        #update_description_label()
        '''this is commented out as of right now due to the in accuracy with threading
        it makes the code run really slow and it annoys me, i will work on it when i feel like it'''
        
    #error box if there is an issue
    except Exception as e:
        messagebox.showerror("Translate",e)

#end of our translate_it

#define the description label to know what words mean what specifically
def update_description_label():
    #take the language that there is already and write it down
    from_lang = language_choice.get()
    to_lang = translated_choice.get()
    transalted_sentance = "This translates from {} to {}\n".format(from_lang, to_lang)

    try:
        # Take the sentance that is printed above and then say it in the language that it is being transalted from
        # assuming that the lanugage you are coming from would be your primary language
        translated_description = googletrans.Translator().translate(transalted_sentance, src=to_lang, dest=from_lang)
        description_label.config(text=translated_description.text)
    except Exception as e:
        # just a fail safe
        description_label.config(text=transalted_sentance)


#clear button to clear the input and the output 
def clear():
    #call global to set the origional text back to nothgin so when you press the swap button there isnt anything 
    global original_text  
    original_text = ""    
    start.delete(1.0, END)
    finish.delete(1.0, END)

#create a swap button that will change our finihsed language to the starting langue so we can translate easier
def swap():
    # Swap the values of the language_choice and translated_choice comboboxes
    from_lang = language_choice.get()
    to_lang = translated_choice.get()
    language_choice.set(to_lang)
    translated_choice.set(from_lang)

    # Swap the language keys as well
    global from_language_key, to_language_key
    from_language_key, to_language_key = to_language_key, from_language_key

    # Swap the text in the input and output text widgets
    input_text = start.get(1.0, END)
    start.delete(1.0, END)
    finish_text = finish.get(1.0, END)
    finish.delete(1.0, END)
    start.insert(1.0, finish_text)
    finish.insert(1.0, input_text)

#this is a defenitiion to clear all the words that we have learned
def clear_words():
    #clears the description list title
    description_label.config(text="")
    #clears the tree holding the words learned and sets the heading back to the origional
    for item in tree.get_children():
        tree.delete(item)
        tree.heading("Input Language", text="Input Language")
        tree.heading("Output Language", text="Output Language")

# this is for the search function for the combo box
def check_input(event):
    value = event.widget.get()
    # this just calls the list and seaches through the array for the language choice combobox
    if value == '':
        language_choice['values'] = language_list
    else:
        data = []
        for item in language_list:
            if value.lower() in item.lower():
                data.append(item)

        language_choice['values'] = data
    # this just calls the list and seaches through the array for the Transalted choice combobox
    if value == '':
        translated_choice['values'] = language_list
    else:
        data = []
        for item in language_list:
            if value.lower() in item.lower():
                data.append(item)

        translated_choice['values'] = data

#language list
languages = googletrans.LANGUAGES
language_list = list(languages.values())

#input text and textbox 
start = Text(page, height=15, width = 76)
start.grid(row=0, column=0, pady=20, padx=20)

#translate button
button = Button(page, text="Translate!", font=(24), command=translate_it)
button.grid(row=0, column=1, padx=20)

#trasnalted text and textbox
finish = Text(page, height=15, width = 76)
finish.grid(row=0, column=2, pady=20, padx=20)

#choice of inputted language
language_choice = ttk.Combobox(page, width=50, value=language_list)
language_choice.current(21)
language_choice.grid(row=1, column=0)
language_choice.bind('<KeyRelease>', check_input)

#choice of outputted language
translated_choice = ttk.Combobox(page, width=50, value=language_list)
translated_choice.current(30)
translated_choice.grid(row=1, column=2)
translated_choice.bind('<KeyRelease>', check_input)

#clear button for the text
clear_button = Button(page, text="clear text", command=clear)
clear_button.grid(row=3, column=0)

#holds the words in the lsit
description_label = ttk.Label(page, justify=RIGHT)
description_label.grid(row=4, column=2, pady=5)

#a button to clear all the learned words 
clear_words_button = Button(page, text="clear word list", command=clear_words)
clear_words_button.grid(row=3, column=2)

#this is the swap button propsed by my friend greek and I told him I would name it after him in his honor
greek_switch = Button(page, text="Swap", command=swap)
greek_switch.grid(row=1, column=1, pady=10)

#this is the words learned section
cols = ("Input Language", "Output Language")
tree = ttk.Treeview(page, columns=cols, show="headings", height=18)
for col in cols:
    tree.heading(col, text=col, anchor="center")
tree.grid(row=5, column=2, columnspan=1)

#scroll bar for words learned section
tree_scrollbar = ttk.Scrollbar(page, orient="vertical", command=tree.yview)
tree_scrollbar.place(x=1320, y=385, height=386)
tree.configure(yscrollcommand=tree_scrollbar.set)

page.mainloop()

'''
Reference:
https://www.youtube.com/watch?v=64f5fKBM3-o
Cheesewheel23
Stacked Overflow
Chat GPT
Python.com
Textblob.com
googletrans.com
Threading.com
tkinter.com
'''

#end of code
