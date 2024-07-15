/////////////////////////////// Libraries used for Pulse Counter /////////////////////////////////////////////

// Global variables //

volatile const int MAX = 1024; // Limit of the data tab (RAM is limited to 2048 Bytes)
volatile unsigned long int i=0; // Int used for loops
volatile unsigned char cpt_data[MAX]; // Int tab for storing measured data limited to values of 255 per cell
volatile int cptk=0;             // Pulse counter for Erlang Mode
volatile int flagStart = 0; // Flag to start counting
volatile int flagProcess = 0; // Flag used to start/stop measures
volatile int cpt = 0; // Counter variable
volatile unsigned int prevrb7 = 1; // Previous state of RB7 for rising edge detection
volatile int measureCount = 0; // Variable used to count the number of measures on Pool Mode

// Functions //

void Counting() {
    // This function increases by one a counter until 1024
    if(flagStart==1){
        cpt++;
        }
    if(cpt > MAX){ // The iteration is ignored if 1024 clock periods elapse (Limit set by the 1024 cells of the data tab)
        cpt = 0;
        flagStart = 0;
        prevrb7 = 0;
        }
}

// This function sends all stored data
void send_data() {
    UART_Write('w'); // Sends a char 'w' meaning the state "Writing" to Application
    UART_Write(0x0D); // Line Breaker
    UART_Write(0x0A);
    for(i=0;i<MAX;i++) {
        if(cpt_data[i]!=0){
            UART_send_long_int(i); // Index
            UART_Write(';'); // Separator of values
            UART_send_int(cpt_data[i]); // Value at Index
            UART_Write(0x0D); // Line Breaker
            UART_Write(0x0A);
            }
        }
    UART_Write('d'); // Sends a char 'd' meaning the state "Done Writing" to Application
    UART_Write(0x0D); // Line breaker
    UART_Write(0x0A);
    UART_Write('m'); // Sends a char 'm' meaning the state "Measuring" to Application
    UART_Write(0x0D); // Line breaker
    UART_Write(0x0A);
}

void send_data_pool() {
    UART_Write('w'); // Sends a char 'w' meaning the state "Writing" to Application
    UART_Write(0x0D); // Line breaker
    UART_Write(0x0A);
    UART_send_long_int(measureCount); // Sends the number of measures done as an Index
    UART_Write(';'); // Separator of values
    UART_send_int(cpt); // Sends the value of the counter
    UART_Write(0x0D); // Line breaker
    UART_Write(0x0A);
    UART_Write('d'); // Sends a char 'd' meaning the state "Done Writing" to Application
    UART_Write(0x0D); // Line Breaker
    UART_Write(0x0A);
    UART_Write('m'); // Sends a char 'm' meaning the state "Measuring" to Application
    UART_Write(0x0D); // Line breaker
    UART_Write(0x0A);
    measureCount++; // Increases by one the number of measures done
}

// Init all cells of the data tab to 0
void init_cpt_data(){
    for(i=0;i<MAX;i++) {
        cpt_data[i]=0;
        }
}