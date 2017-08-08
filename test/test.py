#!/bin/python3.5

# @DEVI-if you wanna pipe the output, run with python -u. buffered output
# screws up the output

# call it the regression testing file
import sys
import os
from test_LEB128 import test_signed_LEB128
from test_LEB128 import test_unsigned_LEB128
from abc import ABCMeta, abstractmethod
sys.path.append('../')
from utils import Colors
from argparser import PythonInterpreter

total_test_cnt = int()
expected_pass_cnt = int()
expected_fail_cnt = int()

success = Colors.green + "SUCCESS: " + Colors.ENDC
fail = Colors.red + "FAIL: " + Colors.ENDC


class Void_Spwner():
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def Legacy(self):
        pass

    @abstractmethod
    def GetName(self):
        return(str())

    def Spwn(self):
        pid = os.fork()

        # I don't have a bellybutton
        if pid == 0:
            self.Legacy()
            sys.exit()
        elif pid > 0:
            cpid, status = os.waitpid(pid, 0)
            if status == 0:
                print(success + ': ' + self.GetName())
            else:
                print(fail + ': ' + self.GetName())
        else:
            # basically we couldnt fork a child
            print(fail + 'return code:' + pid)
            raise Exception("could not fork child")


def ObjectList():
    obj_list = []
    cwd = os.getcwd()
    for file in os.listdir(cwd + "/testsuite"):
        if file.endswith(".wasm"):
            obj_list.append(cwd + "/testsuite/" + file)

    return(obj_list)


class LEB128EncodeTest(Void_Spwner):
    def Legacy(self):
        test_unsigned_LEB128()
        test_signed_LEB128()

    def GetName(self):
        return('leb128encodetest')


def main():
    return_list = []
    # LEB128 tests
    leb128encodetest = LEB128EncodeTest()
    leb128encodetest.Spwn()
    # parser test on the WASM testsuite
    obj_list = ObjectList()
    for testfile in obj_list:
        pid = os.fork()
        # I dont have a bellybutton
        if pid == 0:
            # @DEVI-FIXME- the dbg option in argparser is not working yet
            # if you want to pipe this, run with python -u
            sys.stdout = open('/dev/null', 'w')
            sys.stderr = open('/dev/null', 'w')

            interpreter = PythonInterpreter()
            module = interpreter.parse(testfile)
            # interpreter.dump_sections(module)
            sys.exit()
        # the parent process
        elif pid > 0:
            cpid, status = os.waitpid(pid, 0)
            return_list.append(status)
            # @DEVI-FIXME- if you pipe it its broken
            if status == 0:
                print(success + testfile)
            else:
                print(fail + testfile)
        else:
            # basically we couldnt fork a child
            print(fail + 'return code:' + pid)
            raise Exception("could not fork child")


if __name__ == '__main__':
    main()
