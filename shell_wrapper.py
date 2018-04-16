#!/usr/bin/python2
# @file shell_wrapper.py
# @brief The tool allow to wrap awful command line tools to provide command history feature. Initialy it is targeted on 'jdb' debugger.
#        Now, such tools are supported: jdb, gdb, bash, sh
# @author Bohdan Kovalenko
# @version v0.1
# @date 2018-04-16

# @version  v0.1

import cmd
import re
import select
import sys
import time
import threading

from subprocess import CalledProcessError, Popen, PIPE

timeout = 0.2
timeout_init = 2

class Shell(cmd.Cmd):
    def __init__(self, shellname, **kwargs):
        cmd.Cmd.__init__(self)
        name = shellname if type(shellname) != type(list()) else shellname[0]
        self.process = Popen(shellname, stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=0)
        if "color" in kwargs:
            if kwargs["color"] == True:
                self.cl_red = "\033[91m"
                self.cl_error = "\033[91m"
                self.cl_prompt = "\033[94m"
                self.cl_default = "\033[0m"
        self.prompt = "%s%s$ %s"%(self.cl_prompt, name, self.cl_default)
        self.r1 = threading.Thread(target=self.reader)
        self.r1.daemon = True
        self.r1.start()
        self.r2 = threading.Thread(target=self.reader_error)
        self.r2.daemon = True
        self.r2.start()
        time.sleep(timeout_init)
        self.process.stdin.write('\n\n')

    def reader(self):
        while True:
            print self.process.stdout.readline().strip()
    def reader_error(self):
        while True:
            sys.stdout.write("%s%s%s\n"%(self.cl_error, self.process.stderr.readline().strip(), self.cl_default))

    def onecmd(self,line):
        if re.match("[^a-zA-Z]*exit[^a-zA-Z]*", line) != None or re.match("[^a-zA-Z]*quit[^a-zA-Z]*", line) != None:
            self.process.terminate()
            return True
        else:
            self.process.stdin.write(line+'\n')
            self.process.stdin.flush()
            time.sleep(timeout)

def run_wrapper(shellname, params = None):
    Shell(shellname, color=True).cmdloop()

if __name__ == "__main__":
    if sys.argv[0] == "shell_wrapper.py":
        if not "-cmd" in sys.argv:
            print "The tool is used to wrap unusefull interactive command line interfaces (like as jdb)"
            print "Supported shells: jdb"
            print "Usage:"
            print "    python shell_wrapper.py -cmd <shell name> -opt <options>"
            print "    ln -s shell_wrapper.py <shell name>.py; python <shell name> <options>"
            print "Examples:"
            print "    python shell_wrapper.py -cmd jdb"
            print "    ln -s shell_wrapper.py jdb.py; python jdb.py"
        else:
            cmdname = sys.argv[sys.argv.index("-cmd")+1]
            if "-opt" in sys.argv:
                options = [i for i in sys.argv[sys.argv.index("-opt")+1].split(' ') if i.strip() != '']
            else:
                options = []
            run_wrapper([cmdname] + options)
    else:
        if sys.argv[0][-3:] != ".py":
            print "Error: extension must be '*.py'"
            exit(-1)
        run_wrapper([sys.argv[0][:-3]] + sys.argv[1:])

