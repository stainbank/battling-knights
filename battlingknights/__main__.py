import functools

from battlingknights.pieces import Knight, Item, Position, Direction
from battlingknights.game import Arena


LIMITS = (7, 7)
BASE_STATS = (1, 1)


def make_pieces():
    knights = {
        'R': Knight('RED', (0, 0), BASE_STATS),
        'B': Knight('BLUE', (7, 0), BASE_STATS),
        'G': Knight('GREEN', (7, 7), BASE_STATS),
        'Y': Knight('YELLOW', (0, 7), BASE_STATS),
    }
    items = [  # in priority order
        Item('Axe', (2, 2), (2, 0)),
        Item('MagicStaff', (5, 2), (1, 1)),
        Item('Dagger', (2, 5), (1, 0)),
        Item('Helmet', (5, 5), (1, 1)),
    ]
    return knights, items


def choose_by_order(tile_items, ordered_items):
    for item in ordered_items:
        if item in tile_items:
            return item
    else:
        return None


def make_instructions(knights, filepath='moves.txt'):
    directions = {'N': Direction.NORTH, 'E': Direction.EAST,
                  'S': Direction.SOUTH, 'W': Direction.WEST}
    with open(filepath) as o:
        raw_instructions = iter(o.read().splitlines())

    def instructions():
        start_code = next(raw_instructions)
        assert start_code == 'GAME-START'
        for instruction in raw_instructions:
            if instruction == 'GAME-END':
                return
            knight, direction = instruction.split(':')
            yield knights[knight], directions[direction]
    return instructions()


def main():
    knights, items = make_pieces()
    item_chooser = functools.partial(choose_by_order, ordered_items=items)
    arena = Arena(LIMITS, item_chooser=item_chooser)
    arena.set_pieces(*knights.values(), *items)
    instructions = make_instructions(knights)
    for knight, direction in instructions:
        arena.run_instruction(knight, direction)
        print(knight.name, knight.position)


if __name__ == '__main__':
    main()
