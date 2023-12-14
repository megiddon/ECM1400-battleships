import importlib
import inspect
import pytest
from components import *
from game_engine import *
from mp_game_engine import *
import tests.test_helper_functions as thf
import pdb
import os

testReport = thf.TestReport("test_report.txt")

import shutil


#THis is necessary so that we can dynamically modify placement.json for testing.
def rewrite_placement(filename):
    os.remove("placement.json")
    shutil.copyfile(filename, "placement.json")


########################################################################################################################
# Test Components.py functions
########################################################################################################################
@pytest.mark.depends()
def test_components_exists():
    """
    Test if the components module exists.
    """
    try:
        importlib.import_module('components')
    except ImportError:
        testReport.add_message("components module does not exist in your solution.")
        pytest.fail("components module does not exist")


#Tests the integrity of all data stored in external files
def test_choose_advanced_square_return_type():

    """
    Test if the choose_advanced_square function returns a value of the correct type
    """

    # Run the function
    square = choose_advanced_square([], {"A":5}, 2, 10)
    # Check that the return is a tuple
    assert isinstance(square, tuple), "choose_advanced_square does not return a tuple of integers"
    assert isinstance(square[0], int), "choose_advanced_square does not return a tuple of integers"
    assert isinstance(square[1],int), "choose_advanced_square does not return a tuple of integers"
    # check that the length of the tuple is 2
    assert len(square) == 2, "choose_advanced_square returns a tuple of the wrong size"
    # Check that the value of the tuple is the value expected

def test_placement_error_handling():

    """
Checks how the place_battleships function responds to ships of invalid length being placed.
    """
    board = initialise_board()
    ships = create_battleships()
    board = place_battleships(board, ships, "custom")
    
    ships1 = {"A":9001}
    board1 = initialise_board(10)
    assert place_battleships(board1, ships1, "custom") == board, "place_battleships function does not handle massive ships"

    ships2 = {"A":0}
    board2 = initialise_board(10)
    assert place_battleships(board2, ships2, "custom") == board, "place_battleships function does not handle ships of zero length"

    ships3 = {"A":"mudkip"}
    board3 = initialise_board(10)
    assert place_battleships(board3, ships3, "custom") == board, "place_battleships function does not handle ships of non-int length"



#If this test throws up an error then placement.json gets nuked.

def test_bad_ship_placements():
    """Checks how the game responds to bad ship placements."""

    shutil.copyfile("placement.json", "placement_bkp.json")

    noneboard = [[None] * 10] * 10
    oneboard = [["Aircraft_Carrier"] * 5 + [None] * 5] + [[None] * 10] * 9


    #if the coordinates for a ship contain a string that can't be cast to an integer
    board = initialise_board()
    ships = {"Aircraft_Carrier": 5}
    rewrite_placement("tests/bad_placements/test_placement_1.json")
    assert place_battleships(board, ships, "custom")

    #if there is a ship that begins inside the board but ends outside of it
    board2 = initialise_board()
    rewrite_placement("tests/bad_placements/test_placement_2.json")
    assert place_battleships(board2, ships, "custom")

    #if there is a ship that begins outside the board
    rewrite_placement("tests/bad_placements/test_placement_3.json")
    board3 = initialise_board()
    assert place_battleships(board3, ships, "custom")

    #if placement.json contains more ships than are given in battleships.txt
    rewrite_placement("tests/bad_placements/test_placement_5.json")
    board5 = initialise_board()
    assert place_battleships(board5, ships, "custom")

    #if placement.json contains ships with names not in battleships.txt
    rewrite_placement("tests/bad_placements/test_placement_6.json")
    board6 = initialise_board()
    assert place_battleships(board5, ships, "custom")

    os.remove("placement.json")
    shutil.copyfile("placement_bkp.json", "placement.json")
    os.remove("placement_bkp.json")

def test_wintest_output():
    """Tests if the wintest function in game_engine behaves as expected

    """
    assert wintest({"A":5, "B":0}) == False, "wintest function not returning expected value"

    assert wintest({"A":0, "B":0}) == True, "wintest function not returning expected value"

    assert wintest({}) == True, "wintest function not returning expected value"

def test_coord_input_validation():
    """Tests if the validate_coord_input function behaves as expected

    """

    assert validate_coords_input("1,1") == True, "validate_coords_input not function not behaving as expected"

    assert validate_coords_input("") == False, "validate_coords_input not function not behaving as expected"

    assert validate_coords_input("mudkip") == False, "validate_coords_input not function not behaving as expected"

    assert validate_coords_input("10,10") == True, "validate_coords_input not function not behaving as expected"

    assert validate_coords_input("a,1") == False, "validate_coords_input not function not behaving as expected"

    assert validate_coords_input("1 , 1") == False, "validate_coords_input not function not behaving as expected"
