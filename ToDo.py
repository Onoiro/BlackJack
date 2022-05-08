HELP = """
help - напечатать справку о программе.
add - добавить задачу в список
show - напечатать все добавленные задачи
exit - выход из программы"""

today_tasks = []
tommorow_tasks = []
other_tasks = []

run = True

while run:
    command = input("Введите команду: ")
    if command == "help":
        print(HELP)
    elif command == "show":
        print(f"Сегодня нужно: {today_tasks}\n"
              f"Завтра нужно: {tommorow_tasks}\n"
              f"Вообще нужно: {other_tasks}")
    elif command == "add":
        task = input("Введите название задачи: ")
        date = input("Когда нужно выполнить задачу? ")
        if date == "Сегодня" or date == "сегодня":
            today_tasks.append(task)
            print("Задача добавлена")
        elif date == "Завтра" or date == "завтра":
            tommorow_tasks.append(task)
            print("Задача добавлена")
        else:
            other_tasks.append(task)
            print("Задача добавлена")
    elif command == "exit":
        print("Спасибо за использование! До свидания!")
        break
    else:
        print("Неизвестная команда")
        print("Повторите ввод")
print("До свидания")