# TODO
## Static set up
- [x] implement `Piece`
  - [x] .name
  - [x] .position: (row, col)
  - [x] .score : [atk, def]
- [x] implement `Item`
  - [x] .knight
- [x] implement `Knight`
  - [x] .item 

## Equipment
- [x] implement knight equip item
- [x] implement knight drop item 
- [x] implement knight gain item bonus

## Movement
- [x] implement direction enum
- [x] implement piece movement
- [x] implement knight carrying item
- [x] implement Arena limits
  - [x] position change checks limits
  - [x] implement drowning
  - [x] implement item dropping

## Fighting
- [x] implement knight .status
- [x] implement knight suprise bonus
- [x] implement knight attack knight
- [x] implement knight die
  - [x] item dropping
  - [x] status change
  - [x] movement forbidden

## Game
- [x] implement `Arena`
  - [x] .limits
  - [x] .pieces
- [x] implement piece setting
- [x] implement `Tile`
  - [x] .items
  - [x] .knight
- [] implement item ordering
- [x] implement instruction
  - [x] implement item pickup
  - [x] implement knight encounter
- [x] implement instructions from text
- [] implement final state output
- [] write README

# Clean up
- [] Ensure full type annotations
- [x] Remove duplication in test suite
- [] Remove unused imports
- [] Use consistent imports
- [] Order definitions appropriately

## Extras
- [] read initialisation from config
- [] implement logging
- [] make installable package
- [] implement CLI
- [] implement arena visualisation
- [] refactor move checking to arena
  - [] knight.move_to(position)
