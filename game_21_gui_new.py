"""Game BlackJack (21, point)"""

from tkinter import *
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
            break


def count_points(value, i):
    # Определение кол-ва очков в зависимости от номинала карты по первой букве
    points = 0
    for x in value[i]:
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


def get_my_points():
    # Определение карт игрока
    my_cards = []
    my_points = 0
    card_number = 0

    while True:
        # получаю карту с раздачи
        my_cards.append(deal())
        # добавляю кол-во очков, в зависимости от карты
        my_points += count_points(my_cards, card_number)
        card_number += 1
        # раздача сразу по 2 карты
        if card_number < 2:
            my_cards.append(deal())
            my_points += count_points(my_cards, card_number)
            card_number += 1
        print(f"{name} cards is: {my_cards}, {my_points} points")

        if my_points > 21:
            print('Too many - loose')
            my_points = 0
            break

        command = input('More or quit? (press Enter or "q") \n')
        if command == 'q':
            break
    return my_points

    def get_pc_points():
        # Определение карт компьютера
        pc_cards = []
        pc_points = 0
        card_number = 0

        while True:

            pc_cards.append(deal())
            pc_points += count_points(pc_cards, card_number)
            card_number += 1

            if pc_points > 21:
                print(f'PC get too many points: {pc_points}')
                pc_points = 0
                break

            if pc_points >= 17:
                break

        print(f"PC cards is: {pc_cards}, {pc_points} points \n")
        return pc_points

    def get_winner():
        global my_total_points
        global pc_total_points
        global increase_points
        # Определение победителя
        my = get_my_points()
        pc = get_pc_points()
        if my > pc:
            my_total_points += 1 * increase_points
            increase_points = 1
            print(name, ' win \n')
        elif my == pc:
            increase_points = 2
            print('Nobody win \nNext draw with double points')
        else:
            pc_total_points += 1 * increase_points
            increase_points = 1
            print("PC win \n")

        total_score = f"{name} {my_total_points} : PC {pc_total_points}"
        print(total_score)
        return increase_points


    get_winner()
    exit_game()


window = Tk()
window.title("21")
window.geometry("600x300")

name = Label(window, text="What is your name? ")
name.grid(column=0, row=0)
txt = Entry(window, width=10)
txt.grid(column=1, row=0)
txt.focus()
# name = Entry(window, width=10, state='disabled')

# ввод имени
btn = Button(window, text="Ok", command=get_name)
btn.grid(column=2, row=0)

# взять еще карту
btn = Button(window, text="Take card")
btn.grid(column=0, row=2)

# общий счет - мои очки
lbl = Label(window, text=my_total_points)
lbl.grid(column=0, row=1)

# общий счет - очки компьютера
lbl = Label(window, text=pc_total_points)
lbl.grid(column=1, row=1)



window.mainloop()

