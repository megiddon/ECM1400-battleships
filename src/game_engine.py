#Copyright (C) 2023 megiddon
#This program is licensed under the GNU GPL 3.0 or later.
#This is contained in full in the file LICENSE.txt

'''Simple game engine for battleships.
only the simple 1 player game is supported.
'''
import re

from components import initialise_board, create_battleships, place_battleships, print_board

def attack(coordinates:tuple[int,int],board:list[list[str]],ships:dict[str,int]) -> bool:

    '''Carries out an attack on a specific square.

    :param coordinates: The square being attacked.
    :type coordinates: tuple
    :param board: The board of the player being attacked.
    :type board: list
    :param ships: The ships of the player being attacked.
    :type ships: dict

    :return bool:

    '''

    row, col = coordinates[0], coordinates[1]
    name:str = board[row][col]
    #If the square contains a ship
    if name:
        ships[name] -= 1
        #Removes ship from square
        board[row][col] = None
        print(f'Hit battleship at ({col},{row})!')
        if ships[name] == 0:
            print(f'{name} sunk!')
        return True
    print(f'Miss at ({col},{row})!')
    return False

def validate_coords_input(coords:str) -> bool:

    '''Validates input with regex.

    :param coords: the coordinates entered by the user:
    :type coords: str
    :return: whether the input is valid or not:
    :rtype: bool

    '''
    if re.fullmatch('[0-9]+,[0-9]+',coords):
        return True
    return False

def cli_coordinates_input() -> tuple[int,int]:

    '''Gets a pair of coordinates representing a square from the user.

    :return: The square entered by the user.
    :rtype: tuple

    '''
    #Loops until a valid response is received from the user.
    while True:
        coords:str = input('Please enter a pair of coordinates in the format x,y. ')
        if validate_coords_input(coords):
            #Parses coordinates into integer values
            coords = coords.split(',')
            return (int(coords[1]), int(coords[0]))

def wintest(ships:dict[str,int]) -> bool:
    '''Checks if all of a player's ships have been sunk.

    :param ships: The player's ships.
    :type ships: dict
    :return: Whether the player has no ships remaining or not.
    :rtype: bool

    '''
    for i in ships.values():
        if i:
            return False
    return True

def simple_game_loop() -> None:


    '''Simple single player game loop.

    '''
    print('Welcome to Battleship!')
    board = initialise_board()
    ships = create_battleships()
    board = place_battleships(board,ships,'simple')
    #Loops until player has won.
    while not wintest(ships):
        print_board(board)
        coords = cli_coordinates_input()
        attack(coords,board,ships)
    print('Player 1 wins!')

if __name__ == '__main__':
    simple_game_loop()
