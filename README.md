# Battleships
Copyright megidderp 2023
Made for the ECM1400 Programming module.

## Features Implemented
- Core gameplay as detailed in specification
- Adjustable difficulty implemented through config.py
- Series of unit tests written in test_custom.py

## Overview
This program is an implementation of the classic two-player game Battleships in python. The game can be played both in a command-line interface and a web-based interface built with the Flask module.

## Getting Started
-Ensure you have python 3.9 or newer installed.
This can be found at https://www.python.org/downloads/.

**Optional:**
-Install the **flask** and **flask_session** modules. These can be installed with the following commands on the terminal and are required to play the game with the web-based interface.

GNU/Linux or MacOS:

***python3 pip install flask***

***python3 pip install flask_session***

Windows:

***python -m pip install flask***

***python -m pip install flask_session***

To play through the command line interface:
- Run **src/mp_game_engine.py**.

To do this through the command line:
- Navigate to **/src** from the **root** directory.
- 
GNU/Linux or MacOS:

***python3 mp_game_engine.py***

Windows:

***python mp_game_engine.py***

To play through the web-based interface:
- Run **src/main.py**

To do this through the command line:
- Navigate to **/src** from the **root** directory.
- 
GNU/Linux or MacOS:

***python3 main.py***

Windows:

***python main.py***

- Navigate to **127.0.0.1:5000/placement** in a web browser (note: javascript is required for the game to run).
- Once the game is over you must re-enter the above URL in order to play again.

## Configuration

The game's difficulty as well as the size of the game board can be configured.

- Open config.JSON in a text editor.
To change the difficulty, replace "hard" with one of the following:

**"easy"**:  The AI guesses randomly and does not sink ships that it has found.

**"medium"**: The AI guesses randomly, but if it finds a ship it will stop guessing randomly to sink that ship.

**"hard"**:  As with Medium, but the AI guesses with polarity.

**"very hard"**: As with Hard, but the AI's guess is weighted based on the approximate probability that a ship could be in a particular square.

**"extreme"**: As with Very Hard, but the polarity that the AI guesses with changes dynamically based on what ships have been sunk.

- To change the size of the board, replace the number **10** with a positive integer of your choice. Be aware that very large board sizes may not render in the web-based interface.
## Testing

In order to run the tests written for the application:
- Navigate into the **/src** directory in the command line.
- Enter the following:
- **GNU/Linux or MacOS** :
python3 -pytest
- **Windows**:
python -m pytest 

The **pytest** and **pytest-depends** modules must be installed. To do this, open the terminal and enter the folllowing:

GNU/Linux or MacOS:  
_**python3 pip install pytest**_  
Windows:  
_**python -m pip install pytest**_  

## License

This program is licensed under the GNU GPL 3.0, which is contained in full in the file **license.txt**.


## Contact
The source code for this project can be found at **https://github.com/megidderp/ECM1400-battleships.**

Issues should be raised at **https://github.com/megidderp/ECM1400-battleships/issues.**

All other concerns should be directed to **megidderp@outlook.com**.
