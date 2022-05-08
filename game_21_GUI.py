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
increase_points = 1

def get_name():
    res = "Hello {}".format(txt.get())
    name.configure(text=res)

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

my_cards = []

def get_my_points():
    # Определение карт и очков игрока

    my_cards.append(deal())
    my_points = count_points(my_cards)

    for i in range(len(my_cards)):
        # моя карта
        lbl = Label(window, text=my_cards[i])
        lbl.grid(column=0, row=3+i)

    lbl = Label(window, text=f"You have {my_points} points")
    lbl.grid(column=0, row=8)

    if my_points > 21:
        lbl = Label(window, text="Too many. You loose")
        lbl.grid(column=1, row=10)
        my_points = 0

    return my_points

pc_cards = []
def get_pc_points():

    # Определение карт компьютера
    while True:
        # карта PC
        pc_cards.append(deal())
        pc_points = count_points(pc_cards)

        for i in range(len(pc_cards)):

            lbl = Label(window, text=pc_cards[i])
            lbl.grid(column=4, row=3+i)

        if pc_points > 21:
            lbl = Label(window, text="PC got too many. PC loose")
            lbl.grid(column=4, row=10)
            pc_points = 0
            break

        if pc_points >= 17:
            lbl = Label(window, text=f"PC got {pc_points}.")
            lbl.grid(column=5, row=8)
            break

    return pc_points

def get_points():
    # кнопка - взять еще карту
    # раздача сразу 2 карты
    for i in range(2):
        get_my_points()
    btn = Button(window, text="Take card", command=get_my_points)
    btn.grid(column=0, row=2)

    # кнопка - достаточно карт
    btn = Button(window, text="Enough", command=get_pc_points)
    btn.grid(column=1, row=2)


def get_winner():
    global my_total_points
    global pc_total_points
    global increase_points

    # Определение победителя
    my = get_points()
    pc = get_points()


    if my > pc:
        my_total_points += 1 * increase_points
        increase_points = 1
        lbl = Label(window, text="You win")
        lbl.grid(column=1, row=12)
    elif my == pc:
        increase_points = 2
        lbl = Label(window, text="Nobody win. Next draw with double points")
        lbl.grid(column=1, row=12)
    else:
        pc_total_points += 1 * increase_points
        increase_points = 1
        lbl = Label(window, text="PC win")
        lbl.grid(column=4, row=12)

    total_score = f"{name} {my_total_points} : PC {pc_total_points}"
    print(total_score)
    return increase_points

window = Tk()
window.title("21")
window.geometry("400x300")

name = Label(window, text="What is your name? ")
name.grid(column=0, row=0)
txt = Entry(window, width=10)
txt.grid(column=1, row=0)
txt.focus()
#name = Entry(window, width=10, state='disabled')

# ввод имени
btn = Button(window, text="Ok", command=get_name)
btn.grid(column=2, row=0)

# общий счет - мои очки
lbl = Label(window, text = my_total_points)
lbl.grid(column=0, row=1)

# общий счет - очки компьютера
lbl = Label(window, text=pc_total_points)
lbl.grid(column=1, row=1)

get_points()

#get_winner()
window.mainloop()