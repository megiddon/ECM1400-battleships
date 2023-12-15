#Copyright (C) 2023 ****** ******
#This program is licensed under the GNU GPL 3.0 or later.
#This is contained in full in the file LICENSE.txt



''' main web-based game.

'''

import json
import os
import logging
import sys
from math import floor
from uuid import uuid1

try:
    import jinja2
    from flask import Flask, request, session, render_template, jsonify
    from flask_session import Session
except ModuleNotFoundError:
    print('Modules not present! Refer to README.md for instructions on installing.')
    input('Press Enter to quit.')
    sys.exit()

from mp_game_engine import generate_attack, generate_advanced_attack, advanced_ai_attack, validate_config_data
from game_engine import attack, wintest
from components import get_json_data, create_battleships, place_battleships, initialise_board, await_exit

logging.basicConfig(encoding='utf-8',
                    level=logging.INFO,
                    handlers=[logging.FileHandler('gamelog.log'),logging.StreamHandler()],
                    format='%(asctime)s %(levelname)-1s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

#Disables logging of server messages
log = logging.getLogger('werkzeug')
log.disabled = True


app = Flask(__name__)
#Route for /placement url.
@app.route('/placement', methods=['GET', 'POST'])
def placement_interface():

    '''Represents the /placement url.
    GET requests render the template,
    POST requests redirect to the / url.
    '''

    if request.method == 'POST':
        session['aiships'] = create_battleships()

        data = request.get_json()

        #Reloads page if not all of the ships have been placed.
        if len(data) < len(session['player_ships']):
            logging.info('id %s: send game used while not all ships placed', session["ident"])
            return render_template('placement.html',
                                   ships=session['player_ships'],
                                   board_size=session['size'])


        #The spec says the place_battleships method can only take 3 params so we have to do this.

        #Copies data in placement.json into memory.
        placement_data = get_json_data('placement.json')

        #Deletes placement.json from filesystem.
        os.remove('placement.json')

        #Rewrites placement.json with data from user.
        with open('placement.json', 'w') as file_1:
            json.dump(data, file_1)

        player_board = initialise_board(session['size'])
        session['player_board'] = place_battleships(player_board,
                                                    session['player_ships'],
                                                    'custom')

        ai_board = initialise_board(session['size'])
        session['ai_board'] = place_battleships(ai_board,
                                                session['aiships'],
                                                'random')

        #Restores contents of placement.json file.
        os.remove('placement.json')
        with open('placement.json', 'w') as file_2:
            json.dump(placement_data, file_2)

        session['ai_checked'] = []
        logging.info('id %s: ship data successfully sent', session["ident"])
        #Message is arbitrary here.
        return jsonify({'message': 'just according to keikaku'}),1000

    if request.method == 'GET':
        config_data = get_json_data('config.json')
        if not config_data:
            config_data = {'difficulty':'hard', 'size':10}

        session['difficulty'] : dict = config_data['difficulty']
        session['size'] : int = config_data['size']

        session['difficulty'], session['size'] = validate_config_data(
            session['difficulty'], session['size'])

        #Generates a unique ID for a session for identification in the log.
        #Not cryptographically secure but it doesn't
        #Need to be for this particular application.
        session['ident'] = uuid1()
        session['hunt'] : dict = []
        session['player_ships'] : dict[str,int] = create_battleships()
        session['player_hit'] : dict[tuple[int,int],bool] = {}


        #We need to track whether the game is over or not because of a weird bug that I found.
        #If the game ends and the player keeps clicking squares,
        #When the game is reloaded by going to /placement again
        #There'll be a ton of latency for some reason.
        #Obviously we don't want this.
        session['end_flag'] = False


        logging.info('id %s:attempting to load placement page', session["ident"])
        try:
            return render_template('placement.html',
                                   ships=session['player_ships'],
                                   board_size=session['size'])

        except jinja2.exceptions.TemplateNotFound:
            logging.critical('placement.html does not exist!')
            await_exit()

@app.route('/', methods=['GET', 'POST'])
def root():

    '''Represents the / url.
    GET requests render main.html,
    POST requests are not defined.
    '''

    if request.method == 'GET':

        #Attempts to redirect to /main.
        try:
            logging.info('id %s: attempting to load main game', session["ident"])
            return render_template('main.html',
                                   player_board=session['player_board'])

        except jinja2.exceptions.TemplateNotFound:
            logging.critical('main.html does not exist!')

@app.route('/attack', methods=['GET', 'POST'])
def process_attack():


    if request.method == 'GET':

        if session['end_flag']:
            return jsonify({})

        #Parses coordinates from client.
        x_coord = int(request.args.get('x'))
        y_coord = int(request.args.get('y'))

        #Processes the attack.

        #Checks if the square the player hits on has already been hit.
        #Returns a dummy response if this is the case.
        #This kept bugging me with the template so I fixed it.
        if (x_coord, y_coord) in session['player_hit'].keys():
            return jsonify({'hit' : session['player_hit'][(x_coord,y_coord)],
                            'AI_Turn': session['ai_checked'][-1][::-1]})

        hit = attack((x_coord,y_coord), session['ai_board'], session['aiships'])
        session['player_hit'][(x_coord,y_coord)] = hit

        if session['difficulty'] == 'easy':
            while True:
                ai_coords = generate_attack(session['size'])
                if ai_coords not in session['ai_checked']:
                    break
            session['ai_checked'].append(ai_coords)

        else:
            ai_coords, session['ai_checked'] = generate_advanced_attack(session['ai_checked'],
                                                                       session['difficulty'],
                                                                       session['hunt'],
                                                                       session['player_ships'],
                                                                       session['size'])
        #If player wins.
        if wintest(session['aiships']):
            logging.info('game over - Player wins')
            session['end_flag'] = True

            return jsonify({'hit': True,
                            'AI_Turn': ai_coords[::-1],
                            'finished': 'you won!'})
        else:

            #Difficulty implementation.
            if session['difficulty'] == 'easy':
                attack(ai_coords,
                            session['player_board'],
                            session['player_ships'])

            else:
                session['hunt'] = advanced_ai_attack(ai_coords,
                                                            session['player_board'],
                                                            session['player_ships'],
                                                            session['hunt'],
                                                            session['difficulty'])

        #If comp wins.
        if wintest(session['player_ships']):
            session['end_flag'] = True
            logging.info('id %s: game over - AI Wins', session["ident"])
            return jsonify({'hit': hit,
                            'AI_Turn': ai_coords[::-1],
                            'finished': 'you lose!'})

        return jsonify({'hit': hit,
                        'AI_Turn': ai_coords[::-1]})


if __name__ == '__main__':
    SESSION_TYPE = 'filesystem'

    #We're using the flask_session module here to act as a pseudo-global variable.
    #It's basically just a dictionary stored as a cookie on the host's filesystem.
    #Flask sessions are unique to a particular client,
    #so if two browsers access the service at the same time,
    #The two aren't going to interfere with each other.
    #Dealing with global variables with a structure like this is painful.
    #Luckily we have a nice solution that fixes all that.

    app.config.from_object(__name__)
    Session(app)
    app.template_folder = 'templates'
    logging.info('app run')
    app.run()
