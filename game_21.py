"""Game BlackJack (21, point)"""
# Простой вариант игры "Очко" (или 21, или BlackJack)

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
# коэффицент увеличения total_points - при равном кол-ве очков удвоение
increase_points = 1

name = input('What is your name? ')

def exit_game():
    # для выхода из игры нужно нажать "q"
    game_active = input('If do you want to quit press "q" or press Enter \n')
    if game_active == 'q':
        sys.exit()

while True:

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
            # раздача игроку сразу по 2 карты
            if card_number < 2:
                my_cards.append(deal())
                my_points += count_points(my_cards, card_number)
                card_number += 1
            print(f"{name} cards is: {my_cards}, {my_points} points")

            if my_points > 21:
                # если кол-во очков более 21 - перебор
                print('Too many - loose')
                my_points = 0
                break
            # если карт достаточно - напишите "q", если нет - нажмите Enter
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
            # если кол-во очков равно - коэффицент начисления total_points удваивается
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