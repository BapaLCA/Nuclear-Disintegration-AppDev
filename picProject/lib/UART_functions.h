/////////////////////////////// Library for UART functions /////////////////////////////////////////////

// Global variables for UART functions //

volatile int j=0; // Int used for loops
volatile char str[15]; // String used for data transmission

// UART functions //

// Char writing function
void UART_send_char(char c)
{
    while(!TXSTA.TRMT); // Waiting for previous transmission to be done
    TXREG = c; // Sends input char
}

// String writing function
void UART_send_string(const char *d)
{
     while(*d!='\0'){
         UART_send_char(*d); // Reuses char writing function for each char of the input string
         d++;
         }
}

// Int writing function (converted as string)
void UART_send_int(int d)
{
    IntToStrWithZeros(d, str); // Converts Int to String

    for(j=0;str[j]!='\0';j++)
    {
        while(!TXSTA.TRMT); // Waits for previous transmission to be done
        TXREG = str[j];
    }
}

// Long int writing function (converted as string)
void UART_send_long_int(int d)
{
    LongIntToStrWithZeros(d, str); // Converts Long Int to String

    for(j=0;str[j]!='\0';j++)
    {
        while(!TXSTA.TRMT); // Waits for previous transmission to be done
        TXREG = str[j];
    }
}

// Reading data function (Unusued, as reception is done through interrupt function)
char UART_read_char() {
    // Waits for char to be received
    while(!PIR1.RCIF);

    // Returns received char
    return RCREG;
}