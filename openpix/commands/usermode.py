import inspect


from openpix import util
from openpix.commands import base


class EnableCommand(base.BaseCommand):
    """
    Turn on privileged commands
    """
    summary = "Turn on privileged commands"
    usage = "%s [<priv_level>]"
    skipHelp = False

    def _doCommand(self, player):
        print "not implemented"


class LoginCommand(base.BaseCommand):
    """
    Log in as a particular user
    """
    summary = "Log in as a particular user"
    usage = "%s"
    skipHelp = False

    def _doCommand(self, player):
        print "not implemented"


class QuitCommand(base.BaseCommand):
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


class ShowCommand(base.BaseCommand):
    """
    Display specific information to the console
    """
    summary = "Show running system information"
    usage = "%s [command [subcommand]]"
    skipHelp = False

    def _doCommand(self, player):
        show = self.tokens.show
        if show.startswith('lic'):
            util.printLicenseNotice()
        elif show.startswith('ver'):
            util.printVersion()
        elif show.startswith('spl'):
            util.printSplashArt()
        elif show.startswith('ban'):
            util.printBanner()
        elif show.startswith('cop'):
            util.printCopyright()
        elif show.startswith('his'):
            util.printHistory()

class BaseHelpCommand(base.BaseCommand):
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
        from openpix.commands import usermode
        klassData = inspect.getmembers(usermode, inspect.isclass)
        sorted(klassData)
        print
        for klassName, klass in klassData:
            if klass.skipHelp:
                continue
            obj = klass()
            print "  %-10s     %s" % (obj.getCommandName(), obj.getSummary())
        print


class HelpCommand(base.BaseCommand):
    """
    Interactive help for commands
    """
    summary = "Interactive help for commands"
    usage = "%s [command]"
    skipHelp = False
    helpTextMethod = "getDesc"

    def _doCommand(self, player):
        print "not implemented"


class PingCommand(base.BaseCommand):
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


class TracerouteCommand(base.BaseCommand):
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


