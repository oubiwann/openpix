import readline

from openpix import util
from openpix.grammar.parser import Parser


maxHistoryLines = 500
readline.set_history_length(maxHistoryLines)


class User(object):
    """

    """
    def __init__(self, name):
        self.name = name
        self.gameOver = False
        self.isEnabled = False


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
    util.printBanner()
    # create parser
    parser = Parser()
    while not user.gameOver:
        commandString = raw_input(util.defaultPrompt)
        processResults(parser.parseCommand(commandString), user)

