def print_ansi_color_palette():
    for i in range(256):
        # Выводим номер цвета и цветной квадрат с соответствующим цветом фона
        print(f"\033[48;5;{i}m {i:3} \033[0m", end=' ')
        # Переходим на новую строку после каждых 16 цветов
        if (i + 1) % 16 == 0:
            print()

print_ansi_color_palette()

