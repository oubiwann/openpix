import readline

from openpix import art
from openpix import meta
from openpix.util import bannerDivider, defaultPrompt, starterHelp
from openpix.grammar.parser import Parser


class User(object):
    """

    """
    def __init__(self, name):
        self.name = name
        self.gameOver = False
        self.inv = []


def printBanner():
    """
    This function provides some beauty in the otherwise dull and boring life of
    a shell's life.
    """
    print bannerDivider
    print art.splashLogo
    print art.splashText
    print bannerDivider
    print "\n%s" % meta.licenseNotice
    print bannerDivider
    print "\n%s" % starterHelp


def processResults(parseResults, user):
    """
    This function performs simple decision-making tasks based on the obtained
    results.
    """
    if parseResults is not None:
        cmd = parseResults.command
        # XXX
        # not sure if this switching logic should happen here or in the
        # command classes during __init__ and __call__
        if cmd.tokens.shortHelp:
            cmd.printShortHelp()
        else:
            cmd(user)


def setUpShell(user):
    """
    This function does everything necessary to start a shell and parse commands
    as they are entered.
    """
    printBanner()
    # create parser
    parser = Parser()
    while not user.gameOver:
        commandString = raw_input(defaultPrompt)
        processResults(parser.parseCommand(commandString), user)

