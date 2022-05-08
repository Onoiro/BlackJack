#Import the tkinter library
from tkinter import *

#Create an instance of tkinter frame
win = Tk()

#Set the geometry
win.geometry("600x250")

#Define a function to clear the input text
def clearToTextInput(my_text):
   my_text.delete("1.0","end")

def create_text():
    #Create a text widget
    my_text=Text(win, height=10)
    my_text.pack()
    return my_text

#Create a Button
btn=Button(win,height=1,width=10, text="Clear",command=lambda: clearToTextInput())
btn.pack()

create_text()
#Display the window without pressing key
win.mainloop()