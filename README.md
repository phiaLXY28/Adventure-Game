# Adventure Game

A console-based adventure game built in Python featuring exploration, inventory management, scoring, and interactive puzzles.

---

## Overview
This project was developed for **CSC111**.  
Players navigate a grid-based map, collect items, solve puzzles, and manage their inventory to win the game.

---


## Game Map
 7  8  9
 
 4  5  6
 
 1  2  3

 ## Commands
 | Command                    | Description          |
| -------------------------- | -------------------- |
| `look`                     | Inspect surroundings |
| `inventory`                | View items           |
| `score`                    | Check score          |
| `log`                      | View history         |
| `undo`                     | Undo last action     |
| `pick`                     | Pick up item         |
| `drop`                     | Drop item            |
| `go north/south/east/west` | Move                 |
| `clue`                     | Get hints            |
| `puzzle`                   | Trigger puzzle       |
| `quit`                     | Exit game            |


## Inventory System
| Item           | Start | Target |
| -------------- | ----- | ------ |
| minion         | 1     | 8      |
| lucky mug      | 2     | 1      |
| yellow star    | 4     | 2      |
| red star       | 3     | 2      |
| blue star      | 3     | 2      |
| robot          | 6     | 5      |
| ticket         | 4     | 1      |
| laptop charger | 8     | 1      |
| loonie         | 6     | 7      |
| ice cap        | 7     | 9      |
| usb            | 9     | 1      |

## Scoring
Earn points by placing items in their correct locations

Different items give different scores
## Lose Conditions
Reach max steps without collecting required items:

usb

laptop charger

lucky mug

Fail a hard puzzle

## Puzzle System (Enhancement)
Randomly triggered puzzles with difficulty based on progress:

| Level  | Type   | Attempts | Reward      |
| ------ | ------ | -------- | ----------- |
| Easy   | Math   | 1        | Extra steps |
| Medium | Riddle | 3        | Extra steps |
| Hard   | Wordle | 6        | Instant win |

## Implementation Highlights
Modular design with separate puzzle functions

Randomized gameplay for replayability

Optimized Wordle logic using preloaded data

## Key Features
Grid-based exploration

Inventory management system

Score tracking

Undo functionality

Random puzzle encounters

Input validation

# Author
Sophia Lin
