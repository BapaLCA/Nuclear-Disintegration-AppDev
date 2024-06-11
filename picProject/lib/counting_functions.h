/////////////////////////////// Librairie de fonctions pour le Compteur d'impulsion /////////////////////////////////////////////

// Variables globales utilisees //

volatile const int MAX = 1024;
volatile unsigned long int i=0; // Entier utilise pour les boucles
volatile unsigned char cpt_data[MAX]; // Tableau de stockage des donnees a relever, limite a des valeurs max de 256
volatile int cptk=0;             // Compteur d'impulsion
volatile int flagStart = 0; //Flag pour l'activation du comptage
volatile int flagProcess = 0; //Flag pour le demarrage/arret des mesures
volatile int cpt = 0; //Variable de comtpage
volatile unsigned int prevrb7 = 1; // etat precedent de RB4 pour detection de front

// Fonctions //

void Counting() {
    // Cette fonction lance un compteur classique jusqu'a 1024
    if(flagStart==1){
        cpt++;
        }
    if(cpt > MAX){ // On ignore le comptage si le temps depasse 1024 periodes d'horloge entre deux impulsions
        cpt = 0;
        flagStart = 0;
        prevrb7 = 0;
        }
}

// Fonction qui envoie les donnees stockees
void send_data() {
    UART_Write('w'); // On envoie une commande indiquant l'etat "Writing data" a l'app
    UART_Write(0x0D);
    UART_Write(0x0A);
    for(i=0;i<MAX;i++) {
        UART_send_long_int(i);
        UART_Write(';');
        UART_send_int(cpt_data[i]);
        UART_Write(0x0D);
        UART_Write(0x0A);
        }
    UART_Write('m'); // On envoie une commande indiquant l'etat "Measuring" a l'app
    UART_Write(0x0D);
    UART_Write(0x0A);
}

// Initialise toutes les cellules du compteur a 0
void init_cpt_data(){
    for(i=0;i<MAX;i++) {
        cpt_data[i]=0;
        }
}