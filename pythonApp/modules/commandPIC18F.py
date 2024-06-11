from modules.terminalUART import *

# Input Commands
# "01" : 
# "02" : Write  <2b> Register <4b> Value
# "03" : Read   <2b> Register <4b> Unusued
# Output Commands


def readState(terminal):
    data_to_send = 0x03010000
    terminal.send_data(data_to_send)

