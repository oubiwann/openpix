from zope import interface
from zope import component

# interfaces
class IUserMode(interface.Interface):
    pass

class IPrivMode(interface.Interface):
    pass

class IParser(interface.Interface):
    pass

class IGrammarFactory(interface.Interface):
    def getGrammar():
        "return the grammar"

# modes
class UserMode(object):
    interface.implements(IUserMode)
    name = "user"

class PrivMode(object):
    interface.implements(IPrivMode)
    name = "priv"

# parser
class Parser(object):
    interface.implements(IParser)
    def parseCommand(self, cmd, mode):
        grammar = component.queryMultiAdapter((self, mode), IGrammarFactory).getGrammar
        print cmd, grammar()

# grammars
class Grammar(object):

    def __init__(self, parser, mode):
        self.parser = parser
        self.mode = mode

class UserGrammar(Grammar):
    component.adapts(IParser, IUserMode)
    interface.implements(IGrammarFactory)

    def getGrammar(self):
        return "user grammar"

component.provideAdapter(UserGrammar)

class PrivGrammar(Grammar):
    component.adapts(IParser, IPrivMode)
    interface.implements(IGrammarFactory)

    def getGrammar(self):
        return "priv grammar"

component.provideAdapter(PrivGrammar)


user = UserMode()
priv = PrivMode()

parser = Parser()
parser.parseCommand("enable", user)
parser.parseCommand("cofigure", priv)


