from zope.interface import implements

from openpix import interfaces
from openpix.command import base
from openpix.command import subcommand
from openpix.util import oneOfCaseless


class NullCommand(base.BaseCommand):
    """

    """
    summary = ""
    usage = ""
    skipHelp = True
    legalVerbs = oneOfCaseless(" ")

    def doCommand(self, user):
        pass


class ShowCommand(base.BaseCommand):
    """
    Display specific information to the console
    """
    implements(interfaces.IUserCommand, interfaces.IPrivCommand)
    summary = "Show running system information"
    usage = "%s [command [subcommand]]"
    skipHelp = False
    legalVerbs = oneOfCaseless("show sho sh")
    subcommands = subcommand.ShowSubCommands()

    def doCommand(self, user):
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

    def printShortHelp(self):
        """

        """
        super(ShowCommand, self).printShortHelp()
        self.printSubCommands()


class ShortHelpCommand(base.BaseHelpCommand):
    """

    """
    implements(interfaces.IUserCommand, interfaces.IPrivCommand)
    skipHelp = True
    helpTextMethod = "getSummary"
    legalVerbs = oneOfCaseless("?")

    def doCommand(self, user):
        print
        for klassName, klass in sorted(base.getCommandClasses(self.mode)):
            if klass.skipHelp:
                continue
            obj = klass(self.parser)
            print "  %-10s     %s" % (obj.getCommandName(), obj.getSummary())
        print


class HelpCommand(base.BaseCommand):
    """
    Interactive help for commands
    """
    implements(interfaces.IUserCommand, interfaces.IPrivCommand)
    summary = "Interactive help for commands"
    usage = "%s [command]"
    skipHelp = False
    helpTextMethod = "getDesc"
    legalVerbs = oneOfCaseless("help h")

    def doCommand(self, user):
        helpSubCommand = self.tokens.subCommand
        print self.shell.getCommand(helpSubCommand).getHelp()


class PingCommand(base.BaseCommand):
    """
    Test connectivity from specified interface to an IP address
    """
    implements(interfaces.IUserCommand, interfaces.IPrivCommand)
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

    def doCommand(self, user):
        print "not implemented"


class TracerouteCommand(base.BaseCommand):
    """
    Print the route packets take to a network host
    """
    implements(interfaces.IUserCommand, interfaces.IPrivCommand)
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

    def doCommand(self, user):
        print "not implemented"
