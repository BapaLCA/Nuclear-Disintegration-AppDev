////////////////////////// Counting Statistics - Nuclear Disintegration - ULB /////////////////////////////////////////////

// Project Configuration //

/*
- PIC18F4550
- 48 MHz MCU
- Prescaler Divide by 2
- HS oscillator, PLL enabled
*/

// Libraries to include in the code //

/*
-ADC
-Conversions
-C_String
-UART
*/

// Personal Libraries //

#include "lib/UART_functions.h"
#include "lib/counting_functions.h"
#include "lib/init_functions.h"
#include "lib/command_manager.h"

// Guide //

/*
    Le programme commence en position Idle :
-Choisissez le mode de mesure Erlang/Poisson avec le bouton RC2 : La LED RE0 indique le mode (eteinte : Erlang, allumee : Poisson)
-Pour le mode Erlang : Utilisez le potentiometre P2 pour regler le k (nb d'impulsion a relever), sa valeur s'affiche sur l'afficheur 7 segments
-Demarrez les mesures avec le bouton RC1 : La LED RE2 s'allumera pour indiquer la position Run du programme
-Vous pouvez mettre en pause les mesures a tout moment avec RC1, la LED RE2 s'eteindra pour indiquer la position Idle du programme

*/

// Global variables //

volatile int mode=0; // Defines the measure mode / 0 : Erlang / 1 : Poisson / 2 : Pool
volatile int k=1; // Amount of pulses before stopping the counter after a first pulse was measured (Minimum 1)
volatile int exitloop = 0; // Flag to exit the main loop
volatile unsigned int prevrc0 = 1; // Previous state of RC0 for rising edge detection
volatile unsigned int prevrc1 = 1; // Previous state of RC1 for rising edge detection
volatile unsigned int prevrc2 = 0; // Previous state of RC2 for rising edge detection
volatile int flagWrite = 0; // Flag to send data to UART
volatile char singlechar; // Char used to detect received command from UART
volatile int received_k_factor=1; // Flag

////////////////////////////////// Interrupt Function //////////////////////////////////////////

void interrupt(void) {
    // Enables or disables Counting when a pulse is detected on RB7
    // Manages the saving and sending of data using UART
    
    if(PIR1.RCIF==1){ // Receiving of data for PIC control
        char received_data = RCREG; // Reads the received data
        PIR1.RCIF = 0; // Resets the interrupt flag
        if (received_k_factor) { // If the previous char received was a 'k', we check the value sent to change the k factor
            if (received_data >= '0' && received_data <= '9') {
                // Converts the char into an int
                k = received_data - '0';
            }
            received_k_factor = 0; // Resets Flag after processing
        } else {
            switch(received_data) {
                case 'k':
                    received_k_factor = 1; // Sets a flag to inform the PIC that the next char to process is the value of the k factor
                    break;
                case 'g':  // GO command to launch measures
                    UART_send_data('m'); // Sends a char 'm' meaning the state "Measuring" to Application
                    UART_send_data(0x0D); // Sends a line breaker
                    UART_send_data(0x0A);
                    cpt=0;           // Counter init
                    init_cpt_data(); // Data tab init
                    flagProcess = 1;    // Updates the process Flag for the process loop
                    INTCON.RBIE=1; // Enables interruptions on PORTB
                    break;
                case 's':  // STOP command to stop measures
                    flagProcess = 0;
                    INTCON.RBIE=0; // Disables interruptions on PORTB
                    flagProcess = 0;    // Updates process flag to exit the processing loop
                    UART_send_data('i'); // Sends a char 'i' meaning the state "Idle" to Application
                    UART_send_data(0x0D); // Line breaker
                    UART_send_data(0x0A);
                    break;
                case 'e':  // ERLANG command to select the measure mode Erlang
                    mode = 0;
                    break;
                case 'p':  // POISSON command to select the measure mode Poisson
                    mode = 1;
                    break;
                case 'o': // POOL command to select the measure mode Pool
                    mode = 2;
                    break;
                case '?': // QUESTION command to ask PIC to send its current state
                    send_state(flagProcess);
                    UART_send_data(0x0D); // Line breaker
                    UART_send_data(0x0A);
                    break;
                case 'u': // Update POOL mode command to end the current measure and send the data measured
                    flagWrite = 1; // Enable flag Write to send to UART the current measured data
                    break;
                case 'r': // Reset POOL mode command to reset the number of measures done
                    measureCount=0;
                    break;
                default:
                    // No char matching, ignoring data received
                    break;
            }
        }
    }
    else{
        if(mode==0){ // Erlang
            if(prevrb7==0){
                cpt = 0;      // Counter Init
                cptk = 0;     // Pulse Counter Init
                flagStart = 1;// Launches the counter
                prevrb7 = 1;  // Saves the previous state of RB7
                }
            else{
                cptk++;
                if(cptk==k){ // Check the number of pulses measured
                    flagStart = 0;      // Stops counter
                    prevrb7 = 0;        // Saves the previous state of RB7
                    cpt_data[cpt]++;    // Saves the data in the corresponding index
                    }
                }
                if(cpt_data[cpt]==255){  // When one of the tab cell reaches 255 (8 bits limit), it enables the writing loop and sends all measured data
                    INTCON &= 0b00110111; // Disable interruptions
                    flagWrite = 1; // Enables writing Flag
                    }
            }

        if(mode==1){ //Poisson
                Counting(); // Counts the number of pulses on cpt variable on pulse detection
            }

        if(mode==2){ // Pool
            cpt++; // Counts the number of pulses on cpt variable on pulse detection, no call for Counting needed as we have no counting limit on this mode
            }


        while(PORTB.B7==1); // Waiting for pulse to be over before quitting interrupt function
        INTCON.RBIF = 0; // Resets the interrupt flag RBIF
        }
}


////////////////////////////////// Main Function //////////////////////////////////////////

void main() {
     // Initialisation
    PORTS_Init();  // PORTs init
    // ADC_Init(); Unused
    ADCON0 = 0;
    PORTE.B1 = 0;
    PORTE.B2 = 0;
    PORTE.B0 = 0;
    PORTB.B1 = 0;
    // RC6 and RC7 must be set as USB-UART (should be the case by default on Ready for PIC)
    UART1_Init(9600); // UART speed configuration set to 9600 Bauds

    delay_ms(1000); // Delay to wait for UART to stabilize
    init_cpt_data();// Data tab init
    Interrupt_Init(); // Sets up the interrupt registers
    INTCON.RBIE=0; // PORTB interrupt shall remain disabled on launch

    // Main Loop
    while (exitloop==0){
            // Mode selection (0 : Erlang, 1 : Poisson, 2 : Pool)

            // Measuring Loop, enabled/disabled by Application through GO/STOP commands
            while(flagProcess==1){

                if(mode==0){ // Erlang
                    if(PORTC.B0==1){
                      if(prevrc0==0){ // Rising edge
                          Counting(); // Increases the counter when a clock rising edge is detected
                          prevrc0=1; // Saves the previous state of RC0
                          }
                      }
                      else{ // Falling edge
                          prevrc0=0;  // Saves the previous state of RC0
                          }
                }
                
                if(mode==1){ // Poisson Mode
                    flagStart=1;
                    if(PORTC.B0==1){
                          cpt_data[cpt]++; // Saves on Index corresponding to the amount of pulses measured
                          cpt=0;          // Counter reset
                      while(PORTC.B0); // Waiting for the high level of the clock to end
                      }

                      if(cpt_data[cpt]==255){  // When a cell's value reaches 255 (8 bits limit) the data is sent through UART
                          INTCON &= 0b00110111; // Disables interruptions for writing
                          flagWrite = 1; // Enables writing flag
                          }
                }
                
                if(mode==2){ // Piscine
                    flagStart=1; // No processing on secondary input here
                    }


                // Common part of all modes //

                if(flagWrite==1){ // Data sending function
                    if(mode<=1){ // Sends data in a tab form for modes Erlang/Poisson
                        send_data(); // Sends data towards UART Terminal
                        init_cpt_data();
                        }
                    if(mode==2){ // Sends data as a single line for Pool mode
                        send_data_pool(); // Sends data towards UART Terminal
                        cpt=0; // Resets counter only, cpt_data is not used in this mode
                        }
                    flagWrite=0;
                    INTCON |= 0b11001000; // Enables back all interruptions
                    }
                }
        }
}