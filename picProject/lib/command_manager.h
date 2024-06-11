/////////////////////////////// Librairie de traitement de commandes /////////////////////////////////////////////
// Cette librairie est utilisée pour traiter l'envoie/la reception de commandes via UART
// pour communiquer avec l'application Python

#include "lib/UART_functions.h"

void read_command_type(int value)
{
    switch (value){
        case 0x01: // Sends current PIC18F4550 state
            command_send_state();
            break;
        case 0x02: // Read
            command_read(value);
            break;
        case 0x03: // Write
            command_write(value);
            break;
        default: // In case none of the case match
            command_error("No command type matching");
    }
}

void command_send_state()
{
    UART_send_int(State);
}

void command_read(int value)
{

}

void command_write(int value)
{

}