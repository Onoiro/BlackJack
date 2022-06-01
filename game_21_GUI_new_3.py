"""Game BlackJack (21, point)"""
# Игра "Очко" ("21" или BlackJack) с использованием Tkinter

from tkinter import*
from random import randint
import json

# Масти и номиналы карт
card_suits = ['diamonds', 'hearts', 'clubs', 'spades']
card_values = ['ace', 'king', 'queen', 'jack', '10', '9', '8', '7', '6', '5', '4', '3', '2']
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

# имя игрока с лучшим результатом
#best_player = "Abo"
#filename = 'best_player.json'
#with open(filename, 'w') as f:
#    json.dump(best_player, f)

filename = 'best_player.json'
with open (filename) as f:
    best_player = json.load(f)
# карты игрока и компьютера
my_cards = []
pc_cards = []
# выведенные на экран надписи
lbls = []
# коэффицент начисления очков за победу
increase_points = 1
# имя игрока
player_name = ""


def deal():
    # Сдача карты
    while True:
        # случайная масть
        random_suit = randint(0, 3)
        # случайный номинал карты
        random_value = randint(0, 12)
        card = f"{card_values[random_value]}_of_{card_suits[random_suit]}"
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
        if x[0] == 'a':
            points += 11
        elif x[0] == 'k' or x[0] == 'q' or x[0] == 'j' or x[0] == '1':
            points += 10
        else:
            points += int(x[0])

    return points


def get_my_cards():
    # набор карт игрока
    global pc_total_points
    global balance

    # кнонка play again пока недоступна
    btn_clear.config(state='disabled')
    # вызываю функцию deal, чтобы выдать мне карту
    my_cards.append(deal())
    # рассчитываем кол-во очков в зависмости от выданной карты
    my_points = count_points(my_cards)
    # если очков достаточно - нажимаем кнопку Enough
    btn_enough = Button(window, text="Enough", font=15, width=16,
                        command=lambda: get_pc_cards(my_points))
    btn_enough.place(x=160, y=110, width=140)

    for i in range(len(my_cards)):
        # вывожу на экран мои карты
        lbl = Label(window, text=my_cards[i], font=15)
        lbl.place(x=10, y=150 + i*30)
        # вывод на экран добавляется в список надписей
        lbls.append(lbl)
        # вывожу на экран кол-во очков
        lbl = Label(window, text=f"You got {my_points} points", font=15)
        lbl.place(x=10, y=320)
        # вывод на экран добавляется в список надписей
        lbls.append(lbl)

    if my_points > 21:
        # если кол-во очков больше 21 - проигрыш -перебор
        lbl = Label(window, text=f"Too many. You loose", font=15)
        lbl.place(x=10, y=360)
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
    #btn_enough = Button(window, text="Enough", font=15, width=16, command=get_pc_cards)
    #btn_enough.place(x=160, y=110, width=140)

    # Определение карт компьютера
    while True:
        # карта PC
        pc_cards.append(deal())
        pc_points = count_points(pc_cards)

        for i in range(len(pc_cards)):
            # вывод на экран карт PC
            lbl = Label(window, text=pc_cards[i], font=15)
            lbl.place(x=160, y=150 + i*30)
            # все надписи на экране добавляются в список
            lbls.append(lbl)

        if pc_points > 21:
            # если у PC перебор
            lbl = Label(window, text=f"PC got {pc_points}.", font=15)
            lbl.place(x=160, y=320)
            lbls.append(lbl)
            lbl = Label(window, text="Too much",font=15 )
            lbl.place(x=160, y=360)
            my_total_points += 1 * increase_points
            balance = my_total_points - pc_total_points
            lbls.append(lbl)
            show_total_score()
            break

        elif pc_points >= 17:
            # если у pc очков более 17 - больше не набирает карты
            lbl = Label(window, text=f"PC got {pc_points}.", font=15)
            lbl.place(x=160, y=320)
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
                lbl = Label(window, text='Nobody win - double points next deal', font=15 )
                lbl.place(x=80, y=360)
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
    global best_player
    # общий счет - мои очки
    my_total = Label(window, text=my_total_points, font=15)
    my_total.place(x=10, y=80, width=140, height=30)
    # общий счет - очки компьютера
    pc_total = Label(window, text=pc_total_points, font=15)
    pc_total.place(x=160, y=80, width=140, height=30)
    # баланс - разница между очками игрока и PC
    total_balance = Label(window, text=balance, font=15)
    total_balance.place(x=310, y=80, width=140, height=30)

    # определяю если текущий баланс лучще рекордного баланса
    if balance > best_balance:
        best_balance = balance
        best_player = player_name
        best_records()


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
    # инициализация игрока и ввод имени
    # запрос имени игрока
    lbl_name = Label(window, text="What is your name?", font=15)
    lbl_name.place(x=10, y=10, width=140, height=30)
    # окно ввода
    name_entry = Entry(textvariable=player_name, width=20, font=15)
    name_entry.place(x=160, y=10, width=140, height=30)
    # установка курсора в поле ввода
    name_entry.focus()
    # кнопка подтверждения имени -> функция активирует кнопку Take card
    name_btn = Button(text="OK", font=15, width=16,
                      command=lambda: btn_take_normal(lbl_name, name_btn, name_entry))
    name_btn.place(x=310, y=10, width=140, height=30)


def btn_take_normal(lbl_name, name_btn, name_entry):
    global player_name
    global best_player
    # инициализация имени игрока
    player_name = name_entry.get()
    # убираю с экрана все поля, связанные с вводом имени игрока
    lbl_name.destroy()
    name_btn.destroy()
    name_entry.destroy()
    # вместо поля для ввода имени вывожу приветствие
    lbl = Label(window, text=f"Good luck {player_name}!", font=15)
    lbl.place(x=10, y=10)
    # кнопка Take card становится активной после ввода имени игрока
    btn_take.config(state='normal')


def best_records():
    # запись в файл лучшего баланса
    filename = 'record.json'
    with open(filename, 'w') as f:
        json.dump(best_balance, f)
    # запись в файл имя игрока с лучшим балансом
    filename = 'best_player.json'
    with open(filename, 'w') as f:
        json.dump(best_player, f)


window = Tk()
window.title("21")
window.geometry("460x460")
window.resizable(0, 0)

canvas = Canvas(window, width=460, height=460)
canvas.pack()

# показываю лучший баланс и имя лучшего игрока внизу игрового экрана
lbl = Label(window, text=f"Best balance: {best_player}  {best_balance}", font=15)
lbl.place(x=10, y=430)

# кнопка Take card - взять еще карту игроку
btn_take = Button(window, text="Take card", font=15, width=16, command=get_my_cards)
btn_take.place(x=10, y=110, width=140)
btn_take.config(state='disabled')

# кнопка Enough - игроку больше не нужно карт, ход переходит к PC
btn_enough = Button(window, text="Enough", font=15, width=16, command=get_pc_cards)
btn_enough.place(x=160, y=110, width=140)
btn_enough.config(state='disabled')

# вывод общего счета
lbl = Label(window, text="your total score", font=15)
lbl.place(x=10, y=50, width=140, height=30)
lbl = Label(window, text="pc total score", font=15)
lbl.place(x=160, y=50, width=140, height=30)
lbl = Label(window, text="balance", font=15)
lbl.place(x=310, y=50, width=140, height=30)

# кнопка Play again - карты обнуляются, новая сдача
btn_clear = Button(window, text="Play again", font=15, width=16,
                   command=lambda: play(lbls))
btn_clear.place(x=310, y=110, width=140)

# ввод имени игрока
init_name()
# общий счет всей игры
show_total_score()
# главный цикл игры
window.mainloop()