#!/usr/bin/env python
# -*- coding: utf-8 -*-
# bitmask_cli
# Copyright (C) 2015, 2016 LEAP
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Bitmask Command Line interface: zmq client.
"""
import sys

from colorama import Fore
from twisted.internet import reactor, defer

from leap.bitmask.cli.eip import Eip
from leap.bitmask.cli.keys import Keys
from leap.bitmask.cli.mail import Mail
from leap.bitmask.cli.command import Command
from leap.bitmask.cli.user import User


class BitmaskCLI(Command):
    usage = '''bitmask_cli <command> [<args>]

Controls the Bitmask application.

SERVICE COMMANDS:

   user       Handles Bitmask accounts
   mail       Bitmask Encrypted Mail
   eip        Encrypted Internet Proxy
   keys       Bitmask Keymanager

GENERAL COMMANDS:

   version    prints version number and exit
   launch     launch the Bitmask backend daemon
   shutdown   shutdown Bitmask backend daemon
   status     displays general status about the running Bitmask services
   stats      show some debug info about bitmask-core
   help       show this help message

'''
    epilog = ("Use 'bitmask_cli <command> help' to learn more "
              "about each command.")
    commands = ['shutdown', 'status', 'stats']

    def user(self, raw_args):
        user = User()
        return user.execute(raw_args)

    def mail(self, raw_args):
        mail = Mail()
        return mail.execute(raw_args)

    def eip(self, raw_args):
        eip = Eip()
        return eip.execute(raw_args)

    def keys(self, raw_args):
        keys = Keys()
        return keys.execute(raw_args)

    # Single commands

    def launch(self, raw_args):
        # XXX careful! Should see if the process in PID is running,
        # avoid launching again.
        import commands
        commands.getoutput('bitmaskd')
        return defer.succeed(None)

    def version(self, raw_args):
        print Fore.GREEN + 'bitmask_cli: 0.0.1' + Fore.RESET
        self.data = ['version']
        return self._send()


def execute():
    cli = BitmaskCLI()
    d = cli.execute(sys.argv[1:])
    d.addCallback(lambda _: reactor.stop())


def main():
    reactor.callWhenRunning(reactor.callLater, 0, execute)
    reactor.run()

if __name__ == "__main__":
    main()
