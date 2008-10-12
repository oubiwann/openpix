import inspect

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


class BaseCommand(object):
    """
    Base class for commands.
    """
    skipHelp = True
    summary = ""
    usage = ""
    syntax = ""

    def __init__(self, tokens):
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


class QuitCommand(BaseCommand):
    """
    Disable privileged commands, end configuration mode, or logout
    """
    summary = "Exit from the EXEC"
    usage = "%s"
    skipHelp = False

    def _doCommand(self, player):
        print "\nLogoff\n"
        player.gameOver = True


class ExitCommand(QuitCommand):
    def __init__(self, *args, **kwds):
        self.__doc__ = QuitCommand.__doc__


class LogoffCommand(QuitCommand):
    def __init__(self, *args, **kwds):
        self.__doc__ = QuitCommand.__doc__


class BaseHelpCommand(BaseCommand):
    """

    """
    skipHelp = True
    helpTextMethod = ""


class ShortHelpCommand(BaseHelpCommand):
    """

    """
    skipHelp = True
    helpTextMethod = "getSummary"

    def _doCommand(self, player):
        from openpix import command
        klassData = inspect.getmembers(command, inspect.isclass)
        sorted(klassData)
        print
        for klassName, klass in klassData:
            if klass.skipHelp:
                continue
            obj = klass()
            print "  %-10s     %s" % (obj.getCommandName(), obj.getSummary())
        print


class HelpCommand(BaseCommand):
    """
    Interactive help for commands
    """
    summary = "Interactive help for commands"
    usage = "%s [command]"
    skipHelp = False
    helpTextMethod = "getDesc"

    def _doCommand(self, player):
        print "not implemented"


class EnableCommand(BaseCommand):
    """
    Turn on privileged commands
    """
    summary = "Turn on privileged commands"
    usage = "%s [<priv_level>]"
    skipHelp = False

    def _doCommand(self, player):
        print "not implemented"


class LoginCommand(BaseCommand):
    """
    Log in as a particular user
    """
    summary = "Log in as a particular user"
    usage = "%s"
    skipHelp = False

    def _doCommand(self, player):
        print "not implemented"


class PingCommand(BaseCommand):
    """
    Test connectivity from specified interface to an IP address
    """
    summary = "Send echo messages"
    usage = """
        %s [if_name] <host> [data <pattern>] [repeat <count>] [size <bytes>]
                    [timeout <seconds>] [validate]
        """
    syntax = """
        [if_name]   The interface name, as specified by the 'nameif' command,
                    by which <host> is accessible.  If not supplied, then <host>
                    is resolved to an IP address and then the routing table
                    is consulted to determine the destination interface.

        <host>      IPv4 address, IPv6 address or name of host to ping.

        <pattern>   16 bit data pattern in hex.

        <count>     Repeat count.

        <bytes>     Datagram size in bytes.

        <seconds>   Timeout in seconds.

        validate    Validate reply data.
        """
    skipHelp = False

    def _doCommand(self, player):
        print "not implemented"


class ShowCommand(BaseCommand):
    """
    Display specific information to the console
    """
    summary = "Show running system information"
    usage = "%s [command [subcommand]]"
    skipHelp = False

    def _doCommand(self, player):
        print "not implemented"


class TracerouteCommand(BaseCommand):
    """
    Print the route packets take to a network host
    """
    summary = "Trace route to destination"
    usage = """
        %s <destination> [source <src_address|src_intf>]
                    [numeric] [timeout <time>] [ttl <min-ttl> <max-ttl>]
                    [probe <probes>] [port <port-value>] [use-icmp]
        """
    syntax = """
        c_intf      Interface through which the destination is accessible
        numeric     Do not resolve addresses to hostnames
        time        The time in seconds to wait for a response to a probe
        min-ttl     Minimum time-to-live value used in probe packets
        max-ttl     Maximum time-to-live value used in probe packets
        probes      The number of probes to send for each TTL value
        port-value  Base UDP destination port used in probes
        use-icmp    Use ICMP probes instead of UDP probes
        """
    skipHelp = False

    def _doCommand(self, player):
        print "not implemented"


