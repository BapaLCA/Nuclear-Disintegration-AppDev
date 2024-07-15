/////////////////////////////// Library for command processing /////////////////////////////////////////////
// This library is used to process sending/receiving of command using UART to communicate with Python Application

// Function for sending UART data - For Interrupt thread only
void UART_send_data(char c)
{
    while(!TXSTA.TRMT); // Waiting for enidng of previous transmission
    TXREG = c; // Sending char
}

// Command for launching measures
void start_measures(void)
{
    UART_send_data('m'); // Sends a char 'm' meaning the state "Measuring" to Application
    UART_send_data(0x0D); // Line breaker
    UART_send_data(0x0A);
    cpt=0;           // Counter init
    init_cpt_data(); // Data tab init before measure launched
    flagProcess = 1;    // Update the process flag to enter process loop
    INTCON.RBIE=1; // Enables interruptions on PORTB
}

// Command for stopping measures
void stop_measures(void)
{
    INTCON.RBIE=0; // Disables interrutpions on PORTB
    flagProcess = 0;    // Updates flag process to leave process loop
    UART_send_data('i'); // Sends a char 'i' meaning the state "Idle" to Application
    UART_send_data(0x0D); // Line Breaker
    UART_send_data(0x0A);
}

// Command to send the current state of the PIC to Application (Used on application startup)
void send_state(char state)
{
    if(state==1) // Uses process flag to know the current state of PIC
    {
        UART_send_data('m');
    }
    else
    {
        UART_send_data('i');
    }
}