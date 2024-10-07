from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = ("Arial", 40, "italic")
WORD_FONT = ("Arial", 80, "bold")
current_card = {}
learn_words = {}

# ---------------------------- FIXING FILE BUG ------------------------------- #
#When first executing the code, words_to_learn.csv does not exist yet, so it will present an error.
#The below exception helps to fix this error.

try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("./data/french_words.csv")
else:
    learn_words = data.to_dict(orient="records")


# ---------------------------- FLASHCARD FUNCTIONS ------------------------------- #
#The next_card function is activated when the red X button is pressed by the user.
#This function moves on to the next card with a different set of vocabulary words.
#The flip_timer is a three second delay that has been added to the front side of the card.
#This holds the French side if the card for three seconds before flipping to the English side of the card.

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(learn_words)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=front_card)
    flip_timer = window.after(3000, func=flip_card)

#The flip_card function what happens after the three second delay on the French side of the flash card.
#This changes the color of the words on the card and the card image.

def flip_card():
    global current_card
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=back_card)

#The is_known function is called when the green checkmark button is clicked.
#This function takes the current word on the cards and removes it from the csv file being used to run through the flashcards
#It is being removed because the user knows this word and doesn't need it to keep popping up.
#The next_card function is then called within this function, so the user can see the next card.

def is_known():
    learn_words.remove(current_card)
    data = pandas.DataFrame(learn_words)
    data.to_csv("./data/words_to_learn.csv", index=False)

    next_card()


#------------------------- UI DESIGN --------------------------- #
#This is where I created the window where my canvas will sit. The canvas holds my cards as well as my buttons.
#I added 50 points of padding to give room between the canvas and the edges of the window.

window = Tk()
window.title("Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

#This is a global variable that I created to allow a three second delay on the front of my cards before they flip.
#flip_timer is called up above in my functions.

flip_timer = window.after(3000, func=flip_card)

# ---------------------------- CANVAS ------------------------------- #
#I added the images of my front and back cards as well as set the size of my canvas to be the exact size as my card images.
#My flashcards always begin on the front and my canvas is configured later to shw my back_car when the card is flipped.
#I used a grid layout so I could position the items where I wanted them to be.

canvas = Canvas(width= 800, height= 526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_card = PhotoImage(file="./images/card_front.png")
back_card = PhotoImage(file="./images/card_back.png")
card_background = canvas.create_image(400, 263, image=front_card)
canvas.grid(column=0, columnspan=2, row=0)
#------------------------- TEXT ON CANVAS --------------------------- #
#This is where I added text on my cards and my functions configure the text to change.
#The title changes to either French or English adn the word changes to a random French word or what it means in English.

card_title = canvas.create_text(400, 150, text="", font=TITLE_FONT)
card_word = canvas.create_text(400, 300, text="", font=WORD_FONT)



#------------------------- BUTTONS --------------------------- #
#I made my X and Checkmark buttons here and gave them images or a red X and  green checkmark.
#The X button uses the next_card function to move on to the next card.
#The checkmark button uses the is_known function to remove the word from the group of words to learn and then moves to the next card.

x_button = PhotoImage(file="./images/wrong.png")
wrong = Button(image=x_button, highlightthickness=0, command=next_card)
wrong.grid(column=0, row=1)

check_button = PhotoImage(file="./images/right.png")
right = Button(image=check_button, highlightthickness=0, command=is_known)
right.grid(column=1, row=1)



next_card()

#This mainloop keep the window up and working instead of it quickly flashing up and then going away.
window.mainloop()