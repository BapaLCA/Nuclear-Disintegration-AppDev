/////////////////////////////// Librairie de fonctions pour Afficheur 7 segments /////////////////////////////////////////////

// Tableau des codes pour l'affichage des chiffres sur un afficheur 7 segments //

const unsigned char DIGITS[] = {
    0x3F, // 0
    0x06, // 1
    0x5B, // 2
    0x4F, // 3
    0x66, // 4
    0x6D, // 5
    0x7D, // 6
    0x07, // 7
    0x7F, // 8
    0x6F  // 9
};

const unsigned char LETTERS[] = {
    0x77, //A - 0
    0x3E, //b - 1
    0x39, //C - 2
    0x5E, //d - 3
    0x79, //E - 4
    0x71, //F - 5
    0x3D, //G - 6
    0x76, //H - 7
    0x06, //I - 8
    0x1E, //J - 9
    0x38, //L - 10
    0x54, //n - 11
    0x5C, //o - 12
    0x73, //p - 13
    0x67, //q - 14
    0x50, //r - 15
    0x6D, //S - 16
    0x78, //t - 17
    0x1C, //U - 18
    0x6E  //y - 19
};

// Fonctions Afficheur 7 segments //

void display7segInt(unsigned int value){
     // Cette fonction affiche le nombre (4 chiffres max) sur l'afficheur 7 segments
     PORTA = 0x01; PORTD = DIGITS[(value%10)]; delay_ms(3);
     PORTA = 0x02; PORTD = DIGITS[((value%100)/10)]; delay_ms(3);
     PORTA = 0x04; PORTD = DIGITS[((value%1000)/100)]; delay_ms(3);
     PORTA = 0x08; PORTD = DIGITS[(value/1000)]; delay_ms(3);
}

void display7segChar(unsigned int value, unsigned int digit){
     // Cette fonction affiche une lettre sur un digit de l'afficheur 7 segments
     PORTA = digit; PORTD = LETTERS[value];
}

void displayClear(){
    PORTA = 0x01; PORTD = 0x00;
}

void displayIntSingleDigit(int nb){
    PORTA = 0x01; PORTD = DIGITS[nb];
}

void displayStop(){
    display7segChar(16, 0x08); delay_ms(3);
    display7segChar(17, 0x04); delay_ms(3);
    display7segChar(12, 0x02); delay_ms(3);
    display7segChar(13, 0x01); delay_ms(3);
}

void displayRun(){
    display7segChar(15, 0x04); //delay_ms(3);
    display7segChar(18, 0x02); //delay_ms(3);
    display7segChar(11, 0x01); //delay_ms(3);
}

void displayEnd(){
    display7segChar(4, 0x04);  delay_ms(3);
    display7segChar(11, 0x02); delay_ms(3);
    display7segChar(3, 0x01);  delay_ms(3);
}