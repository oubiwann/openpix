from zope.interface import Interface


class IMode(Interface):
    """
    An object representing an execution mode, with associated attributes.
    """


class IUserMode(Interface):
    """
    User EXEC mode marker class.
    """


class IPrivMode(Interface):
    """
    Privileged EXEC mode marker class.
    """


class IConfigMode(Interface):
    """
    Configuration EXEC mode marker class.
    """


class IParser(Interface):
    """
    Grammar parser marker class.
    """


class IGrammarFactory(Interface):
    """
    Mostly used as a marker class, this interface defines the methods needed in
    order to be a GrammarFactory.
    """
    def getGrammar():
        """
        Return a pyparsing Grammar for use in parsing shell commands.
        """


class ICommand(Interface):
    """

    """


class IUserCommand(ICommand):
    """

    """


class IPriveCommand(ICommand):
    """

    """


class IConfigCommand(ICommand):
    """

    """


