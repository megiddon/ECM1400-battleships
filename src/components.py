#Copyright (C) 2023 megiddon
#This program is licensed under the GNU GPL 3.0 or later.
#This is contained in full in the file LICENSE.txt

'''Contains a number of functions used in derivative modules
    relating to the internal functionality of the game.
    '''


import sys
from random import shuffle, randint
import json
import logging
import re
from copy import deepcopy



#we set up a logger here.
#this will be imported into all modules that have this as a dependency
logging.basicConfig(encoding='utf-8',
                    level=logging.INFO,
                    handlers=[logging.FileHandler('gamelog.log'),logging.StreamHandler()],
                    format='%(asctime)s %(levelname)-1s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def get_default_ships() -> dict[str,int]:

    return {'Aircraft_Carrier': 5, 'Battleship': 4, 'Cruiser': 3,
                             'Submarine': 3, 'Destroyer': 2}
def await_exit() -> None:
    '''Waits for the user to close the program,
    usually after a critical error has occured.'''

    input('Press Enter to exit. ')
    sys.exit()

def validate_square(square:tuple[int,int],size:int) -> bool:

    '''Checks that a square falls within the boundaries of the board

    :param square: the square to be checked.
    :type square: tuple

    :param size: the size of the board.
    :type size: int (should be > 0)

    :return: whether the square is valid or not
    :rtype: bool

    '''

    if square[0] >= 0 and square[1] >= 0:
        if square[0] < size and square[1] < size:
            return True
    return False



def print_board(board:list[list[str]]) -> None:

    '''Prints out the board to the console. Not used in the web-based game.

    :param board: a list of lists representing a board.
    :type board: list

    :return None

    '''

    outputstring = '||'
    for i in range(len(board)):
        outputstring += str(i)[-1]
    outputstring  += '\n'

    for i in range(len(board)):
        outputstring += (str(i)[-1] + '|')
        for j in board[i]:
            outputstring += j[0] if j else '-'
        outputstring += '\n'
    print(outputstring)

def get_json_data(filename:str) -> dict:

    '''Reads a JSON file and returns the data for later use.

    :param filename: The name of the file to be accessed, with the extension intact.
    :type filename: str

    :return data: The data contained in the JSON file in dictionary format.
    :type data: dict

    '''
    #Opens file and parses JSON data with the stdlib JSON module.
    try:
        file = open(filename)
        data = file.read()
        data = json.loads(data)
        return data

    #Error handling if the file does not exist or contains bad JSON data.
    except FileNotFoundError:
        logging.error('%s does not exist!', filename)
    except json.decoder.JSONDecodeError:
        logging.error('%s contains invalid JSON data!', filename)


def initialise_board(size:int=10) -> list[list[str]]:

    '''Generates the board given a board size.

    :param size: The size of the board.
    :type size: int (should be > 0)

    :return: The board as a list of n lists of size n.
    :rtype: list

    '''
    board = []
    for i in range(size):
        board.append([None] * size)
    return board

def create_battleships(filename:str='battleships.txt') -> dict[str,int]:

    '''Reads a file and copies the data into an array.

    :param filename: The name of the file to be accessed.
    :type filename: str

    :return: A dictionary with the ship name as the key and the length as the value.
    :rtype: dict

    '''
    ships = {}
    #Opens file
    try:
        with open(filename, 'r') as file:
            for line in file:
                #Checks validity of data in each line
                if not re.match(r'[\w]+:[0-9]+', line):
                    logging.error('%s contains bad data! default values for ships will be used.',
                                  filename)
                    ships = get_default_ships()
                #Parses data in file
                else:
                    splitline = line.rstrip().split(':')
                    ships[splitline[0]] = int(splitline[1])

        return ships

    except FileNotFoundError:
        logging.error('%s not present in root! Default values for ships will be used',
                      filename)

        return get_default_ships

def check_square(board:list[list[int]], square:tuple[int,int], size:[int]) -> bool:
    '''Checks if a square is within the board.

    '''
    #returns true if a square is valid, returns false otherwise
    if validate_square(square,size):
        if not board[square[0]][square[1]]:
            return True
    return False




def place_battleships(board:list[list[str]], ships:dict[str,int],
                      algorithm='simple') -> list[list[str]]:

    '''Populates a board with battleships

    :param board: the board as a list of lists.
    :type board: list

    :param ships: the ships to be placed.
    :type ships: dict

    :param algorithm: the method of placement to be used.
    :type algorithm: str ("simple", "random", "custom" currently implemented.)

    :return: the updated board with ships placed.
    :rtype: list

    '''

    #Checks integrity of ship lengths
    for i in ships.values():
        if not isinstance(i,int):
            logging.error('battleships.txt contains ships too large for given board size')
            ships = get_default_ships()

        elif i >= len(board) or i < 1:
            logging.error('battleships.txt contains ships too large for given board size')
            ships = get_default_ships()

    #Places each ship horizontally on column 0 on each row.
    if algorithm == 'simple':
        row = 0
        for key, value in ships.items():
            for j in range(int(value)):
                board[row][j] = key
            row += 1
        return board

    if algorithm == 'random':
        directions = [(0,1), (0,-1), (1,0), (-1,0)]


        for name, length in ships.items():
            valid_flag = False
            while not valid_flag:
                #generates random square
                start_square = (randint(0,len(board)), randint(0,len(board)))
                sequence = [0,1,2,3]
                shuffle(sequence)
                for i in sequence:
                    if valid_flag:
                        break
                    #checks if run of squares is valid
                    new_square = start_square
                    valid_flag = True
                    for j in range(0,length):
                        new_square = (start_square[0] + directions[i][0] * j,
                                      start_square[1] +directions[i][1] * j)
                        if not check_square(board, new_square, len(board)):
                            valid_flag = False

                    #Writes to the board if the placement is valid.
                    if valid_flag:
                        for k in range(0,length):
                            new_square = (start_square[0] + directions[i][0] * k,
                                            start_square[1] + directions[i][1] * k)
                            board[new_square[0]][new_square[1]] = name


        return board



    else:
        #Gets placement data from file.
        data = get_json_data('placement.json')

        #Uses preset ships if placement.json has invalid data or can't be read.
        if not data:
            place_battleships(board, ships, 'random')
            return board

        #Iterates over ships
        for j,k in data.items():
            try:
                board2 = deepcopy(board)
                #Attempts to resolve mismatches between names in battleships.txt and placement.json
                name = j if j in ships.keys() else ships.keys()[list(data.keys()).index(j)]
                #Parses values from 'data' dictionary.
                direction = (1,0) if k[2] == 'h' else (0,1)
                start_square = (int(k[0]), int(k[1]))
                #Writes to 'board'
                for i in range(0,ships[j]):
                    new_square = (start_square[0] + direction[0] * i,
                    start_square[1] + direction[1] * i)
                    board[new_square[1]][new_square[0]] = j

            #Error handling
            except IndexError:
                logging.error('Invalid ship placement - ship goes outside of board')
                return place_battleships(initialise_board(len(board)),ships,'random')
            except TypeError:
                logging.error('Invalid data in placement.json')
                return place_battleships(initialise_board(len(board)),ships,'random')
            except ValueError:
                logging.error('Invalid data in placement.json')
                return place_battleships(initialise_board(len(board)),ships,'random')


        return board

if __name__ == 'main':
    logging.basicConfig(filename='gamelog.log', encoding='utf-8', level=logging.DEBUG)
