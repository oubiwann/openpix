import inspect

from pyparsing import MatchFirst

from openpix import util
from openpix.commands import base
from openpix.util import oneOfCaseless


class EnableCommand(base.BaseCommand):
    """
    Turn on privileged commands
    """
    summary = "Turn on privileged commands"
    usage = "%s [<priv_level>]"
    skipHelp = False
    legalVerbs = oneOfCaseless("enable enab en")

    def _doCommand(self, user):
        # XXX add support for changing the password
        pass

class LoginCommand(base.BaseCommand):
    """
    Log in as a particular user
    """
    summary = "Log in as a particular user"
    usage = "%s"
    skipHelp = False
    legalVerbs = oneOfCaseless("login logi")

    def _doCommand(self, user):
        print "not implemented"


class QuitCommand(base.BaseCommand):
    """
    Disable privileged commands, end configuration mode, or logout
    """
    summary = "Exit from the EXEC"
    usage = "%s"
    skipHelp = False
    legalVerbs = oneOfCaseless("quit q exit ex logout logou logo")

    def _doCommand(self, user):
        print "\nLogoff\n"
        user.logout = True


class ExitCommand(QuitCommand):
    def __init__(self, *args, **kwds):
        self.__doc__ = QuitCommand.__doc__


class LogoffCommand(QuitCommand):
    def __init__(self, *args, **kwds):
        self.__doc__ = QuitCommand.__doc__


class ShowSubCommands(object):
    """
    The subcommands for the show command.

    PIX:
        checksum  Display configuration information cryptochecksum
        curpriv   Display current privilege level
        flash:    Display information about flash: file system
        history   Display the session command history
        rip       IP RIP show commands
        sla       Service Level Agreement (SLA)
        track     Tracking information
        version   Display system software version
    """
    version = oneOfCaseless("version ver")
    license = oneOfCaseless("license lisence lis lic li")
    splash = oneOfCaseless("splash splas spla spl")
    banner = oneOfCaseless("banner ban")
    copyright = oneOfCaseless("copyright copyr copy cop")
    history = oneOfCaseless("history hist his")
    backend = oneOfCaseless("backend back")
    system = oneOfCaseless("system syst sys")

    def getLegalVerbs(self):
        """
        Get all the legal verbs for all the subcommands.
        """
        def isVerb(klass):
            """
            A member checker that ensures we get verb instances as created by
            oneOfCaseless.
            """
            if isinstance(klass, MatchFirst):
                return True
            return False
        klassData = inspect.getmembers(self, isVerb)
        return [klass for  klassName, klass in klassData]


class ShowCommand(base.BaseCommand):
    """
    Display specific information to the console
    """
    summary = "Show running system information"
    usage = "%s [command [subcommand]]"
    skipHelp = False
    legalVerbs = oneOfCaseless("show sho sh")
    subcommands = ShowSubCommands()

    def _doCommand(self, user):
        show = self.tokens.show
        if not show:
            self.printSubCommands()
        elif show in self.subcommands.license.exprs:
            util.printLicenseNotice()
        elif show in self.subcommands.version.exprs:
            util.printVersion()
        elif show in self.subcommands.splash.exprs:
            util.printSplashArt()
        elif show in self.subcommands.banner.exprs:
            util.printBanner()
        elif show in self.subcommands.copyright.exprs:
            util.printCopyright()
        elif show in self.subcommands.history.exprs:
            util.printHistory()
        elif show in self.subcommands.backend.exprs:
            print "\n%s\n" % self.parser.shell.getBackend()
        elif show in self.subcommands.system.exprs:
            print "\n%s\n" % self.parser.shell.getSystem().longName

    def printSubCommands(self):
        """

        """
        print
        print "  Sub-commands:"
        for verb in self.subcommands.getLegalVerbs():
            print "    %s" % verb.exprs[0].returnString
        print 

    def printShortHelp(self):
        """

        """
        super(ShowCommand, self).printShortHelp()
        self.printSubCommands()


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
    legalVerbs = oneOfCaseless("?")

    def _doCommand(self, user):
        from openpix.commands import usermode
        def isCommandClass(klass):
            """
            A check that filters only top-level command classes.
            """
            if inspect.isclass(klass) and issubclass(klass, base.BaseCommand):
                return True
            return False
        klassData = inspect.getmembers(usermode, isCommandClass)
        sorted(klassData)
        print
        for klassName, klass in klassData:
            if klass.skipHelp:
                continue
            obj = klass(self.parser)
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
    legalVerbs = oneOfCaseless("help h")

    def _doCommand(self, user):
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
    legalVerbs = oneOfCaseless("ping pi")

    def _doCommand(self, user):
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
    legalVerbs = oneOfCaseless("traceroute tracert trace trac tra tr")

    def _doCommand(self, user):
        print "not implemented"


