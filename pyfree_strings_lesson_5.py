command = "/add 31.12 Текст задачи"
splitted_command = command.split(maxsplit=2)
print(splitted_command)
date = splitted_command[1]
task = splitted_command[2]

print(date, task)