from zope import component
from zope.interface import implements

from pyparsing import ParseException, LineEnd

from openpix import mode
from openpix import interfaces
from openpix.components import registry

class AppParseException(ParseException):
    pass


class Parser(object):
    """

    """
    implements(interfaces.IParser)

    def __init__(self, shell):
        self.shell = shell
        self._grammar_cache = {}

    def getShell(self):
        """

        """
        return self.shell

    def getGrammar(self, mode):
        """
        A grammar caching mechanism that uses the factory only when neccessary.
        """
        grammar = self._grammar_cache.get(mode)
        if not grammar:
            grammar = registry.queryMultiAdapter(
                (self, mode), interfaces.IGrammarFactory).getGrammar()
            self._grammar_cache[mode] = grammar
        return grammar

    def parseCommand(self, command, mode):
        """

        """
        # switch grammars, based on the mode
        try:
            result = self.getGrammar(mode).parseString(command)
            return result
        except AppParseException, e:
            print e.msg
        except ParseException, e:
            # XXX
            print e
            print "ERROR: Invalid input detected."

