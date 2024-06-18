#line 1 "C:/Users/romai/Documents/18F4550/Nuclear-Disintegration AppDev/picProject/main.c"
#line 1 "c:/users/romai/documents/18f4550/nuclear-disintegration appdev/picproject/lib/uart_functions.h"




volatile int j=0;
volatile char str[15];




void UART_send_char(char c)
{
 while(!TXSTA.TRMT);
 TXREG = c;
}


void UART_send_string(const char *d)
{
 while(*d!='\0'){
 UART_send_char(*d);
 d++;
 }
}


void UART_send_int(int d)
{
 IntToStrWithZeros(d, str);

 for(j=0;str[j]!='\0';j++)
 {
 while(!TXSTA.TRMT);
 TXREG = str[j];
 }
}


void UART_send_long_int(int d)
{
 LongIntToStrWithZeros(d, str);

 for(j=0;str[j]!='\0';j++)
 {
 while(!TXSTA.TRMT);
 TXREG = str[j];
 }
}


char UART_read_char() {

 while(!PIR1.RCIF);


 return RCREG;
}
#line 1 "c:/users/romai/documents/18f4550/nuclear-disintegration appdev/picproject/lib/7seg_functions.h"




const unsigned char DIGITS[] = {
 0x3F,
 0x06,
 0x5B,
 0x4F,
 0x66,
 0x6D,
 0x7D,
 0x07,
 0x7F,
 0x6F
};

const unsigned char LETTERS[] = {
 0x77,
 0x3E,
 0x39,
 0x5E,
 0x79,
 0x71,
 0x3D,
 0x76,
 0x06,
 0x1E,
 0x38,
 0x54,
 0x5C,
 0x73,
 0x67,
 0x50,
 0x6D,
 0x78,
 0x1C,
 0x6E
};



void display7segInt(unsigned int value){

 PORTA = 0x01; PORTD = DIGITS[(value%10)]; delay_ms(3);
 PORTA = 0x02; PORTD = DIGITS[((value%100)/10)]; delay_ms(3);
 PORTA = 0x04; PORTD = DIGITS[((value%1000)/100)]; delay_ms(3);
 PORTA = 0x08; PORTD = DIGITS[(value/1000)]; delay_ms(3);
}

void display7segChar(unsigned int value, unsigned int digit){

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
 display7segChar(15, 0x04);
 display7segChar(18, 0x02);
 display7segChar(11, 0x01);
}

void displayEnd(){
 display7segChar(4, 0x04); delay_ms(3);
 display7segChar(11, 0x02); delay_ms(3);
 display7segChar(3, 0x01); delay_ms(3);
}
#line 1 "c:/users/romai/documents/18f4550/nuclear-disintegration appdev/picproject/lib/counting_functions.h"




volatile const int MAX = 1024;
volatile unsigned long int i=0;
volatile unsigned char cpt_data[MAX];
volatile int cptk=0;
volatile int flagStart = 0;
volatile int flagProcess = 0;
volatile int cpt = 0;
volatile unsigned int prevrb7 = 1;



void Counting() {

 if(flagStart==1){
 cpt++;
 }
 if(cpt > MAX){
 cpt = 0;
 flagStart = 0;
 prevrb7 = 0;
 }
}


void send_data() {
 UART_Write('w');
 UART_Write(0x0D);
 UART_Write(0x0A);
 for(i=0;i<MAX;i++) {
 if(cpt_data[i]!=0){
 UART_send_long_int(i);
 UART_Write(';');
 UART_send_int(cpt_data[i]);
 UART_Write(0x0D);
 UART_Write(0x0A);
 }
 }
 UART_Write('d');
 UART_Write(0x0D);
 UART_Write(0x0A);
 UART_Write('m');
 UART_Write(0x0D);
 UART_Write(0x0A);
}


void init_cpt_data(){
 for(i=0;i<MAX;i++) {
 cpt_data[i]=0;
 }
}
#line 1 "c:/users/romai/documents/18f4550/nuclear-disintegration appdev/picproject/lib/init_functions.h"

void PORTS_Init()
{
 TRISD = 0x00;
 TRISA = 0x00;
 TRISB = 0xFD;
 TRISC = 0xFF;
 TRISE.B0 = 0;
 TRISE.B1 = 0;
 TRISE.B2 = 0;
 TRISE.B3 = 0;
}


void Interrupt_Init()
{
 INTCON2.INTEDG0 = 1;
 INTCON |= 0b11000000;
 INTCON |= 0b00001000;
 INTCON.RBIF = 0;
 PIE1.RCIE = 1;
}
#line 1 "c:/users/romai/documents/18f4550/nuclear-disintegration appdev/picproject/lib/command_manager.h"





void UART_send_data(char c)
{
 while(!TXSTA.TRMT);
 TXREG = c;
}


void start_measures(void)
{
 UART_send_data('m');
 UART_send_data(0x0D);
 UART_send_data(0x0A);
 cpt=0;
 init_cpt_data();
 flagProcess = 1;
 INTCON.RBIE=1;
}


void stop_measures(void)
{
 INTCON.RBIE=0;
 flagProcess = 0;
 UART_send_data('i');
 UART_send_data(0x0D);
 UART_send_data(0x0A);
}


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
#line 42 "C:/Users/romai/Documents/18F4550/Nuclear-Disintegration AppDev/picProject/main.c"
volatile int mode=0;
volatile int k=1;
volatile int exitloop = 0;
volatile unsigned int prevrc0 = 1;
volatile unsigned int prevrc1 = 1;
volatile unsigned int prevrc2 = 0;
volatile int flagWrite = 0;
volatile char singlechar;
volatile int received_k_factor=1;



void interrupt(void) {




 if(PIR1.RCIF==1){
 char received_data = RCREG;
 PIR1.RCIF = 0;
 if (received_k_factor) {
 if (received_data >= '0' && received_data <= '9') {

 k = received_data - '0';
 }
 received_k_factor = 0;
 } else {
 switch(received_data) {
 case 'k':
 received_k_factor = 1;
 break;
 case 'g':
 UART_send_data('m');
 UART_send_data(0x0D);
 UART_send_data(0x0A);
 cpt=0;
 init_cpt_data();
 flagProcess = 1;
 INTCON.RBIE=1;
 break;
 case 's':
 flagProcess = 0;
 INTCON.RBIE=0;
 flagProcess = 0;
 UART_send_data('i');
 UART_send_data(0x0D);
 UART_send_data(0x0A);
 break;
 case 'e':
 mode = 0;
 break;
 case 'p':
 mode = 1;
 break;
 case '?':
 send_state(flagProcess);
 default:

 break;
 }
 }
 }
 else{
 if(mode==0){
 if(prevrb7==0){
 cpt = 0;
 cptk = 0;
 flagStart = 1;
 prevrb7 = 1;
 }
 else{
 cptk++;
 if(cptk==k){
 flagStart = 0;
 prevrb7 = 0;
 cpt_data[cpt]++;
 }
 }
 if(cpt_data[cpt]==4){
 INTCON &= 0b00110111;
 flagWrite = 1;
 }
 }

 if(mode==1){
 Counting();
 }


 while(PORTB.B7==1);
 INTCON.RBIF = 0;
 }
}




void main() {

 PORTS_Init();
 ADC_Init();
 ADCON0 = 0;
 PORTE.B1 = 0;
 PORTE.B2 = 0;
 PORTE.B0 = 0;
 PORTB.B1 = 0;


 UART1_Init(9600);

 delay_ms(1000);
 init_cpt_data();
 Interrupt_Init();
 INTCON.RBIE=0;


 while (exitloop==0){
 PORTE.B1 = 1;
 PORTE.B2 = 0;
 PORTE.B0=mode;

 displayIntSingleDigit(k);



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


 while(flagProcess==1){
 PORTE.B1=0;
 PORTE.B0=mode;
 PORTE.B2=1;

 if(mode==0){
 if(PORTC.B0==1){
 if(prevrc0==0){
 Counting();
 prevrc0=1;
 }
 }
 else{
 prevrc0=0;
 }
 }

 if(mode==1){
 flagStart=1;
 if(PORTC.B0==1){
 cpt_data[cpt]++;
 cpt=0;
 while(PORTC.B0);
 }

 if(cpt_data[cpt]==4){
 INTCON &= 0b00110111;
 flagWrite = 1;
 }
 }



 if(flagWrite==1){
 send_data();
 init_cpt_data();
 flagWrite=0;
 INTCON |= 0b11001000;
 }

 while(PORTC.B1==1){
 if(prevrc1==0){
 prevrc1=1;
 INTCON.RBIE=0;
 flagProcess = 0;
 UART_Write('i');
 UART_Write(0x0D);
 UART_Write(0x0A);
 }
 }
 }



 while(PORTC.B1==1){
 if(prevrc1==1){
 UART_Write('m');
 UART_Write(0x0D);
 UART_Write(0x0A);
 cpt=0;
 init_cpt_data();
 flagProcess = 1;
 INTCON.RBIE=1;
 prevrc1=0;
 }
 }
 }
}
