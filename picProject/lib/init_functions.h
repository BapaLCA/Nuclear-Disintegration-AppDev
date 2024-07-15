/////////////////////////////// Library for init functions /////////////////////////////////////////////
// This library is used to initialize PORTs and Interrupt registers

// Init function for PORTs used
void PORTS_Init()
{
    // TRISD = 0x00; // Unused
    TRISA = 0x00; // PORTA set as output
    TRISB = 0xFD; // PORTB set as input
    TRISC = 0xFF; // PORTC set up as input
    TRISE.B0 = 0; // Debugging pins
    TRISE.B1 = 0;
    TRISE.B2 = 0;
    TRISE.B3 = 0;
}

// Init function for interrupt registers for PORTB and UART
void Interrupt_Init()
{
    INTCON2.INTEDG0 = 1;
    INTCON |= 0b11000000; // Enables all interruptions (GIE et PEIE)
    INTCON |= 0b00001000; // Enables interruptions on PORTB (RBIE)
    INTCON.RBIF = 0; // Init interrupt flag for RB4 to RB7
    PIE1.RCIE = 1; // Enable interruptions on UART reception
}