////////////////////////// Statistique de comptage - Desintegrations nucléaires /////////////////////////////////////////////

// Configuration du projet //

/*
- PIC18F4550
- 48 MHz MCU
- Prescaler Divide by 2
- HS oscillator, PLL enabled
*/

// Librairies a inclure dans le programme //

/*
-ADC
-Conversions
-C_String
-UART
*/

// Librairies personelles //

#include "lib/UART_functions.h"
#include "lib/7seg_functions.h"
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

// Variables globales //

volatile int mode=0; // Defini le mode de mesure / 0 : Erlang / 1 : Poisson
volatile int k=1; // Nombre d'impulsions a mesurer avant l'arret du compteur (Minimum 1)
volatile int exitloop = 0; //Pour sortir de la boucle principale
volatile unsigned int prevrc0 = 1; // etat precedent de RC0 pour detection de front
volatile unsigned int prevrc1 = 1; // etat precedent de RC1 pour detection de front
volatile unsigned int prevrc2 = 0; // etat precedent de RC2 pour detection de front
volatile int flagWrite = 0; // Pour demander l'ecriture des donnees enregistrees
volatile char singlechar; // Caractère utilisé pour detecter l'arrivée d'une commande recue par UART
volatile int received_k_factor=1;

////////////////////////////////// Fonction d'Interruption //////////////////////////////////////////

void interrupt(void) {
    // Active ou desactive le comptage lors de l'arrivee d'une impulsion sur RB7
    // Procede egalement a la sauvegarde et l'envoie des donnees par UART
    // Cette fonction d'interruption doit rester reservee a RB7, aucune autre pin ne doit etre utilisee
    
    if(PIR1.RCIF==1){ // Reception de données pour controler le PIC
        char received_data = RCREG; // Lire les données reçues
        PIR1.RCIF = 0; // Réinitialiser le drapeau d'interruption de réception
        if (received_k_factor) {
            if (received_data >= '0' && received_data <= '9') {
                // Conversion du caractère en entier
                k = received_data - '0';
            }
            received_k_factor = 0; // Réinitialiser après traitement
        } else {
            switch(received_data) {
                case 'k':
                    received_k_factor = 1; // On informe le PIC que le prochain caractere sera le facteur k
                    break;
                case 'g':  // Commande GO pour lancer les mesures
                    flagProcess = 1;
                    UART_send_data('m'); // On envoie une commande indiquant l'etat "Measuring" a l'app
                    UART_send_data(0x0D); // Saut de ligne
                    UART_send_data(0x0A);
                    cpt=0;           // On initialise le compteur
                    init_cpt_data(); // Et on initialise le tableau de donnees avant lancement
                    flagProcess = 1;    // Met a jour le flag de sortie de boucle
                    INTCON.RBIE=1; // Active les interruptions sur PORTB en dernier
                    break;
                case 's':  // Commande STOP pour arreter les mesures
                    flagProcess = 0;
                    INTCON.RBIE=0; // Desactive les interruptions sur PORTB
                    flagProcess = 0;    // Met a jour le flag de sortie de boucle
                    UART_send_data('i'); // On envoie une commande indiquant l'etat "Idle" a l'app
                    UART_send_data(0x0D); // Saut de ligne
                    UART_send_data(0x0A);
                    break;
                case 'e':  // Commande ERLANG pour selectionner le mode de mesure Erlang
                    mode = 1;
                    break;
                case 'p':  // Commande POISSON pour selectionner le mode de mesure Poisson
                    mode = 0;
                    break;
                case '?': // Commande pour envoyer l'etat actuel du PIC18F4550
                    send_state(flagProcess);
                default:
                    // Aucune correspondance, on ignore la/les données reçues
                    break;
            }
        }
    }
    else{
        if(mode==0){ // Erlang
            if(prevrb7==0){
                cpt = 0;      // Initialisation du compteur
                cptk = 0;     // Initialisation du compteur d'impulsion
                flagStart = 1;// Lancement du compteur
                prevrb7 = 1;  // Sauvegarde de l'etat precedent de RB7
                }
            else{
                cptk++;
                if(cptk==k){ // Verification du nombre d'impulsion mesurees
                    flagStart = 0;      // Arret du compteur
                    prevrb7 = 0;        // Sauvegarde de l'etat precedent du compteur
                    cpt_data[cpt]++;    // Sauvegarde de la donnee dans le canal correspondant
                    }
                }
                if(cpt_data[cpt]==4){  // Lorsqu'une cellule du tableau de donnee atteint sa valeur maximale, on envoie les donnees sur le PC
                    INTCON &= 0b00110111; // Desactive les interruptions
                    flagWrite = 1; // On active le flag d'ecriture des donnees
                    }
            }

        if(mode==1){ //Poisson
                Counting(); // Comptage du nombre d'impulsion sur cpt lors de la detection d'une impulsion
            }


        while(PORTB.B7==1); // On attend que l'impulsion se termine pour sortir de l'interruption (necessaire lors de test par appui sur bouton)
        INTCON.RBIF = 0; // Reinitialise le flag d'interruption RBIF
        }
}


////////////////////////////////// Fonction Principale //////////////////////////////////////////

void main() {
     // Initialisation
    PORTS_Init();  // On initialise les differents PORTs
    ADC_Init(); // On initialise le convertisseur ADC
    ADCON0 = 0;
    PORTE.B1 = 0;
    PORTE.B2 = 0;
    PORTE.B0 = 0;
    PORTB.B1 = 0;
    // J3 et J4 jumpers doivent etre places sur la position USB
    // SW1 doit activer le switch RC7 pour RX et SW2 doit activer le switch RC6 pour TX
    UART1_Init(9600); // Configuration de l'UART a une vitesse en Bauds donnee

    delay_ms(1000); // Attente de la stabilisation de l'UART
    init_cpt_data();// Initilisation du tableau de donnees
    Interrupt_Init(); // Configuration des registres d'interruption
    INTCON.RBIE=0; // Mais on conserve les interruptions desactivees sur PORTB pour le demarrage

    // Boucle principale
    while (exitloop==0){
            PORTE.B1 = 1;  // LED1 : A l'arret (Idle)
            PORTE.B2 = 0;
            PORTE.B0=mode; // LED0 : Indique le mode de fonctionnement (Erlang ou Poisson)
            //k=1+ADC_Read(10)/10;      // Conversion de la valeur analogique entre 1 et 9, a re-regler plus tard
            displayIntSingleDigit(k); // Affichage du k sur le premier digit 7 segments


            // Selection du mode (0 : Erlang, 1 : Poisson)
            if(PORTC.B2==1){
                if(prevrc2==1){
                    prevrc2=0;
                    mode=0;
                    }
                else{
                    prevrc2=1;
                    mode=1;
                    }
                while(PORTC.B2);
                }

            // Boucle de mesure, activee/desactivee lors de l'appui sur le bouton RC1 //
            while(flagProcess==1){
                PORTE.B1=0;
                PORTE.B0=mode; // Affichage du mode de mesure
                PORTE.B2=1; // LED2 : En cours d'execution
                // Detection de front montant sur RC0
                if(mode==0){ // Erlang
                    if(PORTC.B0==1){
                      if(prevrc0==0){
                          Counting(); // Incrementation du compteur
                          prevrc0=1;
                          }
                      }
                      else{
                          prevrc0=0;  // Sauvegarde du dernier etat de RC0
                          }
                }

                if(mode==1){ // Poisson
                    flagStart=1;
                    if(PORTC.B0==1){
                          cpt_data[cpt]++; // Enregistrement sur le canau correspondant au nb d'impulsion mesurees
                          cpt=0;          // Reset du compteur
                      while(PORTC.B0); // On attend que le niveau haut d'horloge se termine
                      }

                      if(cpt_data[cpt]==4){  // Lorsqu'une cellule du tableau de donnee atteint sa valeur maximale, on envoie les donnees sur le PC
                          INTCON &= 0b00110111; // Desactive toutes les interruptions pour l'ecriture
                          flagWrite = 1; // On active le flag d'ecriture des donnees
                          }
                }

                // Partie commune aux deux modes //

                if(flagWrite==1){ // Pour l'envoie des donnees
                    send_data(); // Envoie les donnees vers le terminal
                    init_cpt_data();
                    flagWrite=0;
                    INTCON |= 0b11001000; // Reactive toutes les interruptions
                    }

                while(PORTC.B1==1){ // Met en pause les mesures lors de l'appui sur le bouton RC1
                        if(prevrc1==0){
                            prevrc1=1;          // Sauvegarde du dernier etat de RC1
                            INTCON.RBIE=0; // Desactive les interruptions sur PORTB
                            flagProcess = 0;    // Met a jour le flag de sortie de boucle
                            UART_Write('i'); // On envoie une commande indiquant l'etat "Idle" a l'app
                            UART_Write(0x0D); // Saut de ligne
                            UART_Write(0x0A);
                        }
                    }
                }


            // Met en route les mesures lors de l'appui sur le bouton RC1 //
            while(PORTC.B1==1){
                if(prevrc1==1){
                        UART_Write('m'); // On envoie une commande indiquant l'etat "Measuring" a l'app
                        UART_Write(0x0D); // Saut de ligne
                        UART_Write(0x0A);
                        cpt=0;           // On initialise le compteur
                        init_cpt_data(); // Et on initialise le tableau de donnees avant lancement
                        flagProcess = 1;    // Met a jour le flag de sortie de boucle
                        INTCON.RBIE=1; // Active les interruptions sur PORTB en dernier
                        prevrc1=0;          // Sauvegarde du dernier etat de RC1
                    }
                }
        }
}