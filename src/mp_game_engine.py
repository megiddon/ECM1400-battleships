#Copyright (C) 2023 megiddon
#This program is licensed under the GNU GPL 3.0 or later.
#This is contained in full in the file LICENSE.txt


'''Engine for the two-player version of the game
    played through the command line.
    '''

import random
from math import floor
import logging

from game_engine import cli_coordinates_input, attack, wintest
from components import get_json_data, initialise_board, create_battleships
from components import place_battleships, validate_square, print_board

logging.basicConfig(encoding='utf-8',
                    level=logging.INFO,
                    handlers=[logging.FileHandler('gamelog.log'),logging.StreamHandler()],
                    format='%(asctime)s %(levelname)-1s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def validate_config_data(difficulty,size) -> (str, int):

    '''Validates the data in config.json.

    :param difficulty: the difficulty variable in config.json
    :param size: the size variable in config.json

    '''

    #Checks that the size variable has a valid value.
    try:
        if size != floor(size) or size < 0:
            logging.error('size variable in config.json invalid!')
            size = 10
    except TypeError:
        logging.error('size variable in config.json invalid!')
        size = 10


    #Checks that the board is large enough for all ships to be placed.
    max_ship_length = max(create_battleships().values())
    if size < max_ship_length:
        size = max_ship_length
        logging.error("Specified board size cannot fit all ships!\
                        A larger board will be used.")

    #Checks that the difficulty is valid.
    if difficulty.lower() not in ['easy','medium','hard','very hard','extreme']:
        logging.error('difficulty variable in config.json invalid!')
        difficulty = 'easy'

    return difficulty,size

def choose_advanced_square(ai_checked:list[tuple[int,int]],
                           ships:dict[str,int],
                           polarity:int,
                           size:int) -> tuple[int,int]:

    '''chooses a square based on the probability of the square being able to contain each ship.

    :param ai_checked: list of squares the ai has already attacked
    :type ai_checked: list
    :param ships: the player's ships
    :type ships: dict
    :param polarity: the distance between squares that the ai can check
    :type polarity: int
    :param size: the size of the board
    :type size: int

    :return: the square that the ai chooses
    :rtype: tuple
    '''

    DIRECTIONS = [(1,0), (-1,0), (0,1), (0,-1)]

    #it's the leaning tower of indentation
    scores:list[list[int]]= []
    #populates array
    for i in range(size):
        scores.append([0] * size)

    #iterates over each square
    for i in range(size):
        for j in range(size):
            #checks polarity of square
            if (i + j) % polarity == 1:
                #number of squares to each side of ship
                squares = [0,0,0,0]
                #iterates over each direction
                for k in range(4):
                    new_square = (i,j)
                    endflag = False
                    #checks how many squares are free in each direction
                    while not endflag:
                        new_square = (new_square[0] + DIRECTIONS[k][0],
                                      new_square[1] + DIRECTIONS[k][1])
                        if (new_square in ai_checked or not validate_square(new_square,size)
                        or squares[k] == max(ships.values()) - 1):
                            endflag = True
                        #if the square is free
                        else:
                            squares[k] += 1

                #calculates score based on the number of free squares in each direction
                horizontal_squares:int = squares[0] + squares[1] + 1
                vertical_squares:int = squares[2] + squares[3] + 1
                h_score:int = floor(horizontal_squares ** 2/ 4)
                v_score:int = floor(vertical_squares ** 2 / 4)
                scores[i][j] = h_score + v_score + random.randint(5,7)

    #chooses square, but now factoring in the score for each square.

    total:int = sum(sum(scores, []))
    index:int = random.randint(0,total-1)
    cumulative = 0
    for i in range(size):
        for j in range(size):
            cumulative += scores[i][j]
            if cumulative > index:
                return (i,j)






def advanced_ai_attack(coords:tuple[int,int],
                       board:list[list[str]],
                       ships:dict[str,int],
                       hunt:list[dict[str,tuple[int,int],tuple[int,int],tuple[int,int]]],
                       difficulty:[str]) -> list[dict[str,tuple[int,int],
                                                      tuple[int,int],tuple[int,int]]]:

    '''Replaces the 'attack' function for the more advanced AI.

    :param coords: the square being attacked.
    :type coords: tuple
    :param board: the board being attacked.
    :type board: list
    :param ships: the ships of the player being attacked.
    :type ships: dict
    :param hunt: the list of ships that have been found by the AI
    :type hunt: list

    :return: the list of ships which have been found but not sunk
    :rtype: list

    '''

    row,col = coords[0], coords[1]
    name:str = board[row][col]

    if difficulty != 'easy':
        #if there has been a hit
        if name:
            #if there is a ship being looked for
            if hunt:

                #if the ship is the one being looked for
                if hunt[0]['name'] == name:

                    #if the orientation has not been found
                    if hunt[0]['orientation'] == (0,0):
                        if abs(coords[0] - hunt[0]['lsquare'][0]) == 1:
                            hunt[0]['orientation'] = (1,0)
                        else:
                            hunt[0]['orientation'] = (0,1)

                    if sum(coords) - sum(hunt[0]['lsquare']) > 0:
                        hunt[0]['rsquare'] = coords
                    else:
                        hunt[0]['lsquare'] = coords



                else:

                    #checks if the ship is a new ship
                    index = None
                    for i in range(1,len(hunt)):
                        if hunt[i]['name'] == name:
                            index = i

                    #if the ship is not a new ship
                    if index:

                        #if the ship's orientation has been found
                        if hunt[index]['orientation'] != (0,0):
                            if hunt[index]['lsquare'] - hunt[index]['orientation'][0] == coords:
                                hunt[index]['lsquare'] = coords
                            elif hunt[index]['rsquare'] + hunt[index]['orientation'][1] == coords:
                                hunt[index]['rsquare'] = coords
                        else:
                            hunt[index]['lsquare'] = coords

                    #if the ship is a new ship
                    else:
                        hunt.append({'name':name, 'lsquare':coords,
                                     'rsquare':coords, 'orientation':(0,0)})

            else:
                hunt.append({'name':name, 'lsquare':coords,
                             'rsquare':coords, 'orientation':(0,0)})

    if name:
        ships[name] -= 1
        board[row][col] = None
        print(f'AI hit battleship at ({col},{row})!')
        if ships[name] == 0:
            for i in hunt:
                if ships[i['name']] == 0:
                    hunt.remove(i)
            print(f'{name} sunk!')
        return hunt
    print(f'AI missed at ({col},{row})!')
    return hunt


def choose_square(ai_checked:list[tuple[int,int]],
                  polarity:int,
                  size:int) -> tuple[int,int]:

    '''Chooses square randomly. separate implementation for the more advanced ai
    since the parameters for the generate_attack function are specified
    in the specification.

    :param ai_checked: the squares that the ai has already attacked.
    :type ai_checked: list
    :param polarity: the polarity that the ai attacks with.
    :type polarity: int
    :param size: the size of the board.
    :type size: int
    :return: the square chosen.
    :rtype: tuple

    '''
    while True:
        #Generates random coordinates.
        (x_coord,y_coord) = (random.randint(0,size-1), random.randint(0,size-1))
        #Validates random coordinates.
        if (x_coord,y_coord) not in ai_checked:
            if polarity:
                if (x_coord + y_coord) % 2 == 1:
                    return (x_coord,y_coord)
            else:
                return (x_coord,y_coord)

def generate_attack(size:int=10) -> tuple[int,int]:

    '''Chooses square randomly.

    :param size: the size of the board.
    :type size: int
    :return: the generated square.
    :rtype: tuple
    '''

    new_square = (random.randint(0,size-1), random.randint(0,size-1))
    return new_square

def generate_advanced_attack(ai_checked:list[tuple[int,int]],
                             difficulty:str,
                             hunt:list[dict[str,tuple[int,int],tuple[int,int],tuple[int,int]]],
                             ships:dict[str,int],
                             size:int):

    '''Replaces the 'generate_attack' function for the more advanced AI

    :param ai_checked: the list of squares that the AI has checked
    :type ai_checked: list
    :param difficulty: the difficulty of the game
    :type difficulty: string
    :param hunt: the list of ships that the AI has found
    :type hunt: list
    :param ships: the ships of the player being attacked
    :type ships: dict
    :param size: the size of the board.
    :type size: int
    :return: the square generated by the AI, the list of squares that the AI has checked
    :rtype: tuple, list

    '''

    DIRECTIONS = [(1,0), (-1,0), (0,1), (0,-1)]

    #Loops until a good square is found.
    while True:

        #if there is not a ship on the queue.
        if not hunt:
            if difficulty == 'medium':
                new_square = choose_square(ai_checked,1,size)
            elif difficulty == 'hard':
                new_square = choose_square(ai_checked,2,size)
            elif difficulty == 'very hard':
                new_square = choose_advanced_square(ai_checked, ships, 2, size)
            elif difficulty == 'extreme':
                new_square = choose_advanced_square(ai_checked, ships,
                                                    max(min(ships.values()), 2),size)
        #If there is a ship on the queue.
        else:
            direction_choice = random.choice([0,1])


            #If the direction of the ship is known.
            if hunt[0]['orientation'] != (0,0):
                if direction_choice:
                    new_square = (hunt[0]['lsquare'][0] - hunt[0]['orientation'][0],
                                  hunt[0]['lsquare'][1] - hunt[0]['orientation'][1])
                else:
                    new_square = (hunt[0]['rsquare'][0] + hunt[0]['orientation'][0],
                                  hunt[0]['rsquare'][1] + hunt[0]['orientation'][1])
            else:
                direction = random.choice(DIRECTIONS)
                new_square = (hunt[0]['lsquare'][0] + direction[0],
                              hunt[0]['lsquare'][1] + direction[1])

        #If the square has already been checked.
        if new_square in ai_checked or not validate_square(new_square,size):
            pass

        #If the square has not been checked.
        else:
            ai_checked.append(new_square)
            return new_square, ai_checked

def ai_opponent_game_loop() -> None:

    '''Ai game loop. takes nothing and returns nothing.

    '''
    ai_checked = []
    if DIFFICULTY != 'easy':
        hunt = []
    print('Welcome to Battleships!')
    print(f'Opponent set to {DIFFICULTY} AI.')
    player_name = input('Please enter your username. ')

    players[player_name] = {'board': initialise_board(BOARD_SIZE), 'ships': create_battleships()}
    players['ai'] = {'board': initialise_board(BOARD_SIZE), 'ships': create_battleships()}
    players[player_name]['board'] = place_battleships(players[player_name]['board'],
                                                    players[player_name]['ships'], 'custom')

    players['ai']['board'] = place_battleships(players['ai']['board'],
                                             players['ai']['ships'], 'random')


    while True:
        coords = cli_coordinates_input()
        if validate_square(coords, BOARD_SIZE):
            attack(coords,players['ai']['board'], players['ai']['ships'])

            #Checks if the player has won.
            if wintest(players['ai']['ships']):
                print(f' {player_name} wins!')
                break

            #Generates AI attack
            if DIFFICULTY == 'easy':
                while True:
                    aicoords = generate_attack(BOARD_SIZE)
                    if aicoords not in ai_checked:
                        break
            else:
                aicoords, ai_checked = generate_advanced_attack(ai_checked,DIFFICULTY,
                                                                hunt,players[player_name]['ships'],
                                                                BOARD_SIZE)
            #Executes AI attack.
            if DIFFICULTY == 'easy':
                attack(aicoords,players[player_name]["board"],
                       players[player_name]["ships"])
                ai_checked.append(aicoords)
            else:
                hunt = advanced_ai_attack(aicoords,players[player_name]['board'],
                                          players[player_name]['ships'],hunt,DIFFICULTY)

            #Checks if the opponent has won.
            if wintest(players[player_name]["ships"]):
                print('AI Potemkin wins! ')
                break
            print_board(players[player_name]['board'])

#Initialises game
if __name__ == '__main__':

    players = {}

    #Obtains and validates config data from config.json file.
    config_data = get_json_data('config.json')
    if not config_data:
        config_data = {'size': 10, 'difficulty': 'hard'}
    global BOARD_SIZE
    BOARD_SIZE = config_data['size']
    DIFFICULTY = config_data['difficulty']
    DIFFICULTY, BOARD_SIZE = validate_config_data(DIFFICULTY,BOARD_SIZE)




    ai_opponent_game_loop()
