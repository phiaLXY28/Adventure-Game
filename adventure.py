"""CSC111 Project 1: Text Adventure Game - Game Manager

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from __future__ import annotations
import json
from typing import Optional, Any
import random
from random import randrange

from game_entities import Location, Item, Descriptions
from proj1_event_logger import Event, EventList
# from hypothesis.stateful import precondition
# from scipy.stats import false_discovery_control


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - _location: dictionary storing all the locations
        - _items: list storing all the items
        - current_location_id: ID of current location in the game
        - ongoing: boolean check if game is ongoing
        - puzzle: the word for wordle

    Representation Invariants:
        - self.current_location_id in self._locations
        - all(isinstance(loc_id, int) and isinstance(loc, Location) for loc_id, loc in self._locations.items())
        - all(isinstance(name, str) and isinstance(item, Item) for name, item in self._items.items())
        - isinstance(self.puzzle, str) and len(self.puzzle) > 0
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a mapping from item name to Item object.
    #                       This represents all the items in the game.

    _locations: dict[int, Location]
    _items: dict[str, Item]
    current_location_id: int
    ongoing: bool
    puzzle: str

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """

        self._locations, self._items, self.puzzle = self._load_game_data(game_data_file)
        self.current_location_id = initial_location_id  # game begins at this location
        self.ongoing = True  # whether the game is ongoing

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], dict[str, Item], str]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a dictionary of all Item objects."""
        words = ["tree", "gold", "jump", "fire", "moon", "wind", "rain", "clock"]
        puzzle_word = random.choice(words)  # choose a random word for the puzzle
        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations_lst = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location(loc_data['id'], loc_data["name"], Descriptions(loc_data['brief_description'],
                                    loc_data['long_description']), loc_data['available_commands'],
                                    loc_data['items'], False, loc_data["clue"].get(puzzle_word))

            locations_lst[loc_data['id']] = location_obj

        items_lst = {}
        for data in data["items"]:
            item_ob = Item(data["name"], data["description"], data["start_position"], data["target_position"],
                           data["target_points"], data["preconditions"])
            items_lst[item_ob.name] = item_ob

        return locations_lst, items_lst, puzzle_word

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """
        if loc_id is None:
            return self._locations.get(self.current_location_id)
        return self._locations.get(loc_id)

    def precondition_pick(self, require_elements: list[str]) -> bool:
        """before picking up items, check if all the required elements are in place"""
        for i in require_elements:
            if i not in self._locations.get(self._items.get(i).target_position).items:
                return False
        return True

    def pick(self, curr_loc: Location, item: str, inventories: list[str]) -> bool:
        """Check if the item player wants to pick is available at the location,
        and pick it up if it's available.
        """
        require_elements = self._items.get(item).preconditions
        item_obj = self._items.get(item)

        if item_obj.target_position == curr_loc.id_num:
            print("This item belongs here. You can no longer pick it up.")
            return False
        if item in curr_loc.items and self.precondition_pick(require_elements):
            # check if all required items are in place
            curr_loc.items.remove(item)
            print(item_obj.description)
            inventories.append(item)
            return True
        else:
            print("Please find required items to pick up this item.")
            return False

    def drop(self, item: str, curr_loc: Location, inventories: list[str]) -> int:
        """drop the item in player's inventory to the correct place"""
        item_ob = self._items.get(item)
        if curr_loc.id_num == item_ob.target_position:  # dropped at correct place
            inventories.remove(item)
            curr_loc.items.append(item)
            print("Congrats, you have earned " + str(item_ob.target_points) + (" points by dropping item to "
                                                                               "the correct position"))
            return item_ob.target_points
        else:
            print("This item doesn't belong here")
            return 0

    def undo(self, prev_inven: list[str], cur_event: list[str]) -> None:
        """undo a drop/pick action"""
        if len(prev_inven) < len(cur_event):  # undo a "pick" action
            item = [x for x in cur_event if x not in prev_inven][0]
            self._locations.get(self._items.get(item).target_position).items.remove(item)
        else:  # undo a "drop" action
            item = [x for x in prev_inven if x not in cur_event][0]
            self._locations.get(self._items.get(item).start_position).items.append(item)

    @staticmethod
    def wordle(word: str) -> tuple[bool, str]:
        """wordle: if user wins gets extra steps, else remove 3 steps"""
        print("\n\nThis is a wordle game. Base on the clues, you have 5 times to guess the correct word. "
              "\nGuessing correct word will win. Unable to guess the word will loose"
              "\nEach time the system will tell you how many letters are correct "
              "and how many letters are in correc positions. Good Luck")
        solution = list(word)  # parse word into list of letters
        counter = 0
        while counter < 5:
            counter += 1
            print("It's a " + str(len(word)) + " letter word")
            ipt_guess = (input("\nPlease enter your guess: ").lower().strip())
            guess = list(ipt_guess)
            if len(ipt_guess) != len(word):  # The length is not correct
                print("Note: it's a " + str(len(word)) + " letter word")
            elif guess == solution:
                return True, "H"
            else:
                correct_position = sum(guess[i] == solution[i] for i in range(len(solution)))  # Count correct positions
                correct_letters = sum(min(guess.count(letter), solution.count(letter)) for letter in solution)
                # count correct letters
                print("Correct positions: " + str(correct_position) + "\n Correct letters: " + str(correct_letters))
                print("You have " + str(5 - counter) + " chances left")
        print("The correct word is: " + word)
        return False, "H"

    @staticmethod
    def math_puzzle() -> tuple[bool, str]:
        """A simple math puzzle."""
        num1, num2 = random.randint(10, 50), random.randint(1, 10)
        correct_answer = num1 * num2  # Multiplication problem

        print("\n MATH CHALLENGE:\n You have one change ")
        print(f"Solve: {num1} × {num2}")
        try:
            attempt = int(input("Your answer: "))
        except ValueError:
            print("Invalid input! You failed.")
            return False, "E"
        if attempt == correct_answer:
            print("Correct! You may proceed.")
            return True, "E"
        else:
            print(f"Incorrect! The correct answer was {correct_answer}.")
            return False, "E"

    @staticmethod
    def riddle_puzzle() -> tuple[bool, str]:
        """A riddle puzzle."""
        riddles = {
            "I speak without a mouth and hear without ears. I have no body, but I come alive with wind.": "echo",
            "The more of me you take, the more you leave behind.": "footsteps",
            "I can be cracked, made, told, and played.": "joke"
        }
        riddle, answer = random.choice(list(riddles.items()))

        print("\nRIDDLE CHALLENGE:\n You have 3 chances to guess the correct answer\n")
        counter = 0
        while counter < 3:
            print(riddle)
            attempt = input("Your answer: ").lower().strip()
            counter += 1
            if attempt == answer:
                print("Correct! You may proceed.")
                return True, "M"
            else:
                print("Incorrect!")
        return False, "M"

    @staticmethod
    def win_lose(step: int, loc: Location) -> Any:
        """check win/lose condition"""
        total_item = ["ticket", "usb", "lucky mug", "laptop charger"]
        if step > 70:
            print("Already 4pm, you loose")
            return False
        elif loc.id_num == 1 and all([i in loc.items for i in total_item]):
            print("You have collected all the require items, and got back to dorm on time. Continue working!")
            return True
        return None

    def advanced_puzzle(self, word: str, player_steps: int) -> Any:
        """advanced puzzle section"""
        print("You have entered the puzzle world. There are 3 types of puzzles: easy, medium, hard. "
              "You will get each base on how many steps you have taken: \n 0 - 25 steps: hard level"
              "\n 25 - 50 steps: medium level"
              "\n 51 or above: easy level"
              "\n Complete easy or medium level puzzle will award you with 3 or 5 steps. "
              "Unable to complete will loose 1 or 3 steps"
              "\n Complete hard level puzzle will automatically win the game. Else you loose the game"
              "\n QUIT NOW BEFORE IT'S TOO LATE. Current steps: " + str(player_steps))
        end = input("Type quit to quit, else game start: ").lower().strip()
        if end == "quit":
            return False, "Q"
        elif player_steps < 5:
            print("You have too much steps left. Explore the map and then come back")
            return False, "Q"
        if player_steps <= 25:
            return self.wordle(word)
        elif player_steps <= 50:
            return self.riddle_puzzle()
        else:
            return self.math_puzzle()

    @staticmethod
    def open_puzzle(menu_list: list[str]) -> bool:
        """Randomly open up puzzle during the game"""
        menu_list.extend(["puzzle", "clue"])
        print("Congrads, you have encounted a mystery multi-type puzzle."
              " Clues for hard level puzzles have been distributed to different locations, simply type clue"
              "\nWhen you are ready, input puzzle")
        return True

    @staticmethod
    def puzzle_result(result_of_puzzle: bool, level: str) -> Any:
        """check if player finish the puzzle correctly, return award or "punishment" """
        if result_of_puzzle:
            if level == "H":
                print("You win! A mystery elf have helped you collect all items needed. "
                      "Time to go back to your dorm and finish your work")
                return None
            elif level == "M":
                return -5
            else:
                return -3
        elif not result_of_puzzle:
            if level == "H":
                print("You have been stuck in the puzzle for too long. Already passed 4pm. You loose")
                return None
            elif level == "M":
                return 3
            elif level == "E":
                return 1
        return 0


if __name__ == "__main__":

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })

    game_log = EventList()
    game = AdventureGame('game_data.json', 1)
    menu = ["look", "inventory", "score", "log", "quit", "undo"]  # Regular menu options available at each location
    actions = ["pick", "drop"]
    choice = None
    inventory = []
    score = 0
    steps = 0
    puzzle = False

    while game.ongoing:
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your marks will be based on how well-organized your code is.

        location = game.get_location()
        if choice not in menu and choice != "None":
            steps += 1
            game_log.add_event(Event(location.id_num, location.descriptions.brief_description,
                                     inventory=inventory.copy(), score=score), command=choice)

        if not location.visited:  # check type of description to print
            print("\n" + location.descriptions.long_description)
            location.visited = True
        else:
            print("\n" + location.descriptions.brief_description)

        # Display possible actions at this location
        print("What to do? Choose from: " + ", ".join(menu))
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        while choice not in location.available_commands and choice not in menu and choice not in actions:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()

        print("========")
        print("You decided to:", choice)

        if choice in menu:
            if choice == "log":
                game_log.display_events()
            elif choice == "look":
                print(location.descriptions.long_description)
            elif choice == "inventory":
                print(game_log.last.inventory)
            elif choice == "score":
                print(score)
            elif choice == "quit":
                print("Thanks for playing")
                break

            elif choice == "undo":
                if len(game_log) == 1:
                    print("You haven't done anything yet")
                else:
                    remove_event = game_log.last
                    prev_command = remove_event.prev.next_command  # command that led to this event
                    steps -= 1
                    game_log.remove_last_event()
                    game.current_location_id = game_log.last.id_num
                    inventory = game_log.last.inventory.copy()  # copy the previous inventory
                    score = game_log.last.score  # copy the previous score
                    if prev_command in {"pick", "drop"}:  # remove/add items to inventory
                        game.undo(remove_event.inventory, inventory)

            elif choice == "puzzle":
                results, levels = game.advanced_puzzle(game.puzzle, steps)
                output = game.puzzle_result(results, levels)  # check if user win the puzzle
                if output is None:  # user win/loose hard level puzzle, game ends
                    break
                steps += output

            elif choice == "clue":
                print(location.clue)
        else:
            if choice == "pick":
                if len(location.items) == 0:
                    print("No items here")
                    choice = "None"
                else:
                    print("Which item do you want to pick up: " + ", ".join(location.items))
                    ipt = input("\n: ").lower().strip()
                    if ipt in location.items:
                        item_picked = game.pick(location, ipt, inventory)
                        if not item_picked:
                            choice = "None"
                    else:
                        print("Item not available")
                        choice = "None"

            elif choice == "drop":
                if len(inventory) == 0:
                    print("No items in your inventory")
                    choice = "None"
                else:
                    print("Which item do you want to drop: " + ", ".join(inventory))
                    ipt = input(": ").lower().strip()
                    if ipt in inventory:
                        output = game.drop(ipt, location, inventory)
                        if output == 0:  # item does not belong here
                            choice = "None"
                        score += output
                    else:
                        print("Item not available")
                        choice = "None"
            else:  # directions command
                result = location.available_commands[choice]
                game.current_location_id = result

        result = game.win_lose(steps, location)  # check if player win/lose
        if result is not None:
            break
        if randrange(5) == 2 and not puzzle:
            puzzle = AdventureGame.open_puzzle(menu)
