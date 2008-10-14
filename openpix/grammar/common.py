from zope.interface import implements

from pyparsing import Optional

from openpix import interfaces
# XXX the following imported code needs to be moved from usermode into either
# commands.base or commands.common and then imported from there
from openpix.commands import usermode


shortHelpOption = Optional(
    usermode.ShortHelpCommand.legalVerbs).setResultsName('shortHelp')


class Grammar(object):
    implements(interfaces.IGrammarFactory)

    def __init__(self, parser, mode):
        self.parser = parser
        self.mode = mode
