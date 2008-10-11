import random

from pyparsing import *


def aOrAn( item ):
    if item.desc[0] in "aeiou":
        return "an"
    else:
        return "a"

def enumerateItems(l):
    if len(l) == 0: return "nothing"
    out = []
    for item in l:
        if len(l)>1 and item == l[-1]:
            out.append("and")
        out.append( aOrAn( item ) )
        if item == l[-1]:
            out.append(item.desc)
        else:
            if len(l)>2:
                out.append(item.desc+",")
            else:
                out.append(item.desc)
    return " ".join(out)


class Command(object):
    "Base class for commands"
    def __init__(self, verb, verbProg):
        self.verb = verb
        self.verbProg = verbProg

    @staticmethod
    def helpDescription():
        return ""

    def _doCommand(self, player):
        pass

    def __call__(self, player ):
        print self.verbProg.capitalize()+"..."
        self._doCommand(player)


class MoveCommand(Command):
    def __init__(self, quals):
        super(MoveCommand,self).__init__("MOVE", "moving")
        self.direction = quals["direction"][0]

    @staticmethod
    def helpDescription():
        return """MOVE or GO - go NORTH, SOUTH, EAST, or WEST
          (can abbreviate as 'GO N' and 'GO W', or even just 'E' and 'S')"""

    def _doCommand(self, player):
        rm = player.room
        nextRoom = rm.doors[
            {
            "N":0,
            "S":1,
            "E":2,
            "W":3,
            }[self.direction]
            ]
        if nextRoom:
            player.moveTo( nextRoom )
        else:
            print "Can't go that way."


class QuitCommand(Command):
    def __init__(self, quals):
        super(QuitCommand,self).__init__("QUIT", "quitting")

    @staticmethod
    def helpDescription():
        return "QUIT or Q - ends the game"

    def _doCommand(self, player):
        print "Ok...."
        player.gameOver = True


class HelpCommand(Command):
    def __init__(self, quals):
        super(HelpCommand,self).__init__("HELP", "helping")

    @staticmethod
    def helpDescription():
        return "HELP or H or ? - displays this help message"

    def _doCommand(self, player):
        print "Enter any of the following commands (not case sensitive):"
        for cmd in [
            MoveCommand,
            QuitCommand,
            HelpCommand,
            ]:
            print "  - %s" % cmd.helpDescription()
        print






