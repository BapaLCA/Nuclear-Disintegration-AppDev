
_UART_send_char:

;uart_functions.h,11 :: 		
;uart_functions.h,13 :: 		
L_UART_send_char0:
	BTFSC       TXSTA+0, 1 
	GOTO        L_UART_send_char1
	GOTO        L_UART_send_char0
L_UART_send_char1:
;uart_functions.h,14 :: 		
	MOVF        FARG_UART_send_char_c+0, 0 
	MOVWF       TXREG+0 
;uart_functions.h,15 :: 		
L_end_UART_send_char:
	RETURN      0
; end of _UART_send_char

_UART_send_string:

;uart_functions.h,18 :: 		
;uart_functions.h,20 :: 		
L_UART_send_string2:
	MOVF        FARG_UART_send_string_d+0, 0 
	MOVWF       TBLPTRL+0 
	MOVF        FARG_UART_send_string_d+1, 0 
	MOVWF       TBLPTRH+0 
	MOVF        FARG_UART_send_string_d+2, 0 
	MOVWF       TBLPTRU+0 
	TBLRD*+
	MOVFF       TABLAT+0, R1
	MOVF        R1, 0 
	XORLW       0
	BTFSC       STATUS+0, 2 
	GOTO        L_UART_send_string3
;uart_functions.h,21 :: 		
	MOVF        FARG_UART_send_string_d+0, 0 
	MOVWF       TBLPTRL+0 
	MOVF        FARG_UART_send_string_d+1, 0 
	MOVWF       TBLPTRH+0 
	MOVF        FARG_UART_send_string_d+2, 0 
	MOVWF       TBLPTRU+0 
	TBLRD*+
	MOVFF       TABLAT+0, FARG_UART_send_char_c+0
	CALL        _UART_send_char+0, 0
;uart_functions.h,22 :: 		
	MOVLW       1
	ADDWF       FARG_UART_send_string_d+0, 1 
	MOVLW       0
	ADDWFC      FARG_UART_send_string_d+1, 1 
	ADDWFC      FARG_UART_send_string_d+2, 1 
;uart_functions.h,23 :: 		
	GOTO        L_UART_send_string2
L_UART_send_string3:
;uart_functions.h,24 :: 		
L_end_UART_send_string:
	RETURN      0
; end of _UART_send_string

_UART_send_int:

;uart_functions.h,27 :: 		
;uart_functions.h,29 :: 		
	MOVF        FARG_UART_send_int_d+0, 0 
	MOVWF       FARG_IntToStrWithZeros_input+0 
	MOVF        FARG_UART_send_int_d+1, 0 
	MOVWF       FARG_IntToStrWithZeros_input+1 
	MOVLW       _str+0
	MOVWF       FARG_IntToStrWithZeros_output+0 
	MOVLW       hi_addr(_str+0)
	MOVWF       FARG_IntToStrWithZeros_output+1 
	CALL        _IntToStrWithZeros+0, 0
;uart_functions.h,31 :: 		
	CLRF        _j+0 
	CLRF        _j+1 
L_UART_send_int4:
	MOVLW       _str+0
	ADDWF       _j+0, 0 
	MOVWF       FSR0L+0 
	MOVLW       hi_addr(_str+0)
	ADDWFC      _j+1, 0 
	MOVWF       FSR0L+1 
	MOVF        POSTINC0+0, 0 
	MOVWF       R1 
	MOVF        R1, 0 
	XORLW       0
	BTFSC       STATUS+0, 2 
	GOTO        L_UART_send_int5
;uart_functions.h,33 :: 		
L_UART_send_int7:
	BTFSC       TXSTA+0, 1 
	GOTO        L_UART_send_int8
	GOTO        L_UART_send_int7
L_UART_send_int8:
;uart_functions.h,34 :: 		
	MOVLW       _str+0
	ADDWF       _j+0, 0 
	MOVWF       FSR0L+0 
	MOVLW       hi_addr(_str+0)
	ADDWFC      _j+1, 0 
	MOVWF       FSR0L+1 
	MOVF        POSTINC0+0, 0 
	MOVWF       R0 
	MOVF        R0, 0 
	MOVWF       TXREG+0 
;uart_functions.h,31 :: 		
	MOVLW       1
	ADDWF       _j+0, 0 
	MOVWF       R0 
	MOVLW       0
	ADDWFC      _j+1, 0 
	MOVWF       R1 
	MOVF        R0, 0 
	MOVWF       _j+0 
	MOVF        R1, 0 
	MOVWF       _j+1 
;uart_functions.h,35 :: 		
	GOTO        L_UART_send_int4
L_UART_send_int5:
;uart_functions.h,36 :: 		
L_end_UART_send_int:
	RETURN      0
; end of _UART_send_int

_UART_send_long_int:

;uart_functions.h,39 :: 		
;uart_functions.h,41 :: 		
	MOVF        FARG_UART_send_long_int_d+0, 0 
	MOVWF       FARG_LongIntToStrWithZeros_input+0 
	MOVF        FARG_UART_send_long_int_d+1, 0 
	MOVWF       FARG_LongIntToStrWithZeros_input+1 
	MOVLW       0
	BTFSC       FARG_UART_send_long_int_d+1, 7 
	MOVLW       255
	MOVWF       FARG_LongIntToStrWithZeros_input+2 
	MOVWF       FARG_LongIntToStrWithZeros_input+3 
	MOVLW       _str+0
	MOVWF       FARG_LongIntToStrWithZeros_output+0 
	MOVLW       hi_addr(_str+0)
	MOVWF       FARG_LongIntToStrWithZeros_output+1 
	CALL        _LongIntToStrWithZeros+0, 0
;uart_functions.h,43 :: 		
	CLRF        _j+0 
	CLRF        _j+1 
L_UART_send_long_int9:
	MOVLW       _str+0
	ADDWF       _j+0, 0 
	MOVWF       FSR0L+0 
	MOVLW       hi_addr(_str+0)
	ADDWFC      _j+1, 0 
	MOVWF       FSR0L+1 
	MOVF        POSTINC0+0, 0 
	MOVWF       R1 
	MOVF        R1, 0 
	XORLW       0
	BTFSC       STATUS+0, 2 
	GOTO        L_UART_send_long_int10
;uart_functions.h,45 :: 		
L_UART_send_long_int12:
	BTFSC       TXSTA+0, 1 
	GOTO        L_UART_send_long_int13
	GOTO        L_UART_send_long_int12
L_UART_send_long_int13:
;uart_functions.h,46 :: 		
	MOVLW       _str+0
	ADDWF       _j+0, 0 
	MOVWF       FSR0L+0 
	MOVLW       hi_addr(_str+0)
	ADDWFC      _j+1, 0 
	MOVWF       FSR0L+1 
	MOVF        POSTINC0+0, 0 
	MOVWF       R0 
	MOVF        R0, 0 
	MOVWF       TXREG+0 
;uart_functions.h,43 :: 		
	MOVLW       1
	ADDWF       _j+0, 0 
	MOVWF       R0 
	MOVLW       0
	ADDWFC      _j+1, 0 
	MOVWF       R1 
	MOVF        R0, 0 
	MOVWF       _j+0 
	MOVF        R1, 0 
	MOVWF       _j+1 
;uart_functions.h,47 :: 		
	GOTO        L_UART_send_long_int9
L_UART_send_long_int10:
;uart_functions.h,48 :: 		
L_end_UART_send_long_int:
	RETURN      0
; end of _UART_send_long_int

_UART_read_char:

;uart_functions.h,51 :: 		
;uart_functions.h,53 :: 		
L_UART_read_char14:
	BTFSC       PIR1+0, 5 
	GOTO        L_UART_read_char15
	GOTO        L_UART_read_char14
L_UART_read_char15:
;uart_functions.h,56 :: 		
	MOVF        RCREG+0, 0 
	MOVWF       R0 
;uart_functions.h,57 :: 		
L_end_UART_read_char:
	RETURN      0
; end of _UART_read_char

_Counting:

;counting_functions.h,17 :: 		
;counting_functions.h,19 :: 		
	MOVLW       0
	XORWF       _flagStart+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__Counting82
	MOVLW       1
	XORWF       _flagStart+0, 0 
L__Counting82:
	BTFSS       STATUS+0, 2 
	GOTO        L_Counting16
;counting_functions.h,20 :: 		
	MOVLW       1
	ADDWF       _cpt+0, 0 
	MOVWF       R0 
	MOVLW       0
	ADDWFC      _cpt+1, 0 
	MOVWF       R1 
	MOVF        R0, 0 
	MOVWF       _cpt+0 
	MOVF        R1, 0 
	MOVWF       _cpt+1 
;counting_functions.h,21 :: 		
L_Counting16:
;counting_functions.h,22 :: 		
	MOVLW       128
	XORLW       4
	MOVWF       R0 
	MOVLW       128
	XORWF       _cpt+1, 0 
	SUBWF       R0, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__Counting83
	MOVF        _cpt+0, 0 
	SUBLW       0
L__Counting83:
	BTFSC       STATUS+0, 0 
	GOTO        L_Counting17
;counting_functions.h,23 :: 		
	CLRF        _cpt+0 
	CLRF        _cpt+1 
;counting_functions.h,24 :: 		
	CLRF        _flagStart+0 
	CLRF        _flagStart+1 
;counting_functions.h,25 :: 		
	CLRF        _prevrb7+0 
	CLRF        _prevrb7+1 
;counting_functions.h,26 :: 		
L_Counting17:
;counting_functions.h,27 :: 		
L_end_Counting:
	RETURN      0
; end of _Counting

_send_data:

;counting_functions.h,30 :: 		
;counting_functions.h,31 :: 		
	MOVLW       119
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,32 :: 		
	MOVLW       13
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,33 :: 		
	MOVLW       10
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,34 :: 		
	CLRF        _i+0 
	CLRF        _i+1 
	CLRF        _i+2 
	CLRF        _i+3 
L_send_data18:
	MOVLW       0
	SUBWF       _i+3, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__send_data85
	MOVLW       0
	SUBWF       _i+2, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__send_data85
	MOVLW       4
	SUBWF       _i+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__send_data85
	MOVLW       0
	SUBWF       _i+0, 0 
L__send_data85:
	BTFSC       STATUS+0, 0 
	GOTO        L_send_data19
;counting_functions.h,35 :: 		
	MOVLW       _cpt_data+0
	ADDWF       _i+0, 0 
	MOVWF       FSR0L+0 
	MOVLW       hi_addr(_cpt_data+0)
	ADDWFC      _i+1, 0 
	MOVWF       FSR0L+1 
	MOVF        POSTINC0+0, 0 
	MOVWF       R1 
	MOVF        R1, 0 
	XORLW       0
	BTFSC       STATUS+0, 2 
	GOTO        L_send_data21
;counting_functions.h,36 :: 		
	MOVF        _i+0, 0 
	MOVWF       FARG_UART_send_long_int_d+0 
	MOVF        _i+1, 0 
	MOVWF       FARG_UART_send_long_int_d+1 
	CALL        _UART_send_long_int+0, 0
;counting_functions.h,37 :: 		
	MOVLW       59
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,38 :: 		
	MOVLW       _cpt_data+0
	ADDWF       _i+0, 0 
	MOVWF       FSR0L+0 
	MOVLW       hi_addr(_cpt_data+0)
	ADDWFC      _i+1, 0 
	MOVWF       FSR0L+1 
	MOVF        POSTINC0+0, 0 
	MOVWF       R0 
	MOVF        R0, 0 
	MOVWF       FARG_UART_send_int_d+0 
	MOVLW       0
	MOVWF       FARG_UART_send_int_d+1 
	CALL        _UART_send_int+0, 0
;counting_functions.h,39 :: 		
	MOVLW       13
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,40 :: 		
	MOVLW       10
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,41 :: 		
L_send_data21:
;counting_functions.h,34 :: 		
	MOVLW       1
	ADDWF       _i+0, 0 
	MOVWF       R0 
	MOVLW       0
	ADDWFC      _i+1, 0 
	MOVWF       R1 
	MOVLW       0
	ADDWFC      _i+2, 0 
	MOVWF       R2 
	MOVLW       0
	ADDWFC      _i+3, 0 
	MOVWF       R3 
	MOVF        R0, 0 
	MOVWF       _i+0 
	MOVF        R1, 0 
	MOVWF       _i+1 
	MOVF        R2, 0 
	MOVWF       _i+2 
	MOVF        R3, 0 
	MOVWF       _i+3 
;counting_functions.h,42 :: 		
	GOTO        L_send_data18
L_send_data19:
;counting_functions.h,43 :: 		
	MOVLW       100
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,44 :: 		
	MOVLW       13
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,45 :: 		
	MOVLW       10
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,46 :: 		
	MOVLW       109
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,47 :: 		
	MOVLW       13
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,48 :: 		
	MOVLW       10
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,49 :: 		
L_end_send_data:
	RETURN      0
; end of _send_data

_send_data_pool:

;counting_functions.h,51 :: 		
;counting_functions.h,52 :: 		
	MOVLW       119
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,53 :: 		
	MOVLW       13
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,54 :: 		
	MOVLW       10
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,55 :: 		
	MOVF        _measureCount+0, 0 
	MOVWF       FARG_UART_send_long_int_d+0 
	MOVF        _measureCount+1, 0 
	MOVWF       FARG_UART_send_long_int_d+1 
	CALL        _UART_send_long_int+0, 0
;counting_functions.h,56 :: 		
	MOVLW       59
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,57 :: 		
	MOVF        _cpt+0, 0 
	MOVWF       FARG_UART_send_int_d+0 
	MOVF        _cpt+1, 0 
	MOVWF       FARG_UART_send_int_d+1 
	CALL        _UART_send_int+0, 0
;counting_functions.h,58 :: 		
	MOVLW       13
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,59 :: 		
	MOVLW       10
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,60 :: 		
	MOVLW       100
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,61 :: 		
	MOVLW       13
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,62 :: 		
	MOVLW       10
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,63 :: 		
	MOVLW       109
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,64 :: 		
	MOVLW       13
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,65 :: 		
	MOVLW       10
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,66 :: 		
	MOVLW       1
	ADDWF       _measureCount+0, 0 
	MOVWF       R0 
	MOVLW       0
	ADDWFC      _measureCount+1, 0 
	MOVWF       R1 
	MOVF        R0, 0 
	MOVWF       _measureCount+0 
	MOVF        R1, 0 
	MOVWF       _measureCount+1 
;counting_functions.h,67 :: 		
L_end_send_data_pool:
	RETURN      0
; end of _send_data_pool

_init_cpt_data:

;counting_functions.h,70 :: 		
;counting_functions.h,71 :: 		
	CLRF        _i+0 
	CLRF        _i+1 
	CLRF        _i+2 
	CLRF        _i+3 
L_init_cpt_data22:
	MOVLW       0
	SUBWF       _i+3, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__init_cpt_data88
	MOVLW       0
	SUBWF       _i+2, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__init_cpt_data88
	MOVLW       4
	SUBWF       _i+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__init_cpt_data88
	MOVLW       0
	SUBWF       _i+0, 0 
L__init_cpt_data88:
	BTFSC       STATUS+0, 0 
	GOTO        L_init_cpt_data23
;counting_functions.h,72 :: 		
	MOVLW       _cpt_data+0
	ADDWF       _i+0, 0 
	MOVWF       FSR1L+0 
	MOVLW       hi_addr(_cpt_data+0)
	ADDWFC      _i+1, 0 
	MOVWF       FSR1L+1 
	CLRF        POSTINC1+0 
;counting_functions.h,71 :: 		
	MOVLW       1
	ADDWF       _i+0, 0 
	MOVWF       R0 
	MOVLW       0
	ADDWFC      _i+1, 0 
	MOVWF       R1 
	MOVLW       0
	ADDWFC      _i+2, 0 
	MOVWF       R2 
	MOVLW       0
	ADDWFC      _i+3, 0 
	MOVWF       R3 
	MOVF        R0, 0 
	MOVWF       _i+0 
	MOVF        R1, 0 
	MOVWF       _i+1 
	MOVF        R2, 0 
	MOVWF       _i+2 
	MOVF        R3, 0 
	MOVWF       _i+3 
;counting_functions.h,73 :: 		
	GOTO        L_init_cpt_data22
L_init_cpt_data23:
;counting_functions.h,74 :: 		
L_end_init_cpt_data:
	RETURN      0
; end of _init_cpt_data

_PORTS_Init:

;init_functions.h,5 :: 		
;init_functions.h,8 :: 		
	CLRF        TRISA+0 
;init_functions.h,9 :: 		
	MOVLW       253
	MOVWF       TRISB+0 
;init_functions.h,10 :: 		
	MOVLW       255
	MOVWF       TRISC+0 
;init_functions.h,11 :: 		
	BCF         TRISE+0, 0 
;init_functions.h,12 :: 		
	BCF         TRISE+0, 1 
;init_functions.h,13 :: 		
	BCF         TRISE+0, 2 
;init_functions.h,14 :: 		
	BCF         TRISE+0, 3 
;init_functions.h,15 :: 		
L_end_PORTS_Init:
	RETURN      0
; end of _PORTS_Init

_Interrupt_Init:

;init_functions.h,18 :: 		
;init_functions.h,20 :: 		
	BSF         INTCON2+0, 6 
;init_functions.h,21 :: 		
	MOVLW       192
	IORWF       INTCON+0, 1 
;init_functions.h,22 :: 		
	BSF         INTCON+0, 3 
;init_functions.h,23 :: 		
	BCF         INTCON+0, 0 
;init_functions.h,24 :: 		
	BSF         PIE1+0, 5 
;init_functions.h,25 :: 		
L_end_Interrupt_Init:
	RETURN      0
; end of _Interrupt_Init

_UART_send_data:

;command_manager.h,5 :: 		
;command_manager.h,7 :: 		
L_UART_send_data25:
	BTFSC       TXSTA+0, 1 
	GOTO        L_UART_send_data26
	GOTO        L_UART_send_data25
L_UART_send_data26:
;command_manager.h,8 :: 		
	MOVF        FARG_UART_send_data_c+0, 0 
	MOVWF       TXREG+0 
;command_manager.h,9 :: 		
L_end_UART_send_data:
	RETURN      0
; end of _UART_send_data

_start_measures:

;command_manager.h,12 :: 		
;command_manager.h,14 :: 		
	MOVLW       109
	MOVWF       FARG_UART_send_data_c+0 
	CALL        _UART_send_data+0, 0
;command_manager.h,15 :: 		
	MOVLW       13
	MOVWF       FARG_UART_send_data_c+0 
	CALL        _UART_send_data+0, 0
;command_manager.h,16 :: 		
	MOVLW       10
	MOVWF       FARG_UART_send_data_c+0 
	CALL        _UART_send_data+0, 0
;command_manager.h,17 :: 		
	CLRF        _cpt+0 
	CLRF        _cpt+1 
;command_manager.h,18 :: 		
	CALL        _init_cpt_data+0, 0
;command_manager.h,19 :: 		
	MOVLW       1
	MOVWF       _flagProcess+0 
	MOVLW       0
	MOVWF       _flagProcess+1 
;command_manager.h,20 :: 		
	BSF         INTCON+0, 3 
;command_manager.h,21 :: 		
L_end_start_measures:
	RETURN      0
; end of _start_measures

_stop_measures:

;command_manager.h,24 :: 		
;command_manager.h,26 :: 		
	BCF         INTCON+0, 3 
;command_manager.h,27 :: 		
	CLRF        _flagProcess+0 
	CLRF        _flagProcess+1 
;command_manager.h,28 :: 		
	MOVLW       105
	MOVWF       FARG_UART_send_data_c+0 
	CALL        _UART_send_data+0, 0
;command_manager.h,29 :: 		
	MOVLW       13
	MOVWF       FARG_UART_send_data_c+0 
	CALL        _UART_send_data+0, 0
;command_manager.h,30 :: 		
	MOVLW       10
	MOVWF       FARG_UART_send_data_c+0 
	CALL        _UART_send_data+0, 0
;command_manager.h,31 :: 		
L_end_stop_measures:
	RETURN      0
; end of _stop_measures

_send_state:

;command_manager.h,34 :: 		
;command_manager.h,36 :: 		
	MOVF        FARG_send_state_state+0, 0 
	XORLW       1
	BTFSS       STATUS+0, 2 
	GOTO        L_send_state27
;command_manager.h,38 :: 		
	MOVLW       109
	MOVWF       FARG_UART_send_data_c+0 
	CALL        _UART_send_data+0, 0
;command_manager.h,39 :: 		
	GOTO        L_send_state28
L_send_state27:
;command_manager.h,42 :: 		
	MOVLW       105
	MOVWF       FARG_UART_send_data_c+0 
	CALL        _UART_send_data+0, 0
;command_manager.h,43 :: 		
L_send_state28:
;command_manager.h,44 :: 		
L_end_send_state:
	RETURN      0
; end of _send_state

_interrupt:

;main.c,42 :: 		void interrupt(void) {
;main.c,46 :: 		if(PIR1.RCIF==1){ // Receiving of data for PIC control
	BTFSS       PIR1+0, 5 
	GOTO        L_interrupt29
;main.c,47 :: 		char received_data = RCREG; // Reads the received data
	MOVF        RCREG+0, 0 
	MOVWF       interrupt_received_data_L1+0 
;main.c,48 :: 		PIR1.RCIF = 0; // Resets the interrupt flag
	BCF         PIR1+0, 5 
;main.c,49 :: 		if (received_k_factor) { // If the previous char received was a 'k', we check the value sent to change the k factor
	MOVF        _received_k_factor+0, 0 
	IORWF       _received_k_factor+1, 0 
	BTFSC       STATUS+0, 2 
	GOTO        L_interrupt30
;main.c,50 :: 		if (received_data >= '0' && received_data <= '9') {
	MOVLW       48
	SUBWF       interrupt_received_data_L1+0, 0 
	BTFSS       STATUS+0, 0 
	GOTO        L_interrupt33
	MOVF        interrupt_received_data_L1+0, 0 
	SUBLW       57
	BTFSS       STATUS+0, 0 
	GOTO        L_interrupt33
L__interrupt75:
;main.c,52 :: 		k = received_data - '0';
	MOVLW       48
	SUBWF       interrupt_received_data_L1+0, 0 
	MOVWF       _k+0 
	CLRF        _k+1 
	MOVLW       0
	SUBWFB      _k+1, 1 
;main.c,53 :: 		}
L_interrupt33:
;main.c,54 :: 		received_k_factor = 0; // Resets Flag after processing
	CLRF        _received_k_factor+0 
	CLRF        _received_k_factor+1 
;main.c,55 :: 		} else {
	GOTO        L_interrupt34
L_interrupt30:
;main.c,56 :: 		switch(received_data) {
	GOTO        L_interrupt35
;main.c,57 :: 		case 'k':
L_interrupt37:
;main.c,58 :: 		received_k_factor = 1; // Sets a flag to inform the PIC that the next char to process is the value of the k factor
	MOVLW       1
	MOVWF       _received_k_factor+0 
	MOVLW       0
	MOVWF       _received_k_factor+1 
;main.c,59 :: 		break;
	GOTO        L_interrupt36
;main.c,60 :: 		case 'g':  // GO command to launch measures
L_interrupt38:
;main.c,61 :: 		UART_send_data('m'); // Sends a char 'm' meaning the state "Measuring" to Application
	MOVLW       109
	MOVWF       FARG_UART_send_data_c+0 
	CALL        _UART_send_data+0, 0
;main.c,62 :: 		UART_send_data(0x0D); // Sends a line breaker
	MOVLW       13
	MOVWF       FARG_UART_send_data_c+0 
	CALL        _UART_send_data+0, 0
;main.c,63 :: 		UART_send_data(0x0A);
	MOVLW       10
	MOVWF       FARG_UART_send_data_c+0 
	CALL        _UART_send_data+0, 0
;main.c,64 :: 		cpt=0;           // Counter init
	CLRF        _cpt+0 
	CLRF        _cpt+1 
;main.c,65 :: 		init_cpt_data(); // Data tab init
	CALL        _init_cpt_data+0, 0
;main.c,66 :: 		flagProcess = 1;    // Updates the process Flag for the process loop
	MOVLW       1
	MOVWF       _flagProcess+0 
	MOVLW       0
	MOVWF       _flagProcess+1 
;main.c,67 :: 		INTCON.RBIE=1; // Enables interruptions on PORTB
	BSF         INTCON+0, 3 
;main.c,68 :: 		break;
	GOTO        L_interrupt36
;main.c,69 :: 		case 's':  // STOP command to stop measures
L_interrupt39:
;main.c,70 :: 		flagProcess = 0;
	CLRF        _flagProcess+0 
	CLRF        _flagProcess+1 
;main.c,71 :: 		INTCON.RBIE=0; // Disables interruptions on PORTB
	BCF         INTCON+0, 3 
;main.c,72 :: 		flagProcess = 0;    // Updates process flag to exit the processing loop
	CLRF        _flagProcess+0 
	CLRF        _flagProcess+1 
;main.c,73 :: 		UART_send_data('i'); // Sends a char 'i' meaning the state "Idle" to Application
	MOVLW       105
	MOVWF       FARG_UART_send_data_c+0 
	CALL        _UART_send_data+0, 0
;main.c,74 :: 		UART_send_data(0x0D); // Line breaker
	MOVLW       13
	MOVWF       FARG_UART_send_data_c+0 
	CALL        _UART_send_data+0, 0
;main.c,75 :: 		UART_send_data(0x0A);
	MOVLW       10
	MOVWF       FARG_UART_send_data_c+0 
	CALL        _UART_send_data+0, 0
;main.c,76 :: 		break;
	GOTO        L_interrupt36
;main.c,77 :: 		case 'e':  // ERLANG command to select the measure mode Erlang
L_interrupt40:
;main.c,78 :: 		mode = 0;
	CLRF        _mode+0 
	CLRF        _mode+1 
;main.c,79 :: 		break;
	GOTO        L_interrupt36
;main.c,80 :: 		case 'p':  // POISSON command to select the measure mode Poisson
L_interrupt41:
;main.c,81 :: 		mode = 1;
	MOVLW       1
	MOVWF       _mode+0 
	MOVLW       0
	MOVWF       _mode+1 
;main.c,82 :: 		break;
	GOTO        L_interrupt36
;main.c,83 :: 		case 'o': // POOL command to select the measure mode Pool
L_interrupt42:
;main.c,84 :: 		mode = 2;
	MOVLW       2
	MOVWF       _mode+0 
	MOVLW       0
	MOVWF       _mode+1 
;main.c,85 :: 		break;
	GOTO        L_interrupt36
;main.c,86 :: 		case '?': // QUESTION command to ask PIC to send its current state
L_interrupt43:
;main.c,87 :: 		UART_send_string("Hello from PIC18F4550 !");
	MOVLW       ?lstr_1_main+0
	MOVWF       FARG_UART_send_string_d+0 
	MOVLW       hi_addr(?lstr_1_main+0)
	MOVWF       FARG_UART_send_string_d+1 
	MOVLW       higher_addr(?lstr_1_main+0)
	MOVWF       FARG_UART_send_string_d+2 
	CALL        _UART_send_string+0, 0
;main.c,88 :: 		UART_send_data(0x0D); // Line breaker
	MOVLW       13
	MOVWF       FARG_UART_send_data_c+0 
	CALL        _UART_send_data+0, 0
;main.c,89 :: 		UART_send_data(0x0A);
	MOVLW       10
	MOVWF       FARG_UART_send_data_c+0 
	CALL        _UART_send_data+0, 0
;main.c,90 :: 		UART_send_string("Find my source code at : https://github.com/BapaLCA/Nuclear-Disintegration-AppDev");
	MOVLW       ?lstr_2_main+0
	MOVWF       FARG_UART_send_string_d+0 
	MOVLW       hi_addr(?lstr_2_main+0)
	MOVWF       FARG_UART_send_string_d+1 
	MOVLW       higher_addr(?lstr_2_main+0)
	MOVWF       FARG_UART_send_string_d+2 
	CALL        _UART_send_string+0, 0
;main.c,91 :: 		UART_send_data(0x0D); // Line breaker
	MOVLW       13
	MOVWF       FARG_UART_send_data_c+0 
	CALL        _UART_send_data+0, 0
;main.c,92 :: 		UART_send_data(0x0A);
	MOVLW       10
	MOVWF       FARG_UART_send_data_c+0 
	CALL        _UART_send_data+0, 0
;main.c,93 :: 		send_state(flagProcess);
	MOVF        _flagProcess+0, 0 
	MOVWF       FARG_send_state_state+0 
	CALL        _send_state+0, 0
;main.c,94 :: 		UART_send_data(0x0D); // Line breaker
	MOVLW       13
	MOVWF       FARG_UART_send_data_c+0 
	CALL        _UART_send_data+0, 0
;main.c,95 :: 		UART_send_data(0x0A);
	MOVLW       10
	MOVWF       FARG_UART_send_data_c+0 
	CALL        _UART_send_data+0, 0
;main.c,96 :: 		break;
	GOTO        L_interrupt36
;main.c,97 :: 		case 'u': // Update POOL mode command to end the current measure and send the data measured
L_interrupt44:
;main.c,98 :: 		flagWrite = 1; // Enable flag Write to send to UART the current measured data
	MOVLW       1
	MOVWF       _flagWrite+0 
	MOVLW       0
	MOVWF       _flagWrite+1 
;main.c,99 :: 		break;
	GOTO        L_interrupt36
;main.c,100 :: 		case 'r': // Reset POOL mode command to reset the number of measures done
L_interrupt45:
;main.c,101 :: 		measureCount=0;
	CLRF        _measureCount+0 
	CLRF        _measureCount+1 
;main.c,102 :: 		break;
	GOTO        L_interrupt36
;main.c,103 :: 		default:
L_interrupt46:
;main.c,105 :: 		break;
	GOTO        L_interrupt36
;main.c,106 :: 		}
L_interrupt35:
	MOVF        interrupt_received_data_L1+0, 0 
	XORLW       107
	BTFSC       STATUS+0, 2 
	GOTO        L_interrupt37
	MOVF        interrupt_received_data_L1+0, 0 
	XORLW       103
	BTFSC       STATUS+0, 2 
	GOTO        L_interrupt38
	MOVF        interrupt_received_data_L1+0, 0 
	XORLW       115
	BTFSC       STATUS+0, 2 
	GOTO        L_interrupt39
	MOVF        interrupt_received_data_L1+0, 0 
	XORLW       101
	BTFSC       STATUS+0, 2 
	GOTO        L_interrupt40
	MOVF        interrupt_received_data_L1+0, 0 
	XORLW       112
	BTFSC       STATUS+0, 2 
	GOTO        L_interrupt41
	MOVF        interrupt_received_data_L1+0, 0 
	XORLW       111
	BTFSC       STATUS+0, 2 
	GOTO        L_interrupt42
	MOVF        interrupt_received_data_L1+0, 0 
	XORLW       63
	BTFSC       STATUS+0, 2 
	GOTO        L_interrupt43
	MOVF        interrupt_received_data_L1+0, 0 
	XORLW       117
	BTFSC       STATUS+0, 2 
	GOTO        L_interrupt44
	MOVF        interrupt_received_data_L1+0, 0 
	XORLW       114
	BTFSC       STATUS+0, 2 
	GOTO        L_interrupt45
	GOTO        L_interrupt46
L_interrupt36:
;main.c,107 :: 		}
L_interrupt34:
;main.c,108 :: 		}
	GOTO        L_interrupt47
L_interrupt29:
;main.c,110 :: 		if(mode==0){ // Erlang
	MOVLW       0
	XORWF       _mode+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__interrupt97
	MOVLW       0
	XORWF       _mode+0, 0 
L__interrupt97:
	BTFSS       STATUS+0, 2 
	GOTO        L_interrupt48
;main.c,111 :: 		if(prevrb7==0){
	MOVLW       0
	XORWF       _prevrb7+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__interrupt98
	MOVLW       0
	XORWF       _prevrb7+0, 0 
L__interrupt98:
	BTFSS       STATUS+0, 2 
	GOTO        L_interrupt49
;main.c,112 :: 		cpt = 0;      // Counter Init
	CLRF        _cpt+0 
	CLRF        _cpt+1 
;main.c,113 :: 		cptk = 0;     // Pulse Counter Init
	CLRF        _cptk+0 
	CLRF        _cptk+1 
;main.c,114 :: 		flagStart = 1;// Launches the counter
	MOVLW       1
	MOVWF       _flagStart+0 
	MOVLW       0
	MOVWF       _flagStart+1 
;main.c,115 :: 		prevrb7 = 1;  // Saves the previous state of RB7
	MOVLW       1
	MOVWF       _prevrb7+0 
	MOVLW       0
	MOVWF       _prevrb7+1 
;main.c,116 :: 		}
	GOTO        L_interrupt50
L_interrupt49:
;main.c,118 :: 		cptk++;
	MOVLW       1
	ADDWF       _cptk+0, 0 
	MOVWF       R0 
	MOVLW       0
	ADDWFC      _cptk+1, 0 
	MOVWF       R1 
	MOVF        R0, 0 
	MOVWF       _cptk+0 
	MOVF        R1, 0 
	MOVWF       _cptk+1 
;main.c,119 :: 		if(cptk==k){ // Check the number of pulses measured
	MOVF        _cptk+1, 0 
	XORWF       _k+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__interrupt99
	MOVF        _k+0, 0 
	XORWF       _cptk+0, 0 
L__interrupt99:
	BTFSS       STATUS+0, 2 
	GOTO        L_interrupt51
;main.c,120 :: 		flagStart = 0;      // Stops counter
	CLRF        _flagStart+0 
	CLRF        _flagStart+1 
;main.c,121 :: 		prevrb7 = 0;        // Saves the previous state of RB7
	CLRF        _prevrb7+0 
	CLRF        _prevrb7+1 
;main.c,122 :: 		cpt_data[cpt]++;    // Saves the data in the corresponding index
	MOVLW       _cpt_data+0
	ADDWF       _cpt+0, 0 
	MOVWF       R1 
	MOVLW       hi_addr(_cpt_data+0)
	ADDWFC      _cpt+1, 0 
	MOVWF       R2 
	MOVFF       R1, FSR0L+0
	MOVFF       R2, FSR0H+0
	MOVF        POSTINC0+0, 0 
	MOVWF       R0 
	INCF        R0, 1 
	MOVFF       R1, FSR1L+0
	MOVFF       R2, FSR1H+0
	MOVF        R0, 0 
	MOVWF       POSTINC1+0 
;main.c,123 :: 		}
L_interrupt51:
;main.c,124 :: 		}
L_interrupt50:
;main.c,125 :: 		if(cpt_data[cpt]==255){  // When one of the tab cell reaches 255 (8 bits limit), it enables the writing loop and sends all measured data
	MOVLW       _cpt_data+0
	ADDWF       _cpt+0, 0 
	MOVWF       FSR0L+0 
	MOVLW       hi_addr(_cpt_data+0)
	ADDWFC      _cpt+1, 0 
	MOVWF       FSR0L+1 
	MOVF        POSTINC0+0, 0 
	MOVWF       R1 
	MOVF        R1, 0 
	XORLW       255
	BTFSS       STATUS+0, 2 
	GOTO        L_interrupt52
;main.c,126 :: 		INTCON &= 0b00110111; // Disable interruptions
	MOVLW       55
	ANDWF       INTCON+0, 1 
;main.c,127 :: 		flagWrite = 1; // Enables writing Flag
	MOVLW       1
	MOVWF       _flagWrite+0 
	MOVLW       0
	MOVWF       _flagWrite+1 
;main.c,128 :: 		}
L_interrupt52:
;main.c,129 :: 		}
L_interrupt48:
;main.c,131 :: 		if(mode==1){ //Poisson
	MOVLW       0
	XORWF       _mode+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__interrupt100
	MOVLW       1
	XORWF       _mode+0, 0 
L__interrupt100:
	BTFSS       STATUS+0, 2 
	GOTO        L_interrupt53
;main.c,132 :: 		Counting(); // Counts the number of pulses on cpt variable on pulse detection
	CALL        _Counting+0, 0
;main.c,133 :: 		}
L_interrupt53:
;main.c,135 :: 		if(mode==2){ // Pool
	MOVLW       0
	XORWF       _mode+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__interrupt101
	MOVLW       2
	XORWF       _mode+0, 0 
L__interrupt101:
	BTFSS       STATUS+0, 2 
	GOTO        L_interrupt54
;main.c,136 :: 		cpt++; // Counts the number of pulses on cpt variable on pulse detection, no call for Counting needed as we have no counting limit on this mode
	MOVLW       1
	ADDWF       _cpt+0, 0 
	MOVWF       R0 
	MOVLW       0
	ADDWFC      _cpt+1, 0 
	MOVWF       R1 
	MOVF        R0, 0 
	MOVWF       _cpt+0 
	MOVF        R1, 0 
	MOVWF       _cpt+1 
;main.c,137 :: 		}
L_interrupt54:
;main.c,140 :: 		while(PORTB.B7==1); // Waiting for pulse to be over before quitting interrupt function
L_interrupt55:
	BTFSS       PORTB+0, 7 
	GOTO        L_interrupt56
	GOTO        L_interrupt55
L_interrupt56:
;main.c,141 :: 		INTCON.RBIF = 0; // Resets the interrupt flag RBIF
	BCF         INTCON+0, 0 
;main.c,142 :: 		}
L_interrupt47:
;main.c,143 :: 		}
L_end_interrupt:
L__interrupt96:
	RETFIE      1
; end of _interrupt

_main:

;main.c,148 :: 		void main() {
;main.c,150 :: 		PORTS_Init();  // PORTs init
	CALL        _PORTS_Init+0, 0
;main.c,152 :: 		ADCON0 = 0;
	CLRF        ADCON0+0 
;main.c,153 :: 		PORTE.B1 = 0;
	BCF         PORTE+0, 1 
;main.c,154 :: 		PORTE.B2 = 0;
	BCF         PORTE+0, 2 
;main.c,155 :: 		PORTE.B0 = 0;
	BCF         PORTE+0, 0 
;main.c,156 :: 		PORTB.B1 = 0;
	BCF         PORTB+0, 1 
;main.c,158 :: 		UART1_Init(9600); // UART speed configuration set to 9600 Bauds
	BSF         BAUDCON+0, 3, 0
	MOVLW       4
	MOVWF       SPBRGH+0 
	MOVLW       225
	MOVWF       SPBRG+0 
	BSF         TXSTA+0, 2, 0
	CALL        _UART1_Init+0, 0
;main.c,160 :: 		delay_ms(1000); // Delay to wait for UART to stabilize
	MOVLW       61
	MOVWF       R11, 0
	MOVLW       225
	MOVWF       R12, 0
	MOVLW       63
	MOVWF       R13, 0
L_main57:
	DECFSZ      R13, 1, 1
	BRA         L_main57
	DECFSZ      R12, 1, 1
	BRA         L_main57
	DECFSZ      R11, 1, 1
	BRA         L_main57
	NOP
	NOP
;main.c,161 :: 		init_cpt_data();// Data tab init
	CALL        _init_cpt_data+0, 0
;main.c,162 :: 		Interrupt_Init(); // Sets up the interrupt registers
	CALL        _Interrupt_Init+0, 0
;main.c,163 :: 		INTCON.RBIE=0; // PORTB interrupt shall remain disabled on launch
	BCF         INTCON+0, 3 
;main.c,166 :: 		while (exitloop==0){
L_main58:
	MOVLW       0
	XORWF       _exitloop+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__main103
	MOVLW       0
	XORWF       _exitloop+0, 0 
L__main103:
	BTFSS       STATUS+0, 2 
	GOTO        L_main59
;main.c,170 :: 		while(flagProcess==1){
L_main60:
	MOVLW       0
	XORWF       _flagProcess+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__main104
	MOVLW       1
	XORWF       _flagProcess+0, 0 
L__main104:
	BTFSS       STATUS+0, 2 
	GOTO        L_main61
;main.c,172 :: 		if(mode==0){ // Erlang
	MOVLW       0
	XORWF       _mode+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__main105
	MOVLW       0
	XORWF       _mode+0, 0 
L__main105:
	BTFSS       STATUS+0, 2 
	GOTO        L_main62
;main.c,173 :: 		if(PORTC.B0==1){
	BTFSS       PORTC+0, 0 
	GOTO        L_main63
;main.c,174 :: 		if(prevrc0==0){ // Rising edge
	MOVLW       0
	XORWF       _prevrc0+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__main106
	MOVLW       0
	XORWF       _prevrc0+0, 0 
L__main106:
	BTFSS       STATUS+0, 2 
	GOTO        L_main64
;main.c,175 :: 		Counting(); // Increases the counter when a clock rising edge is detected
	CALL        _Counting+0, 0
;main.c,176 :: 		prevrc0=1; // Saves the previous state of RC0
	MOVLW       1
	MOVWF       _prevrc0+0 
	MOVLW       0
	MOVWF       _prevrc0+1 
;main.c,177 :: 		}
L_main64:
;main.c,178 :: 		}
	GOTO        L_main65
L_main63:
;main.c,180 :: 		prevrc0=0;  // Saves the previous state of RC0
	CLRF        _prevrc0+0 
	CLRF        _prevrc0+1 
;main.c,181 :: 		}
L_main65:
;main.c,182 :: 		}
L_main62:
;main.c,184 :: 		if(mode==1){ // Poisson Mode
	MOVLW       0
	XORWF       _mode+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__main107
	MOVLW       1
	XORWF       _mode+0, 0 
L__main107:
	BTFSS       STATUS+0, 2 
	GOTO        L_main66
;main.c,185 :: 		flagStart=1;
	MOVLW       1
	MOVWF       _flagStart+0 
	MOVLW       0
	MOVWF       _flagStart+1 
;main.c,186 :: 		if(PORTC.B0==1){
	BTFSS       PORTC+0, 0 
	GOTO        L_main67
;main.c,187 :: 		cpt_data[cpt]++; // Saves on Index corresponding to the amount of pulses measured
	MOVLW       _cpt_data+0
	ADDWF       _cpt+0, 0 
	MOVWF       R1 
	MOVLW       hi_addr(_cpt_data+0)
	ADDWFC      _cpt+1, 0 
	MOVWF       R2 
	MOVFF       R1, FSR0L+0
	MOVFF       R2, FSR0H+0
	MOVF        POSTINC0+0, 0 
	MOVWF       R0 
	INCF        R0, 1 
	MOVFF       R1, FSR1L+0
	MOVFF       R2, FSR1H+0
	MOVF        R0, 0 
	MOVWF       POSTINC1+0 
;main.c,188 :: 		cpt=0;          // Counter reset
	CLRF        _cpt+0 
	CLRF        _cpt+1 
;main.c,189 :: 		while(PORTC.B0); // Waiting for the high level of the clock to end
L_main68:
	BTFSS       PORTC+0, 0 
	GOTO        L_main69
	GOTO        L_main68
L_main69:
;main.c,190 :: 		}
L_main67:
;main.c,192 :: 		if(cpt_data[cpt]==255){  // When a cell's value reaches 255 (8 bits limit) the data is sent through UART
	MOVLW       _cpt_data+0
	ADDWF       _cpt+0, 0 
	MOVWF       FSR0L+0 
	MOVLW       hi_addr(_cpt_data+0)
	ADDWFC      _cpt+1, 0 
	MOVWF       FSR0L+1 
	MOVF        POSTINC0+0, 0 
	MOVWF       R1 
	MOVF        R1, 0 
	XORLW       255
	BTFSS       STATUS+0, 2 
	GOTO        L_main70
;main.c,193 :: 		INTCON &= 0b00110111; // Disables interruptions for writing
	MOVLW       55
	ANDWF       INTCON+0, 1 
;main.c,194 :: 		flagWrite = 1; // Enables writing flag
	MOVLW       1
	MOVWF       _flagWrite+0 
	MOVLW       0
	MOVWF       _flagWrite+1 
;main.c,195 :: 		}
L_main70:
;main.c,196 :: 		}
L_main66:
;main.c,198 :: 		if(mode==2){ // Piscine
	MOVLW       0
	XORWF       _mode+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__main108
	MOVLW       2
	XORWF       _mode+0, 0 
L__main108:
	BTFSS       STATUS+0, 2 
	GOTO        L_main71
;main.c,199 :: 		flagStart=1; // No processing on secondary input here
	MOVLW       1
	MOVWF       _flagStart+0 
	MOVLW       0
	MOVWF       _flagStart+1 
;main.c,200 :: 		}
L_main71:
;main.c,205 :: 		if(flagWrite==1){ // Data sending function
	MOVLW       0
	XORWF       _flagWrite+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__main109
	MOVLW       1
	XORWF       _flagWrite+0, 0 
L__main109:
	BTFSS       STATUS+0, 2 
	GOTO        L_main72
;main.c,206 :: 		if(mode<=1){ // Sends data in a tab form for modes Erlang/Poisson
	MOVLW       128
	MOVWF       R0 
	MOVLW       128
	XORWF       _mode+1, 0 
	SUBWF       R0, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__main110
	MOVF        _mode+0, 0 
	SUBLW       1
L__main110:
	BTFSS       STATUS+0, 0 
	GOTO        L_main73
;main.c,207 :: 		send_data(); // Sends data towards UART Terminal
	CALL        _send_data+0, 0
;main.c,208 :: 		init_cpt_data();
	CALL        _init_cpt_data+0, 0
;main.c,209 :: 		}
L_main73:
;main.c,210 :: 		if(mode==2){ // Sends data as a single line for Pool mode
	MOVLW       0
	XORWF       _mode+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__main111
	MOVLW       2
	XORWF       _mode+0, 0 
L__main111:
	BTFSS       STATUS+0, 2 
	GOTO        L_main74
;main.c,211 :: 		send_data_pool(); // Sends data towards UART Terminal
	CALL        _send_data_pool+0, 0
;main.c,212 :: 		cpt=0; // Resets counter only, cpt_data is not used in this mode
	CLRF        _cpt+0 
	CLRF        _cpt+1 
;main.c,213 :: 		}
L_main74:
;main.c,214 :: 		flagWrite=0;
	CLRF        _flagWrite+0 
	CLRF        _flagWrite+1 
;main.c,215 :: 		INTCON |= 0b11001000; // Enables back all interruptions
	MOVLW       200
	IORWF       INTCON+0, 1 
;main.c,216 :: 		}
L_main72:
;main.c,217 :: 		}
	GOTO        L_main60
L_main61:
;main.c,218 :: 		}
	GOTO        L_main58
L_main59:
;main.c,219 :: 		}
L_end_main:
	GOTO        $+0
; end of _main
