"""Game BlackJack (21, point)"""
# Игра "Очко" ("21" или BlackJack) с использованием Tkinter

from tkinter import*
from random import randint
import json
from tkinter import messagebox
from datetime import datetime, timedelta
import time


# Масти и номиналы карт
card_suits = ['diamonds', 'hearts', 'clubs', 'spades']
card_values = ['ace', 'king', 'queen', 'jack', '10', '9', '8', '7', '6', '5', '4', '3', '2']
# розданные карты
cards = []
# Общий счет игры
#my_total_points = 0
#pc_total_points = 0
# разница между my_total_points и pc_total_points
balance = 1
# лучший выигрыш в истории
filename = 'record.json'
with open(filename) as f:
    best_balance = json.load(f)

# имя игрока с лучшим результатом
#best_player = "Abo"
#filename = 'best_player.json'
#with open(filename, 'w') as f:
#    json.dump(best_player, f)

# имя игрока с лучшим выигрышем
filename = 'best_player.json'
with open (filename) as f:
    best_player = json.load(f)
# карты игрока и компьютера
my_cards = []
pc_cards = []
# выведенные на экран надписи
lbls = []
# коэффицент начисления очков за победу - ставка (bet)
bet = 1
# выигрыш за одну раздачу
gain = 0
# имя игрока
player_name = ""
blackjack = False
five_cards = False
six_cards = False
game_time = timedelta(minutes=0, seconds=0, milliseconds=0)
game_active = True


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
        # если карта ace (туз)
        if x[0] == 'a':
            # проверяю, если очков будет больше 21, то туз = 1 очко
            if (points + 11) > 21:
                points += 1
            # если очков будет меньше 21, то туз = 11 очков
            else:
                points += 11
        # если карты это "картинки" или "10", то прибавляем 10 очков
        elif x[0] == 'k' or x[0] == 'q' or x[0] == 'j' or x[0] == '1':
            points += 10
        # прибавляю очки в зависимости от номинала карты
        else:
            points += int(x[0])

    return points


def get_my_cards():
    # набор карт игрока
    # global pc_total_points
    global balance
    global gain
    global blackjack
    global five_cards
    global six_cards
    # кнонка play again пока недоступна
    btn_clear.config(state='disabled')
    # вызываю функцию deal, чтобы выдать мне карту
    my_cards.append(deal())
    # рассчитываем кол-во очков в зависмости от выданной карты
    my_points = count_points(my_cards)
    # если 21 очко на 2-х картах - BlackJack
    if my_points == 21 and len(my_cards) == 2:
        blackjack = True
        lbl = Label(window, text="Blackjack", font=("Courier", 12))
        lbl.place(x=30, y=190)
        lbls.append(lbl)
    # если карт 5 и очков 21 или меньше - возможен выигрыш с двойной ставкой
    if len(my_cards) == 5 and my_points <= 21:
        five_cards = True
        lbl = Label(window, text="5 cards", font=("Courier", 12))
        lbl.place(x=30, y=190)
        lbls.append(lbl)
    # если карт 6 и более и очков 21 или меньше - возможен выигрыш с тройной ставкой
    if len(my_cards) >= 6 and my_points <= 21:
        five_cards = False
        six_cards = True
        lbl = Label(window, text="6 cards", font=("Courier", 12))
        lbl.place(x=30, y=190)
        lbls.append(lbl)
    # если очков достаточно - нажимаем кнопку Enough
    btn_enough = Button(window, text="Enough", font=("Courier", 12), width=16,
                        command=lambda: get_pc_cards(my_points))
    btn_enough.place(x=160, y=110, width=140)

    for i in range(len(my_cards)):
        # вывожу на экран мои карты
        card_image = PhotoImage(file=f"images/{my_cards[i]}.gif")
        #card_image = card_image.subsample(2, 2)
        lbl = Label(window)
        lbl.image = card_image
        lbl['image'] = lbl.image
        lbl.place(x=40, y=230 + i*50)
        # вывод на экран добавляется в список надписей
        lbls.append(lbl)
        # вывожу на экран кол-во очков
        lbl = Label(window, text=f"{my_points} points", font=("Courier", 12))
        lbl.place(x=30, y=160)
        # вывод на экран добавляется в список надписей
        lbls.append(lbl)

    if my_points > 21:
        # если кол-во очков больше 21 - проигрыш -перебор
        lbl = Label(window, text=f"Too many", font=("Courier", 12))
        lbl.place(x=30, y=190)
        # вывод на экран добавляется в список надписей
        lbls.append(lbl)
        # кнопки Take card и Enough не активны
        btn_take.config(state='disabled')
        btn_enough.config(state='disabled')
        # общий счет добавляется в пользу pc с учетом коэффицента
        gain = -1 * bet
        balance -= 1 * bet
        # кнопка play_again снова активна
        btn_clear.config(state='normal')
        # переход в функцию, отображающую общий счет
        show_total_score()


def get_pc_cards(my_points):
    # набор карт компа и расчет очков в зависимости от всех карт
    global bet
    global gain
    global balance
    global blackjack
    global five_cards
    global six_cards
    # кнопка take отключена
    btn_take.config(state='disabled')
    # Определение карт компьютера
    while True:
        # карта PC
        pc_cards.append(deal())
        pc_points = count_points(pc_cards)

        for i in range(len(pc_cards)):
            # вывод на экран карт PC
            card_image = PhotoImage(file=f"images/{pc_cards[i]}.gif")
            lbl = Label(window)
            lbl.image = card_image
            lbl['image'] = lbl.image
            lbl.place(x=190, y=230 + i * 50)
            # все надписи на экране добавляются в список
            lbls.append(lbl)

        if pc_points > 21:
            # если у PC перебор
            lbl = Label(window, text=f"{pc_points} points", font=("Courier", 12))
            lbl.place(x=180, y=160)
            lbls.append(lbl)
            lbl = Label(window, text="Too many", font=("Courier", 12))
            lbl.place(x=180, y=190)
            lbls.append(lbl)
            # расчет выигрыша игрока в зависимости от расклада карт (BlackJack и др.)
            if blackjack == True:
                gain = 2 * bet
                balance += 2 * bet
                show_total_score()
            elif five_cards == True:
                gain = 2 * bet
                balance += 2 * bet
                show_total_score()
            elif six_cards == True:
                gain = 4 * bet
                balance += 4 * bet
                show_total_score()
            else:
                # к общему счету игрока прибавляется 1
                gain = 1 * bet
                balance += 1 * bet
                show_total_score()
            break

        elif pc_points >= 17:
            # если у pc очков более 17 - больше не набирает карты
            lbl = Label(window, text=f"{pc_points} points", font=("Courier", 12))
            lbl.place(x=180, y=160)
            lbls.append(lbl)
            # определение победителя
            # и расчет выигрыша игрока в зависимости от расклада
            if my_points > pc_points:
                if blackjack == True:
                    gain = 2 * bet
                    balance += 2 * bet
                    show_total_score()
                elif five_cards == True:
                    gain = 2 * bet
                    balance += 2 * bet
                    show_total_score()
                elif six_cards == True:
                    gain = 4 * bet
                    balance += 4 * bet
                    show_total_score()
                else:
                    # к общему счету игрока прибавляется 1
                    gain = 1 * bet
                    balance += 1 * bet
                    show_total_score()
            elif my_points == pc_points:
                # при равном кол-ве очков ставка увеличивается в 2 раза
                gain = 0
                bet *= 2
                lbl = Label(window, text='No one won. Double the bet.', font=("Courier", 12) )
                lbl.place(x=30, y=190)
                # вывод ставки на экран
                show_bet()
                # кнопка Play again активна
                btn_clear.config(state='normal')
                # собираю все lbl
                lbls.append(lbl)
                # вывожу ткущий счет на экран
                show_total_score()
                return bet

            else:
                # если у игрока меньше очков
                # расчет проигрыша игрока в зависимости от расклада
                if pc_points == 21 and len(pc_cards) == 2:
                    lbl = Label(window, text="Blackjack", font=("Courier", 12))
                    lbl.place(x=180, y=190)
                    lbls.append(lbl)
                    gain = -2 * bet
                    balance -= 2 * bet
                    show_total_score()
                elif len(pc_cards) == 5 and pc_points <= 21:
                    lbl = Label(window, text="5 cards", font=("Courier", 12))
                    lbl.place(x=180, y=190)
                    lbls.append(lbl)
                    gain = -2 * bet
                    balance -= 2 * bet
                    show_total_score()
                elif len(pc_cards) >= 6 and pc_points <= 21:
                    lbl = Label(window, text="6 cards", font=("Courier", 12))
                    lbl.place(x=180, y=190)
                    lbls.append(lbl)
                    gain = -3 * bet
                    balance -= 3 * bet
                    show_total_score()
                else:
                    gain = -1 * bet
                    balance -= 1 * bet
                    show_total_score()
            break

    btn_clear.config(state='normal')
    btn_take.config(state='disabled')


def show_total_score():
    # вывод баланса игрока

    global best_balance
    global gain
    global best_player
    global blackjack
    global five_cards
    global six_cards

    # сброс раскладов увеличивающих коэффицент за победу
    blackjack = False
    five_cards = False
    six_cards = False

    lbl = Label(window, text="your money", font=("Courier", 10))
    lbl.place(x=10, y=50, width=140, height=30)
    total_balance = Label(window, text=f"{balance}$", font=("Courier", 18))
    total_balance.place(x=10, y=80, width=140, height=30)

    # показываю выигрыш на прошлой раздаче
    lbl = Label(window, text="gain", font=("Courier", 10))
    lbl.place(x=160, y=50, width=140, height=30)
    lbl = Label(window, text=f"{gain}$", font=("Courier", 14))
    lbl.place(x=160, y=80, width=140, height=30)

    # кнопка Enough становится неактивной
    btn_enough_disabled()

    # если денег меньше 0$ - конец игры
    if balance < 0:
        game_over()

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
    lbl_name = Label(window, text="Who are you?", font=("Courier", 14))
    lbl_name.place(x=10, y=10, width=140, height=30)
    # окно ввода
    name_entry = Entry(textvariable=player_name, width=20, font=("Courier", 14))
    name_entry.place(x=160, y=10, width=140, height=30)
    # установка курсора в поле ввода
    name_entry.focus()
    # кнопка подтверждения имени -> функция активирует кнопку Take card
    name_btn = Button(text="OK", width=16, font=("Courier", 14),
                      command=lambda: btn_take_normal(lbl_name, name_btn, name_entry))
    name_btn.place(x=310, y=10, width=140, height=30)


def btn_take_normal(lbl_name, name_btn, name_entry):
    global player_name
    global best_player
    global start_time
    # инициализация имени игрока
    player_name = name_entry.get()
    # убираю с экрана все поля, связанные с вводом имени игрока
    lbl_name.destroy()
    name_btn.destroy()
    name_entry.destroy()
    # вместо поля для ввода имени вывожу приветствие
    lbl = Label(window, text=f"Good luck {player_name}!", font=("Courier", 18))
    lbl.place(x=10, y=10)
    # кнопка Take card становится активной после ввода имени игрока
    btn_take.config(state='normal')
    # вызов функции обновляющей текущее время
    update_time()


def best_records():
    # запись в файл лучшего баланса
    filename = 'record.json'
    with open(filename, 'w') as f:
        json.dump(best_balance, f)
    # запись в файл имя игрока с лучшим балансом
    filename = 'best_player.json'
    with open(filename, 'w') as f:
        json.dump(best_player, f)


def btn_enough_disabled():
    # кнопка Enough - игроку больше не нужно карт, ход переходит к PC
    btn_enough = Button(window, text="Enough", font=("Courier", 12), width=16, command=get_pc_cards)
    btn_enough.place(x=160, y=110, width=140)
    btn_enough.config(state='disabled')


def show_bet():
    # вывод на экран текущей ставки
    lbl = Label(window, text=f"{bet}", font=("Courier", 14))
    lbl.place(x=310, y=80, width=140, height=30)


def game_over():
    # конец игры, когда у игрока заканчиваются деньги
    global game_active
    play(lbls)
    game_active = False

    btn_take.config(state='disabled')
    btn_clear.config(state='disabled')

    lbl = Label(window, text="You don't have any more money", font=("Courier", 11))
    lbl.place(x=90, y=240)
    lbl = Label(window, text="GAME OVER", font=("Courier", 40))
    lbl.place(x=80, y=280)

def close():
    # вывод окна с запросом выхода из игры
    if messagebox.askokcancel("Exit", "Do you want to quit?"):
        window.destroy()

def update_time():
    global game_time
    global game_active
    if game_active is True:
        game_time += timedelta(seconds=1)
        time_lbl_sec.config(text=f"{game_time}")
        window.after(1000, update_time)
    else:
        time_lbl_sec.config(text=f"{game_time}")
        window.after(1000, update_time)

def update_global_time():
    time_lbl.config(text=f"{datetime.now():%H:%M:%S}")
    window.after(10, update_global_time)


window = Tk()
window.protocol("WM_DELETE_WINDOW", close)
window.title(f"Welcome to Oriono's Blackjack! Now is {datetime.now():%d}"
             f" of {datetime.now():%B} {datetime.now():%Y}")
window.geometry("460x560")
window.resizable(0, 0)

# показываю лучший баланс и имя лучшего игрока внизу игрового экрана
lbl = Label(window, text=f"Biggest win: {best_player} {best_balance}$", font=("Courier", 12))
lbl.place(x=10, y=530)

# показываю текущее время
time_lbl = Label(window, font=("Courier", 12))
time_lbl.place(x=360, y=530)
# показываю время игры
time_lbl_sec = Label(window, font=("Courier", 12))
time_lbl_sec.place(x=360, y=15)

# кнопка Take card - взять еще карту игроку
btn_take = Button(window, text="Take card", font=("Courier", 12), width=16, command=get_my_cards)
btn_take.place(x=10, y=110, width=140)
btn_take.config(state='disabled')

# показываю текущую ставку
lbl = Label(window, text="bet", font=("Courier", 10))
lbl.place(x=310, y=50, width=140, height=30)
lbl = Label(window, text=f"{bet}", font=("Courier", 14))
lbl.place(x=310, y=80, width=140, height=30)

# кнопка Play again - карты обнуляются, новая сдача
btn_clear = Button(window, text="Play again", font=("Courier", 12), width=16,
                   command=lambda: play(lbls))
btn_clear.place(x=310, y=110, width=140)
btn_clear.config(state='disabled')

# текущее время
update_global_time()
# кнопка Enough неактивна
btn_enough_disabled()
# ввод имени игрока
init_name()
# общий счет всей игры
show_total_score()
# главный цикл игры
window.mainloop()