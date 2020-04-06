/*
 * ds18b20.h
 *
 *  Created on: 30 но€б. 2018 г.
 *      Author: a.spitsyn
 */

#ifndef DS18B20_H_
#define DS18B20_H_

//--------------------------------------------------
#include "stm32f1xx_hal.h"

#include <string.h>
#include <stdlib.h>
#include <stdint.h>
//--------------------------------------------------
#define DS_PORT 	GPIOB
#define DS_PIN		GPIO_PIN_9

extern uint8_t DS_SCRATCHPAD[8];
extern int8_t DS_TEMP;

//--------------------------------------------------
#define SKIP_ROM 0
#define NO_SKIP_ROM 1
//--------------------------------------------------
#define RESOLUTION_9BIT 0x1F
#define RESOLUTION_10BIT 0x3F
#define RESOLUTION_11BIT 0x5F
#define RESOLUTION_12BIT 0x7F
//--------------------------------------------------
uint8_t ds18b20_Reset(void) ;
uint8_t ds18b20_Init(uint8_t resolution_bit);
uint8_t ds18b20_GetTemp(void);
//void ds18b20_MeasureTemperCmd(void);
//void ds18b20_ReadStratcpad(void);
//void ds18b20_Convert_int8_t(void);
//--------------------------------------------------

#endif /* DS18B20_H_ */

