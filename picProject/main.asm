
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

_display7segInt:

;7seg_functions.h,43 :: 		
;7seg_functions.h,45 :: 		
	MOVLW       1
	MOVWF       PORTA+0 
	MOVLW       10
	MOVWF       R4 
	MOVLW       0
	MOVWF       R5 
	MOVF        FARG_display7segInt_value+0, 0 
	MOVWF       R0 
	MOVF        FARG_display7segInt_value+1, 0 
	MOVWF       R1 
	CALL        _Div_16X16_U+0, 0
	MOVF        R8, 0 
	MOVWF       R0 
	MOVF        R9, 0 
	MOVWF       R1 
	MOVLW       _DIGITS+0
	ADDWF       R0, 0 
	MOVWF       TBLPTR+0 
	MOVLW       hi_addr(_DIGITS+0)
	ADDWFC      R1, 0 
	MOVWF       TBLPTR+1 
	MOVLW       higher_addr(_DIGITS+0)
	MOVWF       TBLPTR+2 
	MOVLW       0
	ADDWFC      TBLPTR+2, 1 
	TBLRD*+
	MOVFF       TABLAT+0, PORTD+0
	MOVLW       47
	MOVWF       R12, 0
	MOVLW       191
	MOVWF       R13, 0
L_display7segInt16:
	DECFSZ      R13, 1, 1
	BRA         L_display7segInt16
	DECFSZ      R12, 1, 1
	BRA         L_display7segInt16
	NOP
	NOP
;7seg_functions.h,46 :: 		
	MOVLW       2
	MOVWF       PORTA+0 
	MOVLW       100
	MOVWF       R4 
	MOVLW       0
	MOVWF       R5 
	MOVF        FARG_display7segInt_value+0, 0 
	MOVWF       R0 
	MOVF        FARG_display7segInt_value+1, 0 
	MOVWF       R1 
	CALL        _Div_16X16_U+0, 0
	MOVF        R8, 0 
	MOVWF       R0 
	MOVF        R9, 0 
	MOVWF       R1 
	MOVLW       10
	MOVWF       R4 
	MOVLW       0
	MOVWF       R5 
	CALL        _Div_16X16_U+0, 0
	MOVLW       _DIGITS+0
	ADDWF       R0, 0 
	MOVWF       TBLPTR+0 
	MOVLW       hi_addr(_DIGITS+0)
	ADDWFC      R1, 0 
	MOVWF       TBLPTR+1 
	MOVLW       higher_addr(_DIGITS+0)
	MOVWF       TBLPTR+2 
	MOVLW       0
	ADDWFC      TBLPTR+2, 1 
	TBLRD*+
	MOVFF       TABLAT+0, PORTD+0
	MOVLW       47
	MOVWF       R12, 0
	MOVLW       191
	MOVWF       R13, 0
L_display7segInt17:
	DECFSZ      R13, 1, 1
	BRA         L_display7segInt17
	DECFSZ      R12, 1, 1
	BRA         L_display7segInt17
	NOP
	NOP
;7seg_functions.h,47 :: 		
	MOVLW       4
	MOVWF       PORTA+0 
	MOVLW       232
	MOVWF       R4 
	MOVLW       3
	MOVWF       R5 
	MOVF        FARG_display7segInt_value+0, 0 
	MOVWF       R0 
	MOVF        FARG_display7segInt_value+1, 0 
	MOVWF       R1 
	CALL        _Div_16X16_U+0, 0
	MOVF        R8, 0 
	MOVWF       R0 
	MOVF        R9, 0 
	MOVWF       R1 
	MOVLW       100
	MOVWF       R4 
	MOVLW       0
	MOVWF       R5 
	CALL        _Div_16X16_U+0, 0
	MOVLW       _DIGITS+0
	ADDWF       R0, 0 
	MOVWF       TBLPTR+0 
	MOVLW       hi_addr(_DIGITS+0)
	ADDWFC      R1, 0 
	MOVWF       TBLPTR+1 
	MOVLW       higher_addr(_DIGITS+0)
	MOVWF       TBLPTR+2 
	MOVLW       0
	ADDWFC      TBLPTR+2, 1 
	TBLRD*+
	MOVFF       TABLAT+0, PORTD+0
	MOVLW       47
	MOVWF       R12, 0
	MOVLW       191
	MOVWF       R13, 0
L_display7segInt18:
	DECFSZ      R13, 1, 1
	BRA         L_display7segInt18
	DECFSZ      R12, 1, 1
	BRA         L_display7segInt18
	NOP
	NOP
;7seg_functions.h,48 :: 		
	MOVLW       8
	MOVWF       PORTA+0 
	MOVLW       232
	MOVWF       R4 
	MOVLW       3
	MOVWF       R5 
	MOVF        FARG_display7segInt_value+0, 0 
	MOVWF       R0 
	MOVF        FARG_display7segInt_value+1, 0 
	MOVWF       R1 
	CALL        _Div_16X16_U+0, 0
	MOVLW       _DIGITS+0
	ADDWF       R0, 0 
	MOVWF       TBLPTR+0 
	MOVLW       hi_addr(_DIGITS+0)
	ADDWFC      R1, 0 
	MOVWF       TBLPTR+1 
	MOVLW       higher_addr(_DIGITS+0)
	MOVWF       TBLPTR+2 
	MOVLW       0
	ADDWFC      TBLPTR+2, 1 
	TBLRD*+
	MOVFF       TABLAT+0, PORTD+0
	MOVLW       47
	MOVWF       R12, 0
	MOVLW       191
	MOVWF       R13, 0
L_display7segInt19:
	DECFSZ      R13, 1, 1
	BRA         L_display7segInt19
	DECFSZ      R12, 1, 1
	BRA         L_display7segInt19
	NOP
	NOP
;7seg_functions.h,49 :: 		
L_end_display7segInt:
	RETURN      0
; end of _display7segInt

_display7segChar:

;7seg_functions.h,51 :: 		
;7seg_functions.h,53 :: 		
	MOVF        FARG_display7segChar_digit+0, 0 
	MOVWF       PORTA+0 
	MOVLW       _LETTERS+0
	ADDWF       FARG_display7segChar_value+0, 0 
	MOVWF       TBLPTR+0 
	MOVLW       hi_addr(_LETTERS+0)
	ADDWFC      FARG_display7segChar_value+1, 0 
	MOVWF       TBLPTR+1 
	MOVLW       higher_addr(_LETTERS+0)
	MOVWF       TBLPTR+2 
	MOVLW       0
	ADDWFC      TBLPTR+2, 1 
	TBLRD*+
	MOVFF       TABLAT+0, PORTD+0
;7seg_functions.h,54 :: 		
L_end_display7segChar:
	RETURN      0
; end of _display7segChar

_displayClear:

;7seg_functions.h,56 :: 		
;7seg_functions.h,57 :: 		
	MOVLW       1
	MOVWF       PORTA+0 
	CLRF        PORTD+0 
;7seg_functions.h,58 :: 		
L_end_displayClear:
	RETURN      0
; end of _displayClear

_displayIntSingleDigit:

;7seg_functions.h,60 :: 		
;7seg_functions.h,61 :: 		
	MOVLW       1
	MOVWF       PORTA+0 
	MOVLW       _DIGITS+0
	ADDWF       FARG_displayIntSingleDigit_nb+0, 0 
	MOVWF       TBLPTR+0 
	MOVLW       hi_addr(_DIGITS+0)
	ADDWFC      FARG_displayIntSingleDigit_nb+1, 0 
	MOVWF       TBLPTR+1 
	MOVLW       higher_addr(_DIGITS+0)
	MOVWF       TBLPTR+2 
	MOVLW       0
	BTFSC       FARG_displayIntSingleDigit_nb+1, 7 
	MOVLW       255
	ADDWFC      TBLPTR+2, 1 
	TBLRD*+
	MOVFF       TABLAT+0, PORTD+0
;7seg_functions.h,62 :: 		
L_end_displayIntSingleDigit:
	RETURN      0
; end of _displayIntSingleDigit

_displayStop:

;7seg_functions.h,64 :: 		
;7seg_functions.h,65 :: 		
	MOVLW       16
	MOVWF       FARG_display7segChar_value+0 
	MOVLW       0
	MOVWF       FARG_display7segChar_value+1 
	MOVLW       8
	MOVWF       FARG_display7segChar_digit+0 
	MOVLW       0
	MOVWF       FARG_display7segChar_digit+1 
	CALL        _display7segChar+0, 0
	MOVLW       47
	MOVWF       R12, 0
	MOVLW       191
	MOVWF       R13, 0
L_displayStop20:
	DECFSZ      R13, 1, 1
	BRA         L_displayStop20
	DECFSZ      R12, 1, 1
	BRA         L_displayStop20
	NOP
	NOP
;7seg_functions.h,66 :: 		
	MOVLW       17
	MOVWF       FARG_display7segChar_value+0 
	MOVLW       0
	MOVWF       FARG_display7segChar_value+1 
	MOVLW       4
	MOVWF       FARG_display7segChar_digit+0 
	MOVLW       0
	MOVWF       FARG_display7segChar_digit+1 
	CALL        _display7segChar+0, 0
	MOVLW       47
	MOVWF       R12, 0
	MOVLW       191
	MOVWF       R13, 0
L_displayStop21:
	DECFSZ      R13, 1, 1
	BRA         L_displayStop21
	DECFSZ      R12, 1, 1
	BRA         L_displayStop21
	NOP
	NOP
;7seg_functions.h,67 :: 		
	MOVLW       12
	MOVWF       FARG_display7segChar_value+0 
	MOVLW       0
	MOVWF       FARG_display7segChar_value+1 
	MOVLW       2
	MOVWF       FARG_display7segChar_digit+0 
	MOVLW       0
	MOVWF       FARG_display7segChar_digit+1 
	CALL        _display7segChar+0, 0
	MOVLW       47
	MOVWF       R12, 0
	MOVLW       191
	MOVWF       R13, 0
L_displayStop22:
	DECFSZ      R13, 1, 1
	BRA         L_displayStop22
	DECFSZ      R12, 1, 1
	BRA         L_displayStop22
	NOP
	NOP
;7seg_functions.h,68 :: 		
	MOVLW       13
	MOVWF       FARG_display7segChar_value+0 
	MOVLW       0
	MOVWF       FARG_display7segChar_value+1 
	MOVLW       1
	MOVWF       FARG_display7segChar_digit+0 
	MOVLW       0
	MOVWF       FARG_display7segChar_digit+1 
	CALL        _display7segChar+0, 0
	MOVLW       47
	MOVWF       R12, 0
	MOVLW       191
	MOVWF       R13, 0
L_displayStop23:
	DECFSZ      R13, 1, 1
	BRA         L_displayStop23
	DECFSZ      R12, 1, 1
	BRA         L_displayStop23
	NOP
	NOP
;7seg_functions.h,69 :: 		
L_end_displayStop:
	RETURN      0
; end of _displayStop

_displayRun:

;7seg_functions.h,71 :: 		
;7seg_functions.h,72 :: 		
	MOVLW       15
	MOVWF       FARG_display7segChar_value+0 
	MOVLW       0
	MOVWF       FARG_display7segChar_value+1 
	MOVLW       4
	MOVWF       FARG_display7segChar_digit+0 
	MOVLW       0
	MOVWF       FARG_display7segChar_digit+1 
	CALL        _display7segChar+0, 0
;7seg_functions.h,73 :: 		
	MOVLW       18
	MOVWF       FARG_display7segChar_value+0 
	MOVLW       0
	MOVWF       FARG_display7segChar_value+1 
	MOVLW       2
	MOVWF       FARG_display7segChar_digit+0 
	MOVLW       0
	MOVWF       FARG_display7segChar_digit+1 
	CALL        _display7segChar+0, 0
;7seg_functions.h,74 :: 		
	MOVLW       11
	MOVWF       FARG_display7segChar_value+0 
	MOVLW       0
	MOVWF       FARG_display7segChar_value+1 
	MOVLW       1
	MOVWF       FARG_display7segChar_digit+0 
	MOVLW       0
	MOVWF       FARG_display7segChar_digit+1 
	CALL        _display7segChar+0, 0
;7seg_functions.h,75 :: 		
L_end_displayRun:
	RETURN      0
; end of _displayRun

_displayEnd:

;7seg_functions.h,77 :: 		
;7seg_functions.h,78 :: 		
	MOVLW       4
	MOVWF       FARG_display7segChar_value+0 
	MOVLW       0
	MOVWF       FARG_display7segChar_value+1 
	MOVLW       4
	MOVWF       FARG_display7segChar_digit+0 
	MOVLW       0
	MOVWF       FARG_display7segChar_digit+1 
	CALL        _display7segChar+0, 0
	MOVLW       47
	MOVWF       R12, 0
	MOVLW       191
	MOVWF       R13, 0
L_displayEnd24:
	DECFSZ      R13, 1, 1
	BRA         L_displayEnd24
	DECFSZ      R12, 1, 1
	BRA         L_displayEnd24
	NOP
	NOP
;7seg_functions.h,79 :: 		
	MOVLW       11
	MOVWF       FARG_display7segChar_value+0 
	MOVLW       0
	MOVWF       FARG_display7segChar_value+1 
	MOVLW       2
	MOVWF       FARG_display7segChar_digit+0 
	MOVLW       0
	MOVWF       FARG_display7segChar_digit+1 
	CALL        _display7segChar+0, 0
	MOVLW       47
	MOVWF       R12, 0
	MOVLW       191
	MOVWF       R13, 0
L_displayEnd25:
	DECFSZ      R13, 1, 1
	BRA         L_displayEnd25
	DECFSZ      R12, 1, 1
	BRA         L_displayEnd25
	NOP
	NOP
;7seg_functions.h,80 :: 		
	MOVLW       3
	MOVWF       FARG_display7segChar_value+0 
	MOVLW       0
	MOVWF       FARG_display7segChar_value+1 
	MOVLW       1
	MOVWF       FARG_display7segChar_digit+0 
	MOVLW       0
	MOVWF       FARG_display7segChar_digit+1 
	CALL        _display7segChar+0, 0
	MOVLW       47
	MOVWF       R12, 0
	MOVLW       191
	MOVWF       R13, 0
L_displayEnd26:
	DECFSZ      R13, 1, 1
	BRA         L_displayEnd26
	DECFSZ      R12, 1, 1
	BRA         L_displayEnd26
	NOP
	NOP
;7seg_functions.h,81 :: 		
L_end_displayEnd:
	RETURN      0
; end of _displayEnd

_Counting:

;counting_functions.h,16 :: 		
;counting_functions.h,18 :: 		
	MOVLW       0
	XORWF       _flagStart+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__Counting98
	MOVLW       1
	XORWF       _flagStart+0, 0 
L__Counting98:
	BTFSS       STATUS+0, 2 
	GOTO        L_Counting27
;counting_functions.h,19 :: 		
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
;counting_functions.h,20 :: 		
L_Counting27:
;counting_functions.h,21 :: 		
	MOVLW       128
	XORLW       4
	MOVWF       R0 
	MOVLW       128
	XORWF       _cpt+1, 0 
	SUBWF       R0, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__Counting99
	MOVF        _cpt+0, 0 
	SUBLW       0
L__Counting99:
	BTFSC       STATUS+0, 0 
	GOTO        L_Counting28
;counting_functions.h,22 :: 		
	CLRF        _cpt+0 
	CLRF        _cpt+1 
;counting_functions.h,23 :: 		
	CLRF        _flagStart+0 
	CLRF        _flagStart+1 
;counting_functions.h,24 :: 		
	CLRF        _prevrb7+0 
	CLRF        _prevrb7+1 
;counting_functions.h,25 :: 		
L_Counting28:
;counting_functions.h,26 :: 		
L_end_Counting:
	RETURN      0
; end of _Counting

_send_data:

;counting_functions.h,29 :: 		
;counting_functions.h,30 :: 		
	MOVLW       119
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,31 :: 		
	MOVLW       13
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,32 :: 		
	MOVLW       10
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,33 :: 		
	CLRF        _i+0 
	CLRF        _i+1 
	CLRF        _i+2 
	CLRF        _i+3 
L_send_data29:
	MOVLW       0
	SUBWF       _i+3, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__send_data101
	MOVLW       0
	SUBWF       _i+2, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__send_data101
	MOVLW       4
	SUBWF       _i+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__send_data101
	MOVLW       0
	SUBWF       _i+0, 0 
L__send_data101:
	BTFSC       STATUS+0, 0 
	GOTO        L_send_data30
;counting_functions.h,34 :: 		
	MOVF        _i+0, 0 
	MOVWF       FARG_UART_send_long_int_d+0 
	MOVF        _i+1, 0 
	MOVWF       FARG_UART_send_long_int_d+1 
	CALL        _UART_send_long_int+0, 0
;counting_functions.h,35 :: 		
	MOVLW       59
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,36 :: 		
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
;counting_functions.h,37 :: 		
	MOVLW       13
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,38 :: 		
	MOVLW       10
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,33 :: 		
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
;counting_functions.h,39 :: 		
	GOTO        L_send_data29
L_send_data30:
;counting_functions.h,40 :: 		
	MOVLW       109
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,41 :: 		
	MOVLW       13
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,42 :: 		
	MOVLW       10
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;counting_functions.h,43 :: 		
L_end_send_data:
	RETURN      0
; end of _send_data

_init_cpt_data:

;counting_functions.h,46 :: 		
;counting_functions.h,47 :: 		
	CLRF        _i+0 
	CLRF        _i+1 
	CLRF        _i+2 
	CLRF        _i+3 
L_init_cpt_data32:
	MOVLW       0
	SUBWF       _i+3, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__init_cpt_data103
	MOVLW       0
	SUBWF       _i+2, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__init_cpt_data103
	MOVLW       4
	SUBWF       _i+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__init_cpt_data103
	MOVLW       0
	SUBWF       _i+0, 0 
L__init_cpt_data103:
	BTFSC       STATUS+0, 0 
	GOTO        L_init_cpt_data33
;counting_functions.h,48 :: 		
	MOVLW       _cpt_data+0
	ADDWF       _i+0, 0 
	MOVWF       FSR1L+0 
	MOVLW       hi_addr(_cpt_data+0)
	ADDWFC      _i+1, 0 
	MOVWF       FSR1L+1 
	CLRF        POSTINC1+0 
;counting_functions.h,47 :: 		
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
;counting_functions.h,49 :: 		
	GOTO        L_init_cpt_data32
L_init_cpt_data33:
;counting_functions.h,50 :: 		
L_end_init_cpt_data:
	RETURN      0
; end of _init_cpt_data

_PORTS_Init:

;init_functions.h,2 :: 		
;init_functions.h,4 :: 		
	CLRF        TRISD+0 
;init_functions.h,5 :: 		
	CLRF        TRISA+0 
;init_functions.h,6 :: 		
	MOVLW       253
	MOVWF       TRISB+0 
;init_functions.h,7 :: 		
	MOVLW       255
	MOVWF       TRISC+0 
;init_functions.h,8 :: 		
	BCF         TRISE+0, 0 
;init_functions.h,9 :: 		
	BCF         TRISE+0, 1 
;init_functions.h,10 :: 		
	BCF         TRISE+0, 2 
;init_functions.h,11 :: 		
	BCF         TRISE+0, 3 
;init_functions.h,12 :: 		
L_end_PORTS_Init:
	RETURN      0
; end of _PORTS_Init

_Interrupt_Init:

;init_functions.h,15 :: 		
;init_functions.h,17 :: 		
	BSF         INTCON2+0, 6 
;init_functions.h,18 :: 		
	MOVLW       192
	IORWF       INTCON+0, 1 
;init_functions.h,19 :: 		
	BSF         INTCON+0, 3 
;init_functions.h,20 :: 		
	BCF         INTCON+0, 0 
;init_functions.h,21 :: 		
	BSF         PIE1+0, 5 
;init_functions.h,22 :: 		
L_end_Interrupt_Init:
	RETURN      0
; end of _Interrupt_Init

_interrupt:

;main.c,53 :: 		void interrupt(void) {
;main.c,58 :: 		if(PIR1.RCIF==1){ // Reception de donn�es pour controler le PIC
	BTFSS       PIR1+0, 5 
	GOTO        L_interrupt35
;main.c,59 :: 		char received_data = RCREG; // Lire les donn�es re�ues
	MOVF        RCREG+0, 0 
	MOVWF       interrupt_received_data_L1+0 
;main.c,60 :: 		PIR1.RCIF = 0; // R�initialiser le drapeau d'interruption de r�ception
	BCF         PIR1+0, 5 
;main.c,61 :: 		if (received_k_factor) {
	MOVF        _received_k_factor+0, 0 
	IORWF       _received_k_factor+1, 0 
	BTFSC       STATUS+0, 2 
	GOTO        L_interrupt36
;main.c,62 :: 		if (received_data >= '0' && received_data <= '9') {
	MOVLW       48
	SUBWF       interrupt_received_data_L1+0, 0 
	BTFSS       STATUS+0, 0 
	GOTO        L_interrupt39
	MOVF        interrupt_received_data_L1+0, 0 
	SUBLW       57
	BTFSS       STATUS+0, 0 
	GOTO        L_interrupt39
L__interrupt84:
;main.c,64 :: 		k = received_data - '0';
	MOVLW       48
	SUBWF       interrupt_received_data_L1+0, 0 
	MOVWF       _k+0 
	CLRF        _k+1 
	MOVLW       0
	SUBWFB      _k+1, 1 
;main.c,65 :: 		}
L_interrupt39:
;main.c,66 :: 		received_k_factor = 0; // R�initialiser apr�s traitement
	CLRF        _received_k_factor+0 
	CLRF        _received_k_factor+1 
;main.c,67 :: 		} else {
	GOTO        L_interrupt40
L_interrupt36:
;main.c,68 :: 		switch(received_data) {
	GOTO        L_interrupt41
;main.c,69 :: 		case 'k':
L_interrupt43:
;main.c,70 :: 		received_k_factor = 1; // On informe le PIC que le prochain caractere sera le facteur k
	MOVLW       1
	MOVWF       _received_k_factor+0 
	MOVLW       0
	MOVWF       _received_k_factor+1 
;main.c,71 :: 		break;
	GOTO        L_interrupt42
;main.c,72 :: 		case 'g':  // Commande GO pour lancer les mesures
L_interrupt44:
;main.c,73 :: 		flagProcess = 1;
	MOVLW       1
	MOVWF       _flagProcess+0 
	MOVLW       0
	MOVWF       _flagProcess+1 
;main.c,74 :: 		break;
	GOTO        L_interrupt42
;main.c,75 :: 		case 's':  // Commande STOP pour arreter les mesures
L_interrupt45:
;main.c,76 :: 		flagProcess = 0;
	CLRF        _flagProcess+0 
	CLRF        _flagProcess+1 
;main.c,77 :: 		break;
	GOTO        L_interrupt42
;main.c,78 :: 		case 'e':  // Commande ERLANG pour selectionner le mode de mesure Erlang
L_interrupt46:
;main.c,79 :: 		mode = 1;
	MOVLW       1
	MOVWF       _mode+0 
	MOVLW       0
	MOVWF       _mode+1 
;main.c,80 :: 		break;
	GOTO        L_interrupt42
;main.c,81 :: 		case 'p':  // Commande POISSON pour selectionner le mode de mesure Poisson
L_interrupt47:
;main.c,82 :: 		mode = 0;
	CLRF        _mode+0 
	CLRF        _mode+1 
;main.c,83 :: 		break;
	GOTO        L_interrupt42
;main.c,84 :: 		default:
L_interrupt48:
;main.c,86 :: 		break;
	GOTO        L_interrupt42
;main.c,87 :: 		}
L_interrupt41:
	MOVF        interrupt_received_data_L1+0, 0 
	XORLW       107
	BTFSC       STATUS+0, 2 
	GOTO        L_interrupt43
	MOVF        interrupt_received_data_L1+0, 0 
	XORLW       103
	BTFSC       STATUS+0, 2 
	GOTO        L_interrupt44
	MOVF        interrupt_received_data_L1+0, 0 
	XORLW       115
	BTFSC       STATUS+0, 2 
	GOTO        L_interrupt45
	MOVF        interrupt_received_data_L1+0, 0 
	XORLW       101
	BTFSC       STATUS+0, 2 
	GOTO        L_interrupt46
	MOVF        interrupt_received_data_L1+0, 0 
	XORLW       112
	BTFSC       STATUS+0, 2 
	GOTO        L_interrupt47
	GOTO        L_interrupt48
L_interrupt42:
;main.c,88 :: 		}
L_interrupt40:
;main.c,89 :: 		}
	GOTO        L_interrupt49
L_interrupt35:
;main.c,91 :: 		if(mode==0){ // Erlang
	MOVLW       0
	XORWF       _mode+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__interrupt108
	MOVLW       0
	XORWF       _mode+0, 0 
L__interrupt108:
	BTFSS       STATUS+0, 2 
	GOTO        L_interrupt50
;main.c,92 :: 		if(prevrb7==0){
	MOVLW       0
	XORWF       _prevrb7+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__interrupt109
	MOVLW       0
	XORWF       _prevrb7+0, 0 
L__interrupt109:
	BTFSS       STATUS+0, 2 
	GOTO        L_interrupt51
;main.c,93 :: 		cpt = 0;      // Initialisation du compteur
	CLRF        _cpt+0 
	CLRF        _cpt+1 
;main.c,94 :: 		cptk = 0;     // Initialisation du compteur d'impulsion
	CLRF        _cptk+0 
	CLRF        _cptk+1 
;main.c,95 :: 		flagStart = 1;// Lancement du compteur
	MOVLW       1
	MOVWF       _flagStart+0 
	MOVLW       0
	MOVWF       _flagStart+1 
;main.c,96 :: 		prevrb7 = 1;  // Sauvegarde de l'etat precedent de RB7
	MOVLW       1
	MOVWF       _prevrb7+0 
	MOVLW       0
	MOVWF       _prevrb7+1 
;main.c,97 :: 		}
	GOTO        L_interrupt52
L_interrupt51:
;main.c,99 :: 		cptk++;
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
;main.c,100 :: 		if(cptk==k){ // Verification du nombre d'impulsion mesurees
	MOVF        _cptk+1, 0 
	XORWF       _k+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__interrupt110
	MOVF        _k+0, 0 
	XORWF       _cptk+0, 0 
L__interrupt110:
	BTFSS       STATUS+0, 2 
	GOTO        L_interrupt53
;main.c,101 :: 		flagStart = 0;      // Arret du compteur
	CLRF        _flagStart+0 
	CLRF        _flagStart+1 
;main.c,102 :: 		prevrb7 = 0;        // Sauvegarde de l'etat precedent du compteur
	CLRF        _prevrb7+0 
	CLRF        _prevrb7+1 
;main.c,103 :: 		cpt_data[cpt]++;    // Sauvegarde de la donnee dans le canal correspondant
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
;main.c,104 :: 		}
L_interrupt53:
;main.c,105 :: 		}
L_interrupt52:
;main.c,106 :: 		if(cpt_data[cpt]==4){  // Lorsqu'une cellule du tableau de donnee atteint sa valeur maximale, on envoie les donnees sur le PC
	MOVLW       _cpt_data+0
	ADDWF       _cpt+0, 0 
	MOVWF       FSR0L+0 
	MOVLW       hi_addr(_cpt_data+0)
	ADDWFC      _cpt+1, 0 
	MOVWF       FSR0L+1 
	MOVF        POSTINC0+0, 0 
	MOVWF       R1 
	MOVF        R1, 0 
	XORLW       4
	BTFSS       STATUS+0, 2 
	GOTO        L_interrupt54
;main.c,107 :: 		INTCON &= 0b00110111; // Desactive les interruptions
	MOVLW       55
	ANDWF       INTCON+0, 1 
;main.c,108 :: 		flagWrite = 1; // On active le flag d'ecriture des donnees
	MOVLW       1
	MOVWF       _flagWrite+0 
	MOVLW       0
	MOVWF       _flagWrite+1 
;main.c,109 :: 		}
L_interrupt54:
;main.c,110 :: 		}
L_interrupt50:
;main.c,112 :: 		if(mode==1){ //Poisson
	MOVLW       0
	XORWF       _mode+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__interrupt111
	MOVLW       1
	XORWF       _mode+0, 0 
L__interrupt111:
	BTFSS       STATUS+0, 2 
	GOTO        L_interrupt55
;main.c,113 :: 		Counting(); // Comptage du nombre d'impulsion sur cpt lors de la detection d'une impulsion
	CALL        _Counting+0, 0
;main.c,114 :: 		}
L_interrupt55:
;main.c,117 :: 		while(PORTB.B7==1); // On attend que l'impulsion se termine pour sortir de l'interruption (necessaire lors de test par appui sur bouton)
L_interrupt56:
	BTFSS       PORTB+0, 7 
	GOTO        L_interrupt57
	GOTO        L_interrupt56
L_interrupt57:
;main.c,118 :: 		INTCON.RBIF = 0; // Reinitialise le flag d'interruption RBIF
	BCF         INTCON+0, 0 
;main.c,119 :: 		}
L_interrupt49:
;main.c,120 :: 		}
L_end_interrupt:
L__interrupt107:
	RETFIE      1
; end of _interrupt

_main:

;main.c,125 :: 		void main() {
;main.c,127 :: 		PORTS_Init();  // On initialise les differents PORTs
	CALL        _PORTS_Init+0, 0
;main.c,128 :: 		ADC_Init(); // On initialise le convertisseur ADC
	CALL        _ADC_Init+0, 0
;main.c,129 :: 		ADCON0 = 0;
	CLRF        ADCON0+0 
;main.c,130 :: 		PORTE.B1 = 0;
	BCF         PORTE+0, 1 
;main.c,131 :: 		PORTE.B2 = 0;
	BCF         PORTE+0, 2 
;main.c,132 :: 		PORTE.B0 = 0;
	BCF         PORTE+0, 0 
;main.c,133 :: 		PORTB.B1 = 0;
	BCF         PORTB+0, 1 
;main.c,136 :: 		UART1_Init(9600); // Configuration de l'UART a une vitesse en Bauds donnee
	BSF         BAUDCON+0, 3, 0
	MOVLW       4
	MOVWF       SPBRGH+0 
	MOVLW       225
	MOVWF       SPBRG+0 
	BSF         TXSTA+0, 2, 0
	CALL        _UART1_Init+0, 0
;main.c,138 :: 		delay_ms(1000); // Attente de la stabilisation de l'UART
	MOVLW       61
	MOVWF       R11, 0
	MOVLW       225
	MOVWF       R12, 0
	MOVLW       63
	MOVWF       R13, 0
L_main58:
	DECFSZ      R13, 1, 1
	BRA         L_main58
	DECFSZ      R12, 1, 1
	BRA         L_main58
	DECFSZ      R11, 1, 1
	BRA         L_main58
	NOP
	NOP
;main.c,139 :: 		init_cpt_data();// Initilisation du tableau de donnees
	CALL        _init_cpt_data+0, 0
;main.c,140 :: 		Interrupt_Init(); // Configuration des registres d'interruption
	CALL        _Interrupt_Init+0, 0
;main.c,141 :: 		INTCON.RBIE=0; // Mais on conserve les interruptions desactivees sur PORTB pour le demarrage
	BCF         INTCON+0, 3 
;main.c,144 :: 		while (exitloop==0){
L_main59:
	MOVLW       0
	XORWF       _exitloop+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__main113
	MOVLW       0
	XORWF       _exitloop+0, 0 
L__main113:
	BTFSS       STATUS+0, 2 
	GOTO        L_main60
;main.c,145 :: 		PORTE.B1 = 1;  // LED1 : A l'arret (Idle)
	BSF         PORTE+0, 1 
;main.c,146 :: 		PORTE.B2 = 0;
	BCF         PORTE+0, 2 
;main.c,147 :: 		PORTE.B0=mode; // LED0 : Indique le mode de fonctionnement (Erlang ou Poisson)
	BTFSC       _mode+0, 0 
	GOTO        L__main114
	BCF         PORTE+0, 0 
	GOTO        L__main115
L__main114:
	BSF         PORTE+0, 0 
L__main115:
;main.c,149 :: 		displayIntSingleDigit(k); // Affichage du k sur le premier digit 7 segments
	MOVF        _k+0, 0 
	MOVWF       FARG_displayIntSingleDigit_nb+0 
	MOVF        _k+1, 0 
	MOVWF       FARG_displayIntSingleDigit_nb+1 
	CALL        _displayIntSingleDigit+0, 0
;main.c,153 :: 		if(PORTC.B2==1){
	BTFSS       PORTC+0, 2 
	GOTO        L_main61
;main.c,154 :: 		if(prevrc2==1){
	MOVLW       0
	XORWF       _prevrc2+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__main116
	MOVLW       1
	XORWF       _prevrc2+0, 0 
L__main116:
	BTFSS       STATUS+0, 2 
	GOTO        L_main62
;main.c,155 :: 		prevrc2=0;
	CLRF        _prevrc2+0 
	CLRF        _prevrc2+1 
;main.c,156 :: 		mode=0;
	CLRF        _mode+0 
	CLRF        _mode+1 
;main.c,157 :: 		}
	GOTO        L_main63
L_main62:
;main.c,159 :: 		prevrc2=1;
	MOVLW       1
	MOVWF       _prevrc2+0 
	MOVLW       0
	MOVWF       _prevrc2+1 
;main.c,160 :: 		mode=1;
	MOVLW       1
	MOVWF       _mode+0 
	MOVLW       0
	MOVWF       _mode+1 
;main.c,161 :: 		}
L_main63:
;main.c,162 :: 		while(PORTC.B2);
L_main64:
	BTFSS       PORTC+0, 2 
	GOTO        L_main65
	GOTO        L_main64
L_main65:
;main.c,163 :: 		}
L_main61:
;main.c,166 :: 		while(flagProcess==1){
L_main66:
	MOVLW       0
	XORWF       _flagProcess+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__main117
	MOVLW       1
	XORWF       _flagProcess+0, 0 
L__main117:
	BTFSS       STATUS+0, 2 
	GOTO        L_main67
;main.c,167 :: 		PORTE.B1=0;
	BCF         PORTE+0, 1 
;main.c,168 :: 		PORTE.B0=mode; // Affichage du mode de mesure
	BTFSC       _mode+0, 0 
	GOTO        L__main118
	BCF         PORTE+0, 0 
	GOTO        L__main119
L__main118:
	BSF         PORTE+0, 0 
L__main119:
;main.c,169 :: 		PORTE.B2=1; // LED2 : En cours d'execution
	BSF         PORTE+0, 2 
;main.c,171 :: 		if(mode==0){ // Erlang
	MOVLW       0
	XORWF       _mode+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__main120
	MOVLW       0
	XORWF       _mode+0, 0 
L__main120:
	BTFSS       STATUS+0, 2 
	GOTO        L_main68
;main.c,172 :: 		if(PORTC.B0==1){
	BTFSS       PORTC+0, 0 
	GOTO        L_main69
;main.c,173 :: 		if(prevrc0==0){
	MOVLW       0
	XORWF       _prevrc0+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__main121
	MOVLW       0
	XORWF       _prevrc0+0, 0 
L__main121:
	BTFSS       STATUS+0, 2 
	GOTO        L_main70
;main.c,174 :: 		Counting(); // Incrementation du compteur
	CALL        _Counting+0, 0
;main.c,175 :: 		prevrc0=1;
	MOVLW       1
	MOVWF       _prevrc0+0 
	MOVLW       0
	MOVWF       _prevrc0+1 
;main.c,176 :: 		}
L_main70:
;main.c,177 :: 		}
	GOTO        L_main71
L_main69:
;main.c,179 :: 		prevrc0=0;  // Sauvegarde du dernier etat de RC0
	CLRF        _prevrc0+0 
	CLRF        _prevrc0+1 
;main.c,180 :: 		}
L_main71:
;main.c,181 :: 		}
L_main68:
;main.c,183 :: 		if(mode==1){ // Poisson
	MOVLW       0
	XORWF       _mode+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__main122
	MOVLW       1
	XORWF       _mode+0, 0 
L__main122:
	BTFSS       STATUS+0, 2 
	GOTO        L_main72
;main.c,184 :: 		flagStart=1;
	MOVLW       1
	MOVWF       _flagStart+0 
	MOVLW       0
	MOVWF       _flagStart+1 
;main.c,185 :: 		if(PORTC.B0==1){
	BTFSS       PORTC+0, 0 
	GOTO        L_main73
;main.c,186 :: 		cpt_data[cpt]++; // Enregistrement sur le canau correspondant au nb d'impulsion mesurees
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
;main.c,187 :: 		cpt=0;          // Reset du compteur
	CLRF        _cpt+0 
	CLRF        _cpt+1 
;main.c,188 :: 		while(PORTC.B0); // On attend que le niveau haut d'horloge se termine
L_main74:
	BTFSS       PORTC+0, 0 
	GOTO        L_main75
	GOTO        L_main74
L_main75:
;main.c,189 :: 		}
L_main73:
;main.c,191 :: 		if(cpt_data[cpt]==255){  // Lorsqu'une cellule du tableau de donnee atteint sa valeur maximale, on envoie les donnees sur le PC
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
	GOTO        L_main76
;main.c,192 :: 		INTCON &= 0b00110111; // Desactive toutes les interruptions pour l'ecriture
	MOVLW       55
	ANDWF       INTCON+0, 1 
;main.c,193 :: 		flagWrite = 1; // On active le flag d'ecriture des donnees
	MOVLW       1
	MOVWF       _flagWrite+0 
	MOVLW       0
	MOVWF       _flagWrite+1 
;main.c,194 :: 		}
L_main76:
;main.c,195 :: 		}
L_main72:
;main.c,199 :: 		if(flagWrite==1){ // Pour l'envoie des donnees
	MOVLW       0
	XORWF       _flagWrite+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__main123
	MOVLW       1
	XORWF       _flagWrite+0, 0 
L__main123:
	BTFSS       STATUS+0, 2 
	GOTO        L_main77
;main.c,200 :: 		send_data(); // Envoie les donnees vers le terminal
	CALL        _send_data+0, 0
;main.c,201 :: 		init_cpt_data();
	CALL        _init_cpt_data+0, 0
;main.c,202 :: 		flagWrite=0;
	CLRF        _flagWrite+0 
	CLRF        _flagWrite+1 
;main.c,203 :: 		INTCON |= 0b11001000; // Reactive toutes les interruptions
	MOVLW       200
	IORWF       INTCON+0, 1 
;main.c,204 :: 		}
L_main77:
;main.c,206 :: 		while(PORTC.B1==1){ // Met en pause les mesures lors de l'appui sur le bouton RC1
L_main78:
	BTFSS       PORTC+0, 1 
	GOTO        L_main79
;main.c,207 :: 		if(prevrc1==0){
	MOVLW       0
	XORWF       _prevrc1+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__main124
	MOVLW       0
	XORWF       _prevrc1+0, 0 
L__main124:
	BTFSS       STATUS+0, 2 
	GOTO        L_main80
;main.c,208 :: 		INTCON.RBIE=0; // Desactive les interruptions sur PORTB
	BCF         INTCON+0, 3 
;main.c,209 :: 		flagProcess = 0;    // Met a jour le flag de sortie de boucle
	CLRF        _flagProcess+0 
	CLRF        _flagProcess+1 
;main.c,210 :: 		prevrc1=1;          // Sauvegarde du dernier etat de RC1
	MOVLW       1
	MOVWF       _prevrc1+0 
	MOVLW       0
	MOVWF       _prevrc1+1 
;main.c,211 :: 		UART_Write('i'); // On envoie une commande indiquant l'etat "Idle" a l'app
	MOVLW       105
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;main.c,212 :: 		UART_Write(0x0D);
	MOVLW       13
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;main.c,213 :: 		UART_Write(0x0A);
	MOVLW       10
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;main.c,214 :: 		}
L_main80:
;main.c,215 :: 		}
	GOTO        L_main78
L_main79:
;main.c,216 :: 		}
	GOTO        L_main66
L_main67:
;main.c,220 :: 		while(PORTC.B1==1){
L_main81:
	BTFSS       PORTC+0, 1 
	GOTO        L_main82
;main.c,221 :: 		if(prevrc1==1){
	MOVLW       0
	XORWF       _prevrc1+1, 0 
	BTFSS       STATUS+0, 2 
	GOTO        L__main125
	MOVLW       1
	XORWF       _prevrc1+0, 0 
L__main125:
	BTFSS       STATUS+0, 2 
	GOTO        L_main83
;main.c,222 :: 		UART_Write('m'); // On envoie une commande indiquant l'etat "Measuring" a l'app
	MOVLW       109
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;main.c,223 :: 		UART_Write(0x0D);
	MOVLW       13
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;main.c,224 :: 		UART_Write(0x0A);
	MOVLW       10
	MOVWF       FARG_UART_Write__data+0 
	CALL        _UART_Write+0, 0
;main.c,225 :: 		cpt=0;           // On initialise le compteur
	CLRF        _cpt+0 
	CLRF        _cpt+1 
;main.c,226 :: 		init_cpt_data(); // Et on initialise le tableau de donnees avant lancement
	CALL        _init_cpt_data+0, 0
;main.c,227 :: 		flagProcess = 1;    // Met a jour le flag de sortie de boucle
	MOVLW       1
	MOVWF       _flagProcess+0 
	MOVLW       0
	MOVWF       _flagProcess+1 
;main.c,228 :: 		prevrc1=0;          // Sauvegarde du dernier etat de RC1
	CLRF        _prevrc1+0 
	CLRF        _prevrc1+1 
;main.c,229 :: 		INTCON.RBIE=1; // Active les interruptions sur PORTB en dernier
	BSF         INTCON+0, 3 
;main.c,230 :: 		}
L_main83:
;main.c,231 :: 		}
	GOTO        L_main81
L_main82:
;main.c,232 :: 		}
	GOTO        L_main59
L_main60:
;main.c,233 :: 		}
L_end_main:
	GOTO        $+0
; end of _main
