/////////////////////////////// Librairie de fonctions pour liaison serie UART /////////////////////////////////////////////

// Variables pour les fonctions UART //

volatile int j=0; // Entier utilise pour les boucles
volatile char str[15]; // Chaine de caracteres utilisees pour la transmission de donnees

// Fonctions UART //

// Fonction d'ecriture d'un caractere par UART
void UART_send_char(char c)
{
    while(!TXSTA.TRMT); // Attente de la fin de transmission precedente
    TXREG = c; // Envoie du caractere
}

// Fonction d'ecriture d'une chaine de caracteres par UART
void UART_send_string(const char *d)
{
     while(*d!='\0'){
         UART_send_char(*d);
         d++;
         }
}

// Fonction d'ecriture d'un entier converti en chaine de caracteres par UART
void UART_send_int(int d)
{
    IntToStrWithZeros(d, str);

    for(j=0;str[j]!='\0';j++)
    {
        while(!TXSTA.TRMT);
        TXREG = str[j];
    }
}

// Fonction d'ecriture d'un entier long converti en chaine de caracteres par UART
void UART_send_long_int(int d)
{
    LongIntToStrWithZeros(d, str);

    for(j=0;str[j]!='\0';j++)
    {
        while(!TXSTA.TRMT);
        TXREG = str[j];
    }
}

// Fonction de lecture de donnees (inutilise)
char UART_read_char() {
    // Attendre que le caractere soit reçu
    while(!PIR1.RCIF);

    // Retourner le caractere reçu
    return RCREG;
}