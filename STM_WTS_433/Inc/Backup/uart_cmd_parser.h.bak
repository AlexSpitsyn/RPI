
#ifndef UART_CMD_PARSER_H
#define	UART_CMD_PARSER_H

#include "stm32f1xx_hal.h"
#include "usbd_cdc_if.h"
//#define BUFFER_SIZE 64

//unsigned char msg_flag;
//unsigned char msg_len;




//#define putsUSART(x)	HAL_UART_Transmit(&huart1, (uint8_t*)x, strlen(x), 0xFFFF);
//#define putsUSART(x)	CDC_Transmit_FS( (uint8_t*)x, strlen(x));

void uartInit(void);

void parseCommand(char *buf);

uint8_t str_to_int32(char* str, char** end, uint8_t str_format, uint32_t* val, uint32_t vmin, uint32_t vmax);

#endif	/* CMAD_PARSER_H */

