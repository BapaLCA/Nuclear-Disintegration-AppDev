/////////////////////////////// Librairie de traitement de commandes /////////////////////////////////////////////
// Cette librairie est utilisée pour traiter l'envoie/la reception de commandes via UART
// pour communiquer avec l'application Python

// Fonction d'envoie de donnees UART reservee a la fonction d'interruption
void UART_send_data(char c)
{
    while(!TXSTA.TRMT); // Attente de la fin de transmission precedente
    TXREG = c; // Envoie du caractere
}

// Commande de lancement des mesures
void start_measures(void)
{
    UART_send_data('m'); // On envoie une commande indiquant l'etat "Measuring" a l'app
    UART_send_data(0x0D); // Saut de ligne
    UART_send_data(0x0A);
    cpt=0;           // On initialise le compteur
    init_cpt_data(); // Et on initialise le tableau de donnees avant lancement
    flagProcess = 1;    // Met a jour le flag de sortie de boucle
    INTCON.RBIE=1; // Active les interruptions sur PORTB en dernier
}

// Commande d'arret des mesures
void stop_measures(void)
{
    INTCON.RBIE=0; // Desactive les interruptions sur PORTB
    flagProcess = 0;    // Met a jour le flag de sortie de boucle
    UART_send_data('i'); // On envoie une commande indiquant l'etat "Idle" a l'app
    UART_send_data(0x0D); // Saut de ligne
    UART_send_data(0x0A);
}

// Commande pour envoyer l'etat actuel du PIC18F4550 (utilisé lors du lancement de l'application
void send_state(char state)
{
    if(state==1)
    {
        UART_send_data('m');
    }
    else
    {
        UART_send_data('i');
    }
}