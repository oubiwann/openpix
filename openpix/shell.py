from openpix import art
from openpix import meta
from openpix.parser import Parser


starterHelp = "Type help or '?' for a list of available commands."


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


def playGame(p):
    # create parser
    parser = Parser()
    print "\n%s" % meta.licenseNotice
    print art.splashLogo
    print art.splashText
    print "\n%s" % starterHelp
    while not p.gameOver:
        cmdstr = raw_input(">> ")
        cmd = parser.parseCmd(cmdstr)
        if cmd is not None:
            cmd.command( p )


#====================
# start game definition
# create player
plyr = Player("Bob")

# start game
playGame(plyr)
