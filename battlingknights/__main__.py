import functools
import json

from battlingknights.pieces import Knight, Item, Position, Direction
from battlingknights.game import Arena


LIMITS = (7, 7)
BASE_STATS = (1, 1)


def make_pieces():
    knights = {
        'R': Knight('red', (0, 0), BASE_STATS),
        'B': Knight('blue', (7, 0), BASE_STATS),
        'G': Knight('green', (7, 7), BASE_STATS),
        'Y': Knight('yellow', (0, 7), BASE_STATS),
    }
    items = [  # in priority order
        Item('axe', (2, 2), (2, 0)),
        Item('magic_staff', (5, 2), (1, 1)),
        Item('dagger', (2, 5), (1, 0)),
        Item('helmet', (5, 5), (1, 1)),
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


def get_final_state(knights, items):
    state = {
        **{knight.name: make_knight_state(knight) for knight in knights},
        **{item.name: make_item_state(item) for item in items}
    }
    return state


def make_knight_state(knight):
    position = tuple(knight.position) if knight.position else None
    status = knight.status.name
    item = knight.item.name if knight.item else None
    attack, defense = knight.attack, knight.defense
    return (position, status, item, attack, defense)


def make_item_state(item):
    position = tuple(item.position)
    equipped = bool(item.knight)
    return (position, equipped)


def main():
    knight_mapping, items = make_pieces()
    knights = knight_mapping.values()
    item_chooser = functools.partial(choose_by_order, ordered_items=items)
    arena = Arena(LIMITS, item_chooser=item_chooser)
    arena.set_pieces(*knights, *items)
    for knight, direction in make_instructions(knight_mapping):
        arena.run_instruction(knight, direction)
    state = get_final_state(knights, items)
    with open('final_state.json', 'w') as o:
        json.dump(state, o)


if __name__ == '__main__':
    main()
