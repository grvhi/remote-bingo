import os
import shutil
import sys
import random
from pathlib import Path
from typing import List, Tuple
from jinja2 import Environment, FileSystemLoader, select_autoescape


env = Environment(
    loader=FileSystemLoader(Path().parent),
    autoescape=select_autoescape(['html', 'xml'])
)

RANGES = {
    'b': range(1, 15),
    'i': range(16, 30),
    'n': range(31, 45),
    'g': range(46, 60),
    'o': range(61, 75)
}


def generate_grid():
    columnar = {
        k: random.sample(RANGES[k], 5)
        for k in RANGES.keys()
    }
    columnar['n'].insert(2, 'FREE')
    columnar['n'].pop(3)
    rows = [
        [
            (list(columnar.keys())[col_i], val[i])
            for col_i, val in enumerate(columnar.values())
        ]
        for i in range(0, 5)
    ]
    return list(columnar.keys()), rows


def render_grid(alias: str, title_row: List, grid_rows: List[List]):
    template = env.get_template('card.html')
    return template.render(
        name=alias,
        title_row=title_row,
        grid_rows=grid_rows
    )


def create_grids(aliases: Tuple[str]):
    if not os.path.exists('grids'):
        os.mkdir('grids')
    for alias in aliases:
        alias = alias.strip()
        t_row, g_rows = generate_grid()
        html = render_grid(alias, t_row, g_rows)
        with open(f'grids/{alias}-grid.html', 'w') as f:
            f.write(html)


def end_game():
    shutil.rmtree('grids')
    os.remove('current-game.txt')


def random_ball():
    letter = random.choice(list(RANGES.keys()))
    return f'{letter}{random.choice(RANGES[letter])}'


def start_game():
    if os.path.exists('current-game.txt'):
        resume = input(
            'Confirm you wish to resume an existing game.\n'
            'Answering with "N" will remove the existing game balls, '
            'but will NOT delete existing grids\n(y/N): '
        )
        if not resume:
            os.remove('current-game.txt')
    try:
        with open('current-game.txt', 'w+') as f:
            while True:
                input()
                new = random_ball()
                f.write(f'{new}\n')
                sys.stdout.write(f'\r{new}')
                sys.stdout.flush()
    except (KeyboardInterrupt, SystemExit, SystemError):
        print('Game stopped!')


def check_winner(numbers: Tuple[str]):
    with open('current-game.txt') as f:
        all_balls = [s.strip() for s in f.readlines()]
    confirmed = all([n in all_balls for n in numbers])
    if confirmed:
        print('Yes! The submitted numbers are valid!')
    else:
        diff = ','.join([n for n in numbers if n not in all_balls])
        print(f'Nope.... Submitted numbers not found:\n{diff}')


if __name__ == '__main__':
    import fire

    fire.Fire({
        'create_grids': create_grids,
        'end_game': end_game,
        'start_game': start_game,
        'check_winner': check_winner
    })
