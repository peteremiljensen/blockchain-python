#!/usr/bin/env python3

import datetime
import time
import sys
from cmd import Cmd

from blockchain.node import *
from blockchain.common import *

#                   _
#                  (_)
#   _ __ ___   __ _ _ _ __
#  | '_ ` _ \ / _` | | '_ \
#  | | | | | | (_| | | | | |
#  |_| |_| |_|\__,_|_|_| |_|
#
#

class Prompt(Cmd):
    PRINTS = ['loaf_pool', 'blockchain']

    def __init__(self):
        super().__init__()
        self._node = Node(port)
        self._node.start()

    def do_connect(self, args):
        l = args.split()
        if len(l) != 1:
            print(fail("invalid number of arguments"))
            return
        try:
            ip = l[0]
            self._node.connect_node(ip)
        except:
            print(fail("error connecting to node"))
            raise

    def do_mine(self, args):
        l = args.split()
        if len(l) != 0:
            print (fail("mine doesnt take any arguments"))
            return
        try:
            block = self._node.mine()
            if block is None:
                print(fail("failed to mine and add block"))
            else:
                self._node.broadcast_block(block)
        except:
            print(fail("error trying to mine"))
            raise

    def do_loaf(self, args):
        l = args.split()
        if len(l) != 1:
            print(fail("invalid number of arguments"))
            return
        try:
            loaf = Loaf({"string": l[0]})
            if self._node.add_loaf(loaf):
                self._node.broadcast_loaf(loaf)
            else:
                print(fail("failed to add loaf to loaf pool"))
        except:
            print(fail("error creating and broadcasting loaf"))
            raise

    def do_loafbomb(self, args):
        l = args.split()
        if len(l) != 2:
            print(fail("invalid number of arguments"))
            return
        try:
            for i in range(int(l[1])):
                loaf = Loaf({"string": l[0]+str(i)})
                self._node.broadcast_loaf(loaf)
        except:
            print(fail("error creating and broadcasting loaf"))
            raise

    def do_print(self, args):
        l = args.split()
        if len(l) != 1:
            print(fail("invalid number of arguments"))
            return
        try:
            if l[0] == self.PRINTS[0]:
                for loaf in list(self._node._loaf_pool.values()):
                    print(loaf.json())
            elif l[0] == self.PRINTS[1]:
                print(self._node._chain.json())
            else:
                print(fail(l[0] + " doesn't exist"))

        except:
            print(fail("error printing"))
            raise

    def complete_print(self, text, line, begidx, endidx):
        if not text:
            completions = self.PRINTS[:]
        else:
            completions = [f for f in self.PRINTS
                            if f.startswith(text)]
        return completions

    def do_EOF(self, line):
        self.do_quit(line)

    def do_quit(self, args):
        print(info("Quitting"))
        raise SystemExit

    def do_q(self, args):
        self.do_quit(args)

    def emptyline(self):
        return

if __name__ == '__main__':
    if len(sys.argv) == 1:
        port = 9000
    elif len(sys.argv) == 2:
        port = sys.argv[1]
    else:
        print(fail("you must supply 0 or 1 argument"))
        sys.exit()

    prompt = Prompt()
    prompt.prompt = '3==D~ '
    try:
        prompt.cmdloop(info('Starting node on port ' + str(port) + "..."))
    except KeyboardInterrupt:
        prompt.do_quit(None)
    except SystemExit:
        pass
    except:
        print(fail("fatal error"))
        raise
