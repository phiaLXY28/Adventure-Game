"""CSC111 Project 1: Text Adventure Game - Game Entities

Instructions (READ THIS FIRST!)
===============================

This Python module contains the entity classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from dataclasses import dataclass


@dataclass
class Descriptions:
    """A location in our text adventure game world.

        Instance Attributes:
            - brief_description: Short description of this location
            - long_description: Long description of this location

        Representation Invariants:
            - self.brief_description != ''
            - self.long_description != ''
        """
    brief_description: str
    long_description: str


@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - id_num: Integer id of this location
        - name: name of the location
        - descriptions: Short and short description of this location
        - available_commands: String command which leads this location to the next location
        - items: Items available at this location
        - visited: Boolean showing if visited
        - clue: clue to the wordle
        - commands: all possible commands that could happen at this location, use for testing only

    Representation Invariants:
        - self.id_num > 0
        - self.name != ''
        - self.brief_description != ''
        - self.long_description != ''
        - self.clue != ''
    """
    id_num: int
    name: str
    descriptions: Descriptions
    available_commands: dict[str, int]
    items: list[str]
    visited: bool
    clue: str


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: A string representing the name of item
        - description: A description of the item
        - start_position: An int representing the location ID of where the item is initially located
        - target_position: the location ID of where the item is to be deposited for credit
        - target_point: the number of points received for depositing the item in that credit location
        - preconditions: items required to pick up current item

    Representation Invariants:
        - self.name != ''
        - self.description != ''
        - self.start_position >= 0
        - self.target_position >= 0
        - self.target_points >= 0
    """
    name: str
    description: str
    start_position: int
    target_position: int
    target_points: int
    preconditions: list[str]


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })
