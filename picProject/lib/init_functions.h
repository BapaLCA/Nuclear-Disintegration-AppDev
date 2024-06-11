// Fonction d'initialisation des differents ports utilises
void PORTS_Init()
{
    TRISD = 0x00; // Configuration de PORTD en sortie pour les segments de l'afficheur 7 segments
    TRISA = 0x00; // Configuration de PORTA en sortie
    TRISB = 0xFD; // Configuration de PORTB en entree
    TRISC = 0xFF; // Configuration de PORTC en entree
    TRISE.B0 = 0; // Utilisees pour visualiser certaines actions
    TRISE.B1 = 0;
    TRISE.B2 = 0;
    TRISE.B3 = 0;
}

// Fonction d'initialisation des interruptions sur les PORTB 4 a 7 (Le port RB4 ne fonctionne pas, a verifier)
void Interrupt_Init()
{
    INTCON2.INTEDG0 = 1;
    INTCON |= 0b11000000; // Activer les interruptions globales et peripheriques (GIE et PEIE)
    INTCON |= 0b00001000; // Activer les interruptions sur changement d'etat pour PORTB (RBIE)
    INTCON.RBIF = 0; // Flag d'interruption sur les PORTB 4 a 7
}