"""Game BlackJack (21, point)"""
# Игра "Очко" ("21" или BlackJack) с использованием Tkinter

from tkinter import*
from random import randint
import json

# Масти и номиналы карт
card_suits = ['Diamonds', 'Hearts', 'Clubs', 'Spades']
card_values = ['Ace', 'King', 'Queen', 'Jack', '10', '9', '8', '7', '6', '5', '4', '3', '2']
# розданные карты
cards = []
# Общий счет игры
my_total_points = 0
pc_total_points = 0
# разница между my_total_points и pc_total_points
balance = 0
# лучшая разница в истории
filename = 'record.json'
with open(filename) as f:
    best_balance = json.load(f)
# карты игрока и компьютера
my_cards = []
pc_cards = []
# выведенные на экран надписи
lbls = []
# коэффицент начисления очков за победу
increase_points = 1
# имя игрока
player_name = ""
# имя игрока с лучшим результатом
best_player = ""


def deal():
    # Сдача карты
    while True:
        # случайная масть
        random_suit = randint(0, 3)
        # случайный номинал карты
        random_value = randint(0, 12)
        card = f"{card_values[random_value]} of {card_suits[random_suit]}"
        # проверяю, если такая карта уже была выдана, то выдается заново
        if card in cards:
            cards.remove(card)
        # если не выдана, то добавляем к выданным
        else:
            cards.append(card)
            return card


def count_points(value):
    # Определение кол-ва очков в зависимости от номинала карты по первой букве card
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


def get_my_cards():
    # набор карт игрока
    global pc_total_points
    global balance

    # кнонка play again пока недоступна
    btn_clear.config(state='disabled')
    # вызываю функцию deal, чтобы выдать мне карту
    my_cards.append(deal())
    # рассчитываем кол-во очков в зависмоати от выданной карты
    my_points = count_points(my_cards)
    # если очков достаточно - нажимаем кнопку Enough
    btn_enough = Button(window, text="Enough", width=16, command=lambda: get_pc_cards(my_points))
    btn_enough.grid(column=1, row=3)

    for i in range(len(my_cards)):
        # вывожу на экран мои карты
        lbl = Label(window, text=my_cards[i])
        lbl.grid(column=0, row=4 + i)
        # вывод на экран добавляется в список надписей
        lbls.append(lbl)
        # вывожу на экран кол-во очков
        lbl = Label(window, text=f"You got {my_points} points")
        lbl.grid(column=0, row=10)
        # вывод на экран добавляется в список надписей
        lbls.append(lbl)

    if my_points > 21:
        # если кол-во очков больше 21 - проигрыш -перебор
        lbl = Label(window, text=f"Too many. You loose")
        lbl.grid(column=0, row=10)
        # вывод на экран добавляется в список надписей
        lbls.append(lbl)
        # кнопки Take card и Enough не активны
        btn_take.config(state='disabled')
        btn_enough.config(state='disabled')
        # общий счет добавляется в пользу pc с учетом коэффицента
        pc_total_points += 1 * increase_points
        balance = my_total_points - pc_total_points
        # кнопка play_again снова активна
        btn_clear.config(state='normal')
        # переход в функцию, отображающую общий счет
        show_total_score()


def get_pc_cards(my_points):
    # набор карт компа
    global my_total_points
    global pc_total_points
    global increase_points
    global balance
    # кнопка take отключена
    btn_take.config(state='disabled')
    btn_enough = Button(window, text="Enough", width=16, command=get_pc_cards)
    btn_enough.grid(column=1, row=3)

    # Определение карт компьютера
    while True:
        # карта PC
        pc_cards.append(deal())
        pc_points = count_points(pc_cards)

        for i in range(len(pc_cards)):
            # вывод на экран карт PC
            lbl = Label(window, text=pc_cards[i])
            lbl.grid(column=1, row=4 + i)
            # все надписи на экране добавляются в список
            lbls.append(lbl)

        if pc_points > 21:
            # если у PC перебор
            lbl = Label(window, text="Too much")
            lbl.grid(column=1, row=10)
            my_total_points += 1 * increase_points
            balance = my_total_points - pc_total_points
            lbls.append(lbl)
            show_total_score()
            break

        elif pc_points >= 17:
            # если у pc очков более 17 - больше не набирает карты
            lbl = Label(window, text=f"PC got {pc_points}.")
            lbl.grid(column=1, row=10)
            lbls.append(lbl)
            # определение победителя
            if my_points > pc_points:
                # к общему счету игрока прибавляется 1
                my_total_points += 1 * increase_points
                balance = my_total_points - pc_total_points
                show_total_score()
            elif my_points == pc_points:
                # при равном кол-ве очков ставка увеличивается в 2 раза
                increase_points *= 2
                lbl = Label(window, text='Nobody win\n double points\n next deal')
                lbl.grid(column=1, row=14)
                btn_enough.config(state='disabled')
                btn_clear.config(state='normal')
                lbls.append(lbl)
                show_total_score()
                return increase_points

            else:
                pc_total_points += 1 * increase_points
                balance = my_total_points - pc_total_points
                show_total_score()
            break

    btn_enough.config(state='disabled')
    btn_clear.config(state='normal')


def show_total_score():
    global best_balance
    # общий счет - мои очки
    my_total = Label(window, text=my_total_points)
    my_total.grid(column=0, row=2)
    # общий счет - очки компьютера
    pc_total = Label(window, text=pc_total_points)
    pc_total.grid(column=1, row=2)
    # баланс - разница между очками игрока и PC
    total_balance = Label(window, text=balance)
    total_balance.grid(column=2, row=2)


    # определяю если текущий баланс лучще рекордного баланса
    if balance > best_balance:
        best_balance = balance
        show_best_records()


def play(lbls):
    # новая раздача
    global my_cards
    global pc_cards
    # карты игрока и PC обнуляются
    my_cards = []
    pc_cards = []
    # стираю с экрана карты с предыдущей раздачи
    for lbl in lbls:
        lbl.destroy()
    # кнопка Take card активна
    btn_take.config(state='normal')

def init_name():
    # ввод имени игрока
    # запрос имени игрока
    lbl_name = Label(window, text="What is your name?")
    lbl_name.grid(column=0, row=0)
    # окно ввода
    name_entry = Entry(textvariable=player_name, width=20)
    name_entry.grid(column=1, row=0)
    # установка курсора в поле ввода
    name_entry.focus()
    # кнопка подтверждения имени -> функция активирует кнопку Take card
    name_btn = Button(text="0K", width=16, command=lambda: btn_take_normal(lbl_name, name_btn, name_entry))
    name_btn.grid(column=2, row=0)


def btn_take_normal(lbl_name, name_btn, name_entry):
    global player_name
    # инициализация имени игрока
    player_name = name_entry.get()
    # убираю с экрана все поля, связанные с вводом имени игрока
    lbl_name.destroy()
    name_btn.destroy()
    name_entry.destroy()
    # вместо поля для ввода имени вывожу приветствие
    lbl = Label(window, text=f"Good luck {player_name}!")
    lbl.grid(column=0, row=0)
    # кнопка Take card становится активной после ввода имени игрока
    btn_take.config(state='normal')


def show_best_records():

    # Вывод лучшего результата
    #best_player = player_name
    #record = f"Best balance: {best_player} {best_balance}"
    record = best_balance
    filename = 'record.json'
    with open(filename, 'w') as f:
        json.dump(record, f)


window = Tk()
window.title("21")
window.geometry("370x330")

init_name()


lbl = Label(window, text=f"Best balance: {best_balance}")
# lbl = Label(window, text=f"Best balance: {best_player} {best_balance}")
lbl.grid(column=0, row=20)

# кнопка Take card - взять еще карту игроку
btn_take = Button(window, text="Take card", width=16, command=get_my_cards)
btn_take.grid(column=0, row=3)
btn_take.config(state='disabled')

# кнопка Enough - игроку больше не нужно карт, ход переходит к PC
btn_enough = Button(window, text="Enough", width=16, command=get_pc_cards)
btn_enough.grid(column=1, row=3)
btn_enough.config(state='disabled')

# вывод общего счета
lbl = Label(window, text="your total score")
lbl.grid(column=0, row=1)
lbl = Label(window, text="pc total score")
lbl.grid(column=1, row=1)
lbl = Label(window, text="balance")
lbl.grid(column=2, row=1)

# кнопка Play again - карты обнуляются, новая сдача
btn_clear = Button(window, text="Play again", width=16, command=lambda: play(lbls))
btn_clear.grid(column=2, row=3)

# общий счет всей игры
show_total_score()

# главный цикл игры
window.mainloop()