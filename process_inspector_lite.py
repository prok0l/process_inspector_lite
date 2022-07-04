# импорты
import os
from subprocess import Popen, PIPE
import time
from datetime import datetime
from signal import signal, SIGINT
from sys import argv


# функция окончания программы
def exit_funk():
    os.system("cmd.exe")
    quit()


del_system: bool = False
mas_not_checked: list = ["System", "Services"]
output: list = [0, 1, 2, 3, 4]
save: bool = False
del_preview: bool = False
# дефолтный конфиг

# анализ переданных аргументов
args = argv[1:]
for arg in args:
    if "--d" in arg:
        del_system = True
        continue
    if "--list=" in arg:
        mas_not_checked = arg[9:].split(",")
        continue
    if "--output=" in arg:
        output = arg[9:].split(",")
        output = [int(x) for x in output]
        continue
    if "--save=" in arg:
        save = True
        name = arg[7:]
        if name == "auto":
            save_path = str(datetime.now()).split(".")[0].replace(":", "-")[:-3] + ".txt"
        else:
            save_path = name
        continue
    if "--help" in arg:
        print("--d - disables output of processes specified in config\n" +
              "--list= - change the list of processes in the config. default - System,Services.\n" +
              "--output - change output format. default - 0,1,2,3,4.\n" +
              "--save - changes the logging path\n" +
              "--p - disables preview\n\n\n")
        os.system("cmd.exe")
    if "--p" in arg:
        del_preview = True
        continue

os.system("cls")

# превью
if not del_preview:
    prev = "                                         \n    ____  _________  ________  __________\n   / __ \/ ___/ __" \
           " \/" \
           " ___/ _ \/ ___/ ___/\n  / /_/ / /  / /_/ / /__/  __(__  |__  ) \n / .___/_/   \____/\___/\___/____/____" \
           "/  \n" \
           "/_/                                      \n    _                            __            \n   (_)___  " \
           "_____" \
           "____  ___  _____/ /_____  _____\n  / / __ \/ ___/ __ \/ _ \/ ___/ __/ __ \/ ___/\n / / / / (__  ) /_/ " \
           "/  __" \
           "/ /__/ /_/ /_/ / /    \n/_/_/ /_/____/ .___/\___/\___/\__/\____/_/     \n            /_/              " \
           "      " \
           "            \n\ncreated by prok0l"

    print(f"\x1b[1;34;40m{prev}\x1b[m")
    for i in range(0, 3):
        signal(SIGINT, lambda *_: exit_funk())
        time.sleep(1)

    os.system("cls")


# функция логирования
def save_funk(string: str):
    global save
    if save:
        with open(save_path, "a+") as f:
            f.write(string + "\n")


# функция преобразования строки в табличный формат
def output_mas(string: str):
    global output
    str_out = ""
    str_mas = string.split()
    str_mas_copy = str_mas[:]
    if 4 in output:
        str_mas = str_mas_copy[:4]
        str_mas.append("".join(str_mas_copy[4:]))
    for ind in output:
        str_out += str_mas[ind]
        str_out += " " * (25 - len(str_mas[ind]))
    if len(str_out) > 120:
        str_out = str_out[:119]
    return str_out


# изначальное сканирование пройцессов
mas_not_formated: list = [line.decode('cp866', 'ignore') for line in Popen('tasklist', shell=True, stdout=PIPE)
    .stdout.readlines()][2:]
mas_not_formated: list = [value for value in mas_not_formated if len(value.split()) != 0]
mas_at_first: list = [i.split()[1] for i in mas_not_formated]

# строчка в лог о начале работы
save_funk(f"{' ' * 47}PROCESS INSPECTOR STARTED")

# основной цикл работы программы
while True:
    signal(SIGINT, lambda *_: exit_funk())
    m_new = []
    m_del = []
    mas_not_formated_now: list = [line.decode('cp866', 'ignore') for line in Popen('tasklist', shell=True, stdout=PIPE)
        .stdout.readlines()][2:]
    mas_not_formated_now: list = [value for value in mas_not_formated_now if len(value.split()) != 0]
    mas_now: list = [i.split()[1] for i in mas_not_formated_now]

    for k, i in enumerate(mas_now):
        if i not in mas_at_first:
            name = mas_not_formated_now[k].split()[0]
            if name not in ["cmd.exe", "tasklist.exe"]:
                if del_system and mas_not_formated_now[k].split()[2] in mas_not_checked:
                    pass
                else:
                    m_new.append(output_mas(mas_not_formated_now[k][:-2]))

    for k, i in enumerate(mas_at_first):
        if i not in mas_now:
            name = mas_not_formated[k].split()[0]
            if name not in ["cmd.exe", "tasklist.exe"]:
                if del_system and mas_not_formated[k].split()[2] in mas_not_checked:
                    pass
                else:
                    m_del.append(output_mas(mas_not_formated[k][:-2]))

    if len(m_new) != 0 or len(m_del) != 0:
        time = " ".join(["-" * 54, str(datetime.now().time()).split(".")[0], "-" * 54])
        print(f"\x1b[0;33;40m{time}\x1b[m")
        save_funk(time)
        if len(m_new) != 0:
            print(f"\x1b[0;32;40mNew:\x1b[m")
            save_funk("New:")
            print("\n".join(m_new))
            save_funk("\n".join(m_new))
        if len(m_del) != 0:
            if len(m_new) != 0:
                print()
                save_funk("")
            print(f"\x1b[0;31;40mDelete:\x1b[m")
            save_funk("Delete: ")
            print("\n".join(m_del))
            save_funk("\n".join(m_del))

        mas_at_first = mas_now
        mas_not_formated = mas_not_formated_now
