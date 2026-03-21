"""CSC111 Project 1: Text Adventure Game - Simulator

Instructions (READ THIS FIRST!)
===============================

This Python module contains code for Project 1 that allows a user to simulate an entire
playthrough of the game. Please consult the project handout for instructions and details.

You can copy/paste your code from the ex1_simulation file into this one, and modify it as needed
to work with your game.

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
from typing import Any
from proj1_event_logger import Event, EventList
from adventure import AdventureGame
from game_entities import Location


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    # Private Instance Attributes:
    #   - _game: The AdventureGame instance that this simulation uses.
    #   - _events: A collection of the events to process during the simulation.
    #   - _inventory: A list with all the items player picked up
    #   - _score: An int representing the score of the player
    _game: AdventureGame
    _events: EventList
    _inventory: list[str]
    _score: int
    _expect: Any

    def __init__(self, game_data_file: str, initial_location_id: int, commands: list[str], expect: Any) -> None:
        """Initialize a new game simulation based on the given game data, that runs through the given commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """
        self._events = EventList()
        self._game = AdventureGame(game_data_file, initial_location_id)
        self._inventory = []
        self._score = 0
        self._expect = expect

        # Hint: self._game.get_location() gives you back the current location
        initial_location = self._game.get_location()
        initial_event = Event(initial_location_id, initial_location.descriptions.long_description, [],
                              0, next_command=None)
        self._events.add_event(initial_event)

        # Hint: Call self.generate_events with the appropriate arguments
        self.generate_events(commands, initial_location)

    def generate_events(self, commands: list[str], current_location: Location) -> None:
        """Generate all events in this simulation.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """
        counter = -1
        for command in commands:
            counter += 1
            if command == "inventory":
                assert self._expect == self._inventory
            elif command == "score":
                assert self._expect == self._score
            elif command == "pick":
                self._game.pick(current_location, commands[counter + 1], self._inventory)
            elif command == "drop":
                self._score += self._game.drop(commands[counter + 1], current_location, self._inventory)
            elif command in current_location.available_commands:
                next_location_id = current_location.available_commands[command]
                next_location = self._game.get_location(next_location_id)
                event = Event(next_location.id_num, next_location.descriptions.long_description,
                              self._events.last.inventory.copy(),
                              self._events.last.score)
                self._events.add_event(event, command)
                current_location = next_location

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.

        >>> expect = [1,2]
        >>> sim = AdventureGameSimulation('game_data.json', 1, ["go east"], expect)
        >>> sim.get_id_log()
        [1, 2]

        >>> expect = [1,2,3]
        >>> sim = AdventureGameSimulation('game_data.json', 1, ["go east", "go east"], expect)
        >>> sim.get_id_log()
        [1, 2, 3]
        """

        # Note: We have completed this method for you. Do NOT modify it for ex1.

        return self._events.get_id_log()

    def run(self) -> None:
        """Run the game simulation and log location descriptions."""

        # Note: We have completed this method for you. Do NOT modify it for ex1.

        current_event = self._events.first  # Start from the first event in the list

        while current_event:
            print(current_event.description)
            if current_event is not self._events.last:
                print("You choose:", current_event.next_command)

            # Move to the next event in the linked list
            current_event = current_event.next


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })
    win_walkthrough = ["go north", "pick", "yellow star", "pick", "ticket", "go south", "drop", "ticket", "pick",
                       "minion", "go east", "drop", "yellow star", "go east", "pick", "red star", "go west", "drop",
                       "red star", "go north", "go east", "pick", "robot", "pick", "loonie", "go west", "drop", "robot",
                       "pick", "blue star", "go north", "drop", "minion", "pick", "laptop charger", "go west", "drop",
                       "loonie", "pick", "ice cap", "go east", "go east", "drop", "ice cap", "pick", "usb", "go south",
                       "go west", "go south", "drop", "blue star", "pick", "lucky mug", "go west", "drop", "lucky mug",
                       "drop", "laptop charger", "drop", "usb"]

    expected_log = [1, 4, 1, 2, 3, 2, 5, 6, 5, 8, 7, 8, 9, 6, 5, 2, 1]
    sim = AdventureGameSimulation('game_data.json', 1, win_walkthrough, expected_log)
    assert expected_log == sim.get_id_log()

    # Create a list of all the commands needed to walk through your game to reach a 'game over' state
    lose_demo = ["go north", "pick", "yellow star", "pick", "ticket", "go south", "drop", "ticket", "pick",
                 "minion", "go east", "drop", "yellow star", "go east", "pick", "red star", "go west", "drop",
                 "red star", "go north", "go east", "pick", "robot", "pick", "loonie", "go west", "drop", "robot",
                 "pick", "blue star", "go north", "drop", "minion", "pick", "laptop charger", "go west", "drop",
                 "loonie", "pick", "ice cap", "go east", "go east", "drop", "ice cap", "pick", "usb", "go south",
                 "go west", "go south", "drop", "blue star", "pick", "lucky mug", "go west", "drop", "lucky mug",
                 "drop", "laptop charger", "go north", "go south", "go east", "go east", "go west", "go north",
                 "go east", "go west", "go north", "go west", "go east", "go east", "go south",
                 "go west", "go south", "go west", "go north", "go south", "go east", "go east", "go west", "go north",
                 "go east", "go west", "go north", "go west", "go east", "go east", "go south",
                 "go west", "go south", "go west", "go north", "go south"]
    expected_log = [1, 4, 1, 2, 3, 2, 5, 6, 5, 8, 7, 8, 9, 6, 5, 2, 1,
                    4, 1, 2, 3, 2, 5, 6, 5, 8, 7, 8, 9, 6, 5, 2, 1,
                    4, 1, 2, 3, 2, 5, 6, 5, 8, 7, 8, 9, 6, 5, 2, 1, 4, 1]
    # Uncomment the line below to test your demo
    sim = AdventureGameSimulation('game_data.json', 1, lose_demo, expected_log)
    assert expected_log == sim.get_id_log()

    inventory_demo = ["go north", "pick", "yellow star", "pick", "ticket", "inventory"]
    expected_log = ["yellow star", "ticket"]
    sim = AdventureGameSimulation('game_data.json', 1, inventory_demo, expected_log)

    scores_demo = ["go north", "pick", "yellow star", "pick", "ticket", "go south", "drop", "ticket", "go east",
                   "drop", "yellow star", "score"]
    expected_log = 3
    s = AdventureGameSimulation('game_data.json', 1, scores_demo, expected_log)

    # Add more enhancement_demos if you have more enhancements
    # The enhancement requires user input
