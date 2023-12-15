# Battleships

Copyright megiddon 2023

Made for the ECM1400 Programming module.

## Features Implemented
- Core gameplay as detailed in specification
- Adjustable difficulty implemented through config file. Set to "easy" by default, which is the basic behaviour given in the specification.
- Adjustable board size implemented through config file. Size is set to 10 by default.
- Various quality-of-life additions for the flask interface.
- Series of unit tests written in test_custom.py.
  
## Overview
This program is an implementation of the classic two-player game Battleships in python. The game can be played both in a command-line interface and a web-based interface built with the Flask module.

## Getting Started
-Ensure you have python 3.9 or newer installed.
This can be found [here](https://www.python.org/downloads/.)

**Optional:**
Install the **flask** and **flask-session** modules. These can be installed with the following commands on the terminal and are required to play the game with the web-based interface.

GNU/Linux or MacOS:

***python3 pip install flask***

***python3 pip install flask-session***

Windows:

***python -m pip install flask***

***python -m pip install flask-session***

To play through the command line interface:
- Run **src/mp_game_engine.py**.

To do this through the command line:
- Navigate to **/src** from the **root** directory.
  
GNU/Linux or MacOS:

***python3 mp_game_engine.py***

Windows:

***python mp_game_engine.py***

To play through the web-based interface:
- Run **src/main.py**

To do this through the command line:
- Navigate to **/src** from the **root** directory.
  
GNU/Linux or MacOS:

***python3 main.py***

Windows:

***python main.py***

- Navigate to **127.0.0.1:5000/placement** in a web browser (note: javascript is required for the game to run).
- Once the game is over you must re-enter the above URL in order to play again.


# User Manual

## Changing Battleships

The battleships in the game can be changed through the file **battleships.txt**
- Open **/src/battleships.txt** in a text editor.
- Add a new line for each battleship.
- Write to the line in the format **name**:**length**. For example, an Aircraft Carrier with length 5 would be written as **Aircraft_Carrier:5**, or a Nuclear Submarine with length 2 would be written as **Nuclear_Sumbarine:3**. Note that quotes are not required for the name of the ship or the length and underscores should be used to separate words.

## Changing difficulty and board size

The game's difficulty as well as the size of the game board can be configured.

- Open **/src/config.JSON** in a text editor.
To change the difficulty, replace "easy" with one of the following:

**"easy"**:  The AI guesses randomly and does not sink ships that it has found.

**"medium"**: The AI guesses randomly, but if it finds a ship it will stop guessing randomly to sink that ship.

**"hard"**:  As with Medium, but the AI guesses with polarity. The basis of this is that if the smallest battleship has length 2, then one only needs to search every other square in order to find it. 

**"very hard"**: As with Hard, but the AI's guess is weighted based on the approximate probability that a ship could be in a particular square. This works by counting the number of squares to each side of a ship in each direction, and checking how many ways there are to place a particular ship that would include that square. We assign a score to each square based on this and choose a square randomly based off of that. The results of this vary widely depending on the formula used to assign the score.

**"extreme"**: As with Very Hard, but the polarity that the AI guesses with changes dynamically based on what ships have been sunk. The basis of this is that if the smallest battleship has length n, then we only need to search every nth square in order to find it.

To change the size of the board, replace the number **10** with a positive integer of your choice. Be aware that very large board sizes may not render in the web-based interface. Proceed at your own risk.
  
## Testing

In order to run the tests written for the application:
- Navigate into the **/src** directory in the command line.
- Enter the following:
  
**GNU/Linux or MacOS** :
  
python3 -pytest

**Windows**:

python -m pytest 

The **pytest** and **pytest-depends** modules must be installed. To do this, open the terminal and enter the folllowing:

GNU/Linux or MacOS:  

**python3 pip install pytest**

**python3 pip install pytest-depends**

Windows:  

**python -m pip install pytest**

**python -m pip install pytest-depends**


## Logging

The program keeps a devlog. This can be found at **/src/gamelog.log** and is openable in a text editor.
## Documentation
Documentation of each module can be found in the **/docs** folder of the root directory. These are automatically generated using [Sphinx](https://www.sphinx-doc.org/en/master/). 
To open the documentation, navigate to **/docs/build/html/** and open **index.html** in a browser. In the future the documentation will be pushed to ReadTheDocs and this section will be updated accordingly.


To remake the documentation using sphinx:

-Install the **sphinx** and **autodoc** modules. To do this in the command line:

GNU/Linux or MacOS:

**python3 pip install sphinx**

**python3 pip install autodoc**

Windows:

**python -m pip install sphinx**

**python -m pip install autodoc**

-**Optional** - If you are forking this project, you should edit **conf.py** in the **docs** directory, which contains information about the project that is used to generate the documentation.

**Optional** - If you are adding new files to the program, you should navigate to the **docs** folder in the command line and run the following:

**sphinx-apidoc -o ./source ../src**

This will generate new **.html** files for each module created.

To compile the documentation:

GNU/Linux or MacOS:

Navivate to the **docs** folder in the command line and run **Makefile**

Windows:

Navigate to the **docs** folder in the command line and run **make html**

Note that the documentation is automatically generated based off the docstrings in each module. Docstrings must be structured in [reST](https://peps.python.org/pep-0287) format. More information on this can be found [here](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html).

## License

This program is licensed under the GNU GPL 3.0, which is contained in full in the file **license.txt**.


## Contact
The source code for this project can be found at **https://github.com/megiddon/ECM1400-battleships.**

Issues should be raised at **https://github.com/megiddon/ECM1400-battleships/issues.**

All other concerns should be directed to **megiddon@outlook.com**.
