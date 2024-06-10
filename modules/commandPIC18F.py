from modules.terminalUART import *

def readState(terminal):
    terminal.send_data('A')
    