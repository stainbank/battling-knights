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
- [] implement `Arena`
  - [x] .limits
  - [x] .pieces
- [x] implement piece setting
- [] implement tile
  - [] .items
  - [] .knight
- [] implement instructions
- [] implement item ordering
- [] implement logging
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
- [] make installable package
- [] implement CLI
- [] implement arena visualisation
