# uncompyle6 version 2.9.11
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Nov 17 2016, 17:05:23) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/tianyu/Programming/liubot_telegram/exceptions.py
# Compiled at: 2017-05-12 18:20:01
# Size of source mod 2**32: 373 bytes


class TicTacToeError(Exception):
    pass


class PlayerLimitError(TicTacToeError):
    pass


class AlreadyJoinedError(TicTacToeError):
    pass


class NotInGameError(TicTacToeError):
    pass


class GameStartedError(TicTacToeError):
    pass


class TooFewPlayersError(TicTacToeError):
    pass


class InvalidMoveError(TicTacToeError):
    pass


class GameNotStartedError(TicTacToeError):
    pass
# okay decompiling __pycache__/exceptions.cpython-35.pyc
