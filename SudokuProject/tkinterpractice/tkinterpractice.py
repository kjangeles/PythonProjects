# Check out effbot.org/tkinterbook for more details
import random
import tkinter as tk

window = tk.Tk()
window.title("My App")
window.geometry("400x400")   #dimension in pixels

#----FUNCTIONS----
def phrase_generator():    # on the Sudoku program this would be the puzgen

    phrases = ["Hello ", "What's Up? ", "Aloha ", "Kamusta! "]
    
    name = str(entry1.get())

    return phrases[random.randint(0,3)] + name

def phrase_display():     # on the sudoku program this would be display
    greeting = phrase_generator()
    
    greeting_display = tk.Text(master=window, height=10, width=30)
    greeting_display.grid(column=0, row=3)

    greeting_display.insert(tk.END, greeting)


#----LABEL----
label1 = tk.Label(text="Welcome to My App", font=("Times New Roman", 20))
label1.grid(column=0, row=0)

label2 = tk.Label(text="What is your name?")
label2.grid(column=0, row=1)

#----ENTRY FIELD----
entry1 = tk.Entry()
entry1.grid(column=1, row=1)

#----BUTTON----
button1 = tk.Button(text="Click me!", command=phrase_display)
button1.grid(column=0,row=2)

#----TEXT FIELDS----
#text_field = tk.Text(master=window, height=10, width=30)
#text_field.grid()


window.mainloop()

