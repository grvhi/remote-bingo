Remote Bingo
============
Welcome to Remote Bingo.

For The Host
------------
Install the "library" and its dependencies, then create and distribute grids for
your users, then start the game!

1. `git clone`
2. `pipenv install`
3. `pipenv run python bingo.py create_grids <alias1>,<alias2>,<alias3>.....`
4. `pipenv run python bingo.py start_game`
    -   If a game is already underway, you will be asked if you wish to resume
        or end the existing game.
    -   Hit `enter` when you want a new ball.
5.  When you have a winner, hit `ctrl+c` to stop the game (the game can be resumed)
5.  `pipenv run python bingo.py check_winner <ball1>,<ball2>,<ball3>....`
6.  If the winner is confirmed:
    -   `pipenv run python bingo.py end_game` to delete all files

    
