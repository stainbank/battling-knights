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
- [] implement `Arena`
  - [] .size
  - [] .setup
  - [] .tiles
  - [] .__repr__()

## Equipment
- [x] implement knight equip item
- [x] implement knight drop item 
- [x] implement knight gain item bonus

## Movement
- [x] implement direction enum
- [x] implement piece movement
- [x] implement knight carrying item
- [] implement Arena limits
  - [] position change checks limits
  - [] implement drowning
  - [] implement item dropping

## Fighting
- [] implement knight .status
- [] implement knight suprise bonus
- [] implement knight attack knight
- [] implement knight die
  - [] item dropping 
  - [] status change

## Game
- [] implement instructions
- [] implement logging
- [] implement final state output
- [] write README

## Extras
- [] read initialisation from config
- [] make installable package
- [] implement CLI
