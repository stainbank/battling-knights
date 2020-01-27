class BattlingKnightsException(Exception):
    pass


class InvalidMoveException(BattlingKnightsException):
    pass


class OutsideLimitsException(InvalidMoveException):
    pass


class InvalidGameStateException(BattlingKnightsException):
    pass
