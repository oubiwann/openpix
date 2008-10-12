class BaseCommand(object):
    """
    Base class for commands.
    """
    skipHelp = True
    summary = ""
    usage = ""
    syntax = ""

    def __init__(self, tokens=[]):
        self.tokens = tokens

    def __call__(self, user):
        self._doCommand(user)

    def _doCommand(self, user):
        """
        This method provides the action for each command.

        This needs to be overridden by subclasses.
        """
        raise NotImplementedError

    def getCommandName(self):
        """

        """
        return self.__class__.__name__.replace('Command', '').lower()

    def getDesc(self):
        """

        """
        return self.__doc__.strip()

    def getUsage(self):
        """

        """
        return self.usage.strip() % self.getCommandName()

    def printShortHelp(self):
        """

        """
        print "\n  %s\n\n  %s\n" % (self.getSummary(), self.getUsage())

    def getSyntax(self):
        """

        """
        return self.syntax

    def getSummary(self):
        """

        """
        return self.summary

    def getHelp(self):
        """

        """
        syntax = self.getSyntax()
        if syntax:
            syntax = "SYNTAX:\n%s" % syntax
        return "\nUSAGE:\n%s\nDESCRIPTION:\n%s\n" % (
            self.getUsage(), self.getDesc(), syntax)
