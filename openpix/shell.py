import socket
import readline

from openpix import art
from openpix import meta
from openpix.grammar import Parser


starterHelp = "Type help or '?' for a list of available commands."

dividerSegment = "_" * 34
bannerDivider = "\n %s .:|:. %s\n" % (dividerSegment, dividerSegment)

defaultPrompt = "openpix@%s> " % socket.gethostname()
rootPrompt = "openpix@%s# " % socket.gethostname()

class User(object):
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


def setUpShell(user):
    # create parser
    parser = Parser()
    print bannerDivider
    print art.splashLogo
    print art.splashText
    print bannerDivider
    print "\n%s" % meta.licenseNotice
    print bannerDivider
    print "\n%s" % starterHelp
    while not user.gameOver:
        cmdstr = raw_input(defaultPrompt)
        cmd = parser.parseCommand(cmdstr)
        if cmd is not None:
            # XXX
            # not sure if this switching logic should happen here or in the
            # command classes during __init__ and __call__
            if cmd.command.tokens.shortHelp:
                cmd.command.printShortHelp()
            else:
                cmd.command(user)

