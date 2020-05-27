"""Запрещено использовать этот модуль для сдачи лабораторных и курсовых работ!"""
import random

SIDE_HUMAN = 'Человек'
SIDE_PC = 'Компьютер'

# обозначения
CHAR_X = 'X'
CHAR_O = 'O'
CHAR_EMPTY = ' '

# игровое поле
game_field = [
    [CHAR_EMPTY, CHAR_EMPTY, CHAR_EMPTY],
    [CHAR_EMPTY, CHAR_EMPTY, CHAR_EMPTY],
    [CHAR_EMPTY, CHAR_EMPTY, CHAR_EMPTY],
]

action_log = []  # история ходов

side_map = {SIDE_HUMAN: CHAR_X, SIDE_PC: CHAR_O}  # кто за что играет

turn_char = CHAR_X  # чей ход

winner = None


def get_step_coordinates_human() -> (int, int):
    while True:
        value = input('Координаты вашего хода, "x y": ')
        coordinates = value.split()
        if all([i.isdigit() for i in coordinates]) and len(coordinates) == 2:
            x, y = int(coordinates[0]), int(coordinates[1])
            if 1 <= x <= 3 and 1 <= y <= 3:
                if game_field[x - 1][y - 1] != CHAR_EMPTY:
                    print('Координаты {} {} уже заняты'.format(x, y))
                else:
                    return x - 1, y - 1
            else:
                print('Координаты должны быть числом от 1 до 3')
        else:
            print('Вы ввели неправильные координаты. Пример: 1 3')


def get_side_map() -> dict:
    while True:
        value = input('За кого играет {}? 1 - за "{}", 2 - за "{}": '.format(SIDE_HUMAN, CHAR_X, CHAR_O))
        side = value.strip()
        if side == '1':
            return {SIDE_HUMAN: CHAR_X, SIDE_PC: CHAR_O}
        elif side == '2':
            return {SIDE_HUMAN: CHAR_O, SIDE_PC: CHAR_X}
        else:
            print('Вы ввели неправильную сторону. Введите 1 или 2.')


def draw_field():
    for line in range(50):
        print()
    for action in action_log:
        print(action)
    print()
    for row in game_field:
        print('[ {} {} {} ]'.format(row[0], row[1], row[2]))
    print()


def add_action(action: str):
    action_log.append(action)
    draw_field()


def get_empty_positions() -> [(int, int)]:
    return [(row, col) for row in range(3) for col in range(3) if game_field[row][col] == CHAR_EMPTY]


def get_step_coordinates_ps() -> (int, int):
    """логика игры компьютера"""
    # можно победить
    pass
    # противник следующим ходом победит
    pass
    # случайное свободное поле
    return random.choice(get_empty_positions())


if __name__ == '__main__':
    add_action('=== Крестики-нолики ===')
    add_action('Первыми ходят крестики.')
    side_map = get_side_map()
    add_action(
        '{} играет за "{}", {} играет за "{}"'.format(SIDE_HUMAN, side_map[SIDE_HUMAN], SIDE_PC, side_map[SIDE_PC]))
    while not winner:
        # ход
        if turn_char == side_map[SIDE_HUMAN]:
            # ходит человек
            add_action('Ходит {} за "{}"'.format(SIDE_HUMAN, turn_char))
            x, y = get_step_coordinates_human()
            game_field[x][y] = turn_char
            add_action('{} сходил на {} {}'.format(SIDE_HUMAN, x + 1, y + 1))
        else:
            # ходит компьютер
            add_action('Ходит {} за "{}"'.format(SIDE_PC, turn_char))
            x, y = get_step_coordinates_ps()
            game_field[x][y] = turn_char
            add_action('{} сходил на {} {}'.format(SIDE_PC, x + 1, y + 1))
        # передача хода
        turn_char = CHAR_O if turn_char == CHAR_X else CHAR_X
        # поиск победителя
        for char in (CHAR_X, CHAR_O):
            full_line = (char, char, char)
            for i in range(3):
                if (game_field[i][0], game_field[i][1], game_field[i][2]) == full_line or \
                        (game_field[0][i], game_field[1][i], game_field[2][i]) == full_line:
                    winner = char
            if (game_field[0][0], game_field[1][1], game_field[2][2]) == full_line or \
                    (game_field[0][2], game_field[1][1], game_field[2][0]) == full_line:
                winner = char
        if not winner and len(get_empty_positions()) == 0:
            winner = CHAR_EMPTY
    # конец
    if winner == CHAR_EMPTY:
        add_action('★ Ничья! ★')
    else:
        add_action('★ Победил {} за "{}"! ★'.format({v: k for k, v in side_map.items()}[winner], winner))
    input()
