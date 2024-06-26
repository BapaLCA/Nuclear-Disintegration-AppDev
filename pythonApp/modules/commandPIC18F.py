from modules.terminalUART import *

# Input Commands
# "01" : 
# "02" : Write  <2b> Register <4b> Value
# "03" : Read   <2b> Register <4b> Unusued
# Output Commands


def setFactorK(terminal, user_input):
    terminal.send_data('k') # On envoie le caractere 'k' pour indiquer au PIC qu'il s'agit d'un changement de valeur de k
    terminal.send_data(user_input) # On envoie la valeur de k au PIC


