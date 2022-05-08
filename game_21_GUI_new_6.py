"""Game BlackJack (21, point)"""

from tkinter import*
from random import randint
import sys

# Масти и номиналы карт
card_suits = ['Diamonds', 'Hearts', 'Clubs', 'Spades']
card_values = ['Ace', 'King', 'Queen', 'Jack', '10', '9', '8', '7', '6', '5', '4', '3', '2']
# розданные карты
cards = []

# Счет игры
my_total_points = 0
pc_total_points = 0


def deal():
    # Сдача карты
    while True:
        random_suit = randint(0, 3)
        random_value = randint(0, 12)
        card = f"{card_values[random_value]} of {card_suits[random_suit]}"
        # проверяю, если такая карта уже была выдана, то выдается заново
        if card in cards:
            cards.remove(card)
        else:
            cards.append(card)
            return card

def count_points(value):
    # Определение кол-ва очков в зависимости от номинала карты по первой букве
    points = 0
    for x in value:
        if x[0] == 'A':
            points += 11
        if x[0] == 'K':
            points += 10
        if x[0] == 'Q':
            points += 10
        if x[0] == 'J':
            points += 10
        if x[0] == '1':
            points += 10
        if x[0] == '9':
            points += 9
        if x[0] == '8':
            points += 8
        if x[0] == '7':
            points += 7
        if x[0] == '6':
            points += 6
        if x[0] == '5':
            points += 5
        if x[0] == '4':
            points += 4
        if x[0] == '3':
            points += 3
        if x[0] == '2':
            points += 2

    return points

def play():
    btn_take.config(state='normal')
    btn_enough.config(state='normal')

my_cards = []

def get_my_cards():
    global pc_total_points
    my_cards.append(deal())
    my_points = count_points(my_cards)

    lbls = []

    for i in range(len(my_cards)):
        # моя карта
        lbl = Label(window, text=my_cards[i])
        lbl.grid(column=0, row=3 + i)
        lbl = Label(window, text=f"You got {my_points} points")
        lbl.grid(column=0, row=8)
        lbls.append(lbl)

    if my_points > 21:
        lbl = Label(window, text="Too many. You loose")
        lbl.grid(column=0, row=10)
        btn_take.config(state='disabled')
        btn_enough.config(state='disabled')
        pc_total_points += 1
        lbls.append(lbl)
        show_total_score()

        #play(lbls)

    return my_points, lbls

pc_cards = []

def get_pc_cards():
    global my_total_points
    global pc_total_points
    btn_take.config(state='disabled')


    lbls = []
    # Определение карт компьютера
    while True:
        # карта PC
        pc_cards.append(deal())
        pc_points = count_points(pc_cards)

        for i in range(len(pc_cards)):
            lbl = Label(window, text=pc_cards[i])
            lbl.grid(column=1, row=3 + i)
            lbls.append(lbl)

        if pc_points > 21:
            lbl = Label(window, text="PC got too many. PC loose")
            lbl.grid(column=1, row=10)
            my_total_points += 1
            lbls.append(lbl)
            show_total_score()
            break

        elif pc_points >= 17:
            lbl = Label(window, text=f"PC got {pc_points}.")
            lbl.grid(column=1, row=8)
            lbls.append(lbl)
            if my_points > pc_points:
                my_total_points += 1
                show_total_score()
            else:
                pc_total_points += 1
                show_total_score()
            break

    btn_enough.config(state='disabled')
    return pc_points, lbls

def show_total_score():
    # общий счет - мои очки
    my_total = Label(window, text=my_total_points)
    my_total.grid(column=0, row=1)
    # общий счет - очки компьютера
    pc_total = Label(window, text=pc_total_points)
    pc_total.grid(column=1, row=1)

def play_again(lbls):
    for lbl in lbls:
        lbl.destroy()

window = Tk()
window.title("21")
window.geometry("400x300")
lbl = Label(window, text="")

# кнопка - взять еще карту
btn_take = Button(window, text="Take card", command=get_my_cards)
btn_take.grid(column=0, row=2)
btn_take.config(state='disabled')

btn_enough = Button(window, text="Enough", command=lambda: get_pc_cards(my_points))
btn_enough.grid(column=1, row=2)
btn_enough.config(state='disabled')

btn_clear = Button(window, text="Play", command=play)
btn_clear.grid(column=1, row=12)

btn_clear = Button(window, text="Play again", command=play_again)
btn_clear.grid(column=0, row=12)
btn_clear.config(state='disabled')

show_total_score()
window.mainloop()