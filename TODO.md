# TODO
## Static set up
- [] implement `Piece`
  - [x] .name
  - [x] .position: (row, col)
  - [] .score : [atk, def]
- [] implement `Item`
  - [] .knight
- [] implement `Knight`
  - [] .item 
- [] implement `Arena`
  - [] .size
  - [] .setup
  - [] .tiles
  - [] .__repr__()

## Equipment
- [] implement knight equip item
- [] implement knight drop item 
- [] implement knight gain item bonus

## Movement
- [] implement direction enum
- [] implement piece movement
- [] implement knight carrying item
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
