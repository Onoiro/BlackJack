from tkinter import*
from random import randint

window = Tk()
window.title("test")
window.geometry("100x200")

# Масти и номиналы карт
card_suits = ['Diamonds', 'Hearts', 'Clubs', 'Spades']
card_values = ['Ace', 'King', 'Queen', 'Jack', '10', '9', '8', '7', '6', '5', '4', '3', '2']

def deal():
    # Сдача карты
    random_suit = randint(0, 3)
    random_value = randint(0, 12)
    card = f"{card_values[random_value]} of {card_suits[random_suit]}"
    return card

def show_card():
    my_card = deal()
    lbl = Label(window, text=my_card)
    lbl.pack()
    btn_clear = Button(window, text="Clear card", command=lambda: clear_card(lbl, btn_clear))
    btn_clear.pack()

def clear_card(label, button):
    label.destroy()
    button.destroy()

btn_take = Button(window, text="Take card", command=show_card)
btn_take.pack()

lbl = Label(window, text="")
window.mainloop()