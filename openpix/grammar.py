from pyparsing import *
import random

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

class AppParseException(ParseException):
    pass

class Parser(object):
    def __init__(self):
        self.bnf = self.makeBNF()

    def makeCommandParseAction( self, cls ):
        def cmdParseAction(s,l,tokens):
            return cls(tokens)
        return cmdParseAction

    def makeBNF(self):
        moveVerb = oneOf("MOVE GO", caseless=True) | empty
        quitVerb = oneOf("QUIT Q", caseless=True)
        helpVerb = oneOf("H HELP ?",caseless=True)

        itemRef = OneOrMore(Word(alphas)).setParseAction( self.validateItemName )
        nDir = oneOf("N NORTH",caseless=True).setParseAction(replaceWith("N"))
        sDir = oneOf("S SOUTH",caseless=True).setParseAction(replaceWith("S"))
        eDir = oneOf("E EAST",caseless=True).setParseAction(replaceWith("E"))
        wDir = oneOf("W WEST",caseless=True).setParseAction(replaceWith("W"))
        moveDirection = nDir | sDir | eDir | wDir

        moveCommand = moveVerb + moveDirection.setResultsName("direction")
        quitCommand = quitVerb
        helpCommand = helpVerb

        moveCommand.setParseAction(
            self.makeCommandParseAction( MoveCommand ) )
        quitCommand.setParseAction(
            self.makeCommandParseAction( QuitCommand ) )
        helpCommand.setParseAction(
            self.makeCommandParseAction( HelpCommand ) )

        return (
                  moveCommand |
                  helpCommand |
                  quitCommand ).setResultsName("command") + LineEnd()

    def parseCmd(self, cmdstr):
        try:
            ret = self.bnf.parseString(cmdstr)
            return ret
        except AppParseException, pe:
            print pe.msg
        except ParseException, pe:
            print random.choice([ "Sorry, I don't understand that.",
                                   "Huh?",
                                   "Excuse me?",
                                   "???",
                                   "What?" ] )

class Player(object):
    def __init__(self, name):
        self.name = name
        self.gameOver = False
        self.inv = []

    def moveTo(self, rm):
        self.room = rm
        rm.enter(self)
        if self.gameOver:
            if rm.desc:
                rm.describe()
            print "Game over!"
        else:
            rm.describe()

def createRooms( rm ):
    """
    create rooms, using multiline string showing map layout
    string contains symbols for the following:
     A-Z, a-z indicate rooms, and rooms will be stored in a dictionary by
               reference letter
     -, | symbols indicate connection between rooms
     <, >, ^, . symbols indicate one-way connection between rooms
    """
    # start with empty dictionary of rooms
    ret = {}

    # look for room symbols, and initialize dictionary
    # - exit room is always marked 'Z'
    for c in rm:
        if "A" <= c <= "Z" or "a" <= c <= "z":
            if c != "Z":
                ret[c] = Room(c)
            else:
                ret[c] = Exit()

    # scan through input string looking for connections between rooms
    rows = rm.split("\n")
    for row,line in enumerate(rows):
        for col,c in enumerate(line):
            if "A" <= c <= "Z" or "a" <= c <= "z":
                room = ret[c]
                n = None
                s = None
                e = None
                w = None

                # look in neighboring cells for connection symbols (must take
                # care to guard that neighboring cells exist before testing
                # contents)
                if col > 0 and line[col-1] in "<-":
                    other = line[col-2]
                    w = ret[other]
                if col < len(line)-1 and line[col+1] in "->":
                    other = line[col+2]
                    e = ret[other]
                if row > 1 and col < len(rows[row-1]) and rows[row-1][col] in '|^':
                    other = rows[row-2][col]
                    n = ret[other]
                if row < len(rows)-1 and col < len(rows[row+1]) and rows[row+1][col] in '|.':
                    other = rows[row+2][col]
                    s = ret[other]

                # set connections to neighboring rooms
                room.doors=[n,s,e,w]

    return ret

def playGame(p,startRoom):
    # create parser
    parser = Parser()
    p.moveTo( startRoom )
    while not p.gameOver:
        cmdstr = raw_input(">> ")
        cmd = parser.parseCmd(cmdstr)
        if cmd is not None:
            cmd.command( p )
    print
    print "You ended the game with:"
    for i in p.inv:
        print " -", aOrAn(i), i


#====================
# start game definition
roomMap = """
     d-Z
     |
   f-c-e
   . |
   q<b
     |
     A
"""
rooms = createRooms( roomMap )
rooms["A"].desc = "You are standing at the front door."
rooms["b"].desc = "You are in a garden."
rooms["c"].desc = "You are in a kitchen."
rooms["d"].desc = "You are on the back porch."
rooms["e"].desc = "You are in a library."
rooms["f"].desc = "You are on the patio."
rooms["q"].desc = "You are sinking in quicksand.  You're dead..."
rooms["q"].gameOver = True

# define global variables for referencing rooms
frontPorch = rooms["A"]
garden     = rooms["b"]
kitchen    = rooms["c"]
backPorch  = rooms["d"]
library    = rooms["e"]
patio      = rooms["f"]

# create player
plyr = Player("Bob")

# start game
playGame( plyr, frontPorch )
