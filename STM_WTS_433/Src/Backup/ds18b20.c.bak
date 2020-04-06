/*
 * ds18b20.c
 *
 *  Created on: 30 но€б. 2018 г.
 *      Author: a.spitsyn
 */

#include "ds18b20.h"
//#include "usart.h"

//#define putsUSART(x)	HAL_UART_Transmit(&huart1, (uint8_t*)x, strlen(x), 0xFFFF);

uint8_t DS_SCRATCHPAD[8];
int8_t DS_TEMP = 0;
GPIO_InitTypeDef GPIO_DS18B20;


//--------------------------------------------------
__STATIC_INLINE void DelayMicro(__IO uint32_t micros) {
	micros *= (SystemCoreClock / 1000000) / 9;
	/* Wait till done */
	while (micros--);
}
//--------------------------------------------------
void port_init(void) {
	HAL_GPIO_DeInit(GPIOB, DS_PIN);
	GPIOB->CRH |= GPIO_CRH_MODE9;
	GPIOB->CRH |= GPIO_CRH_CNF9_0;
	GPIOB->CRH &= ~GPIO_CRH_CNF9_1;

}
//--------------------------------------------------
uint8_t ds18b20_Reset(void) {
	uint16_t status;

	GPIOB->ODR &= ~GPIO_ODR_ODR9;
	DelayMicro(485);
	GPIOB->ODR |= GPIO_ODR_ODR9;
	DelayMicro(65);
	status = GPIOB->IDR & GPIO_IDR_IDR9;
	DelayMicro(500);

	return (status ? 1 : 0);
	
	// 1 - FAIL
	// 0 - OK
}
//----------------------------------------------------------
uint8_t ds18b20_ReadBit(void) {
	uint8_t bit = 0;

	GPIOB->ODR &= ~GPIO_ODR_ODR9;
	DelayMicro(2);
	GPIOB->ODR |= GPIO_ODR_ODR9;
	DelayMicro(13);
	bit = (GPIOB->IDR & GPIO_IDR_IDR9 ? 1 : 0);

	DelayMicro(45);
	return bit;
}
//-----------------------------------------------
uint8_t ds18b20_ReadByte(void) {
	uint8_t data = 0;
	uint8_t i=0;
	uint8_t s[16];
	
	for (i = 0; i <= 7; i++){
		data += ds18b20_ReadBit() << i;
	}
	return data;
}
//-----------------------------------------------
void ds18b20_WriteBit(uint8_t bit) {

	GPIOB->ODR &= ~GPIO_ODR_ODR9;
	DelayMicro(bit ? 3 : 65);
	GPIOB->ODR |= GPIO_ODR_ODR9;
	DelayMicro(bit ? 65 : 3);

}
//-----------------------------------------------
void ds18b20_WriteByte(uint8_t dt) {
	for (uint8_t i = 0; i < 8; i++) {		
		ds18b20_WriteBit(dt >> i & 1);
		//Delay Protection
		DelayMicro(5);
	}
}
//-----------------------------------------------
uint8_t ds18b20_Init(uint8_t resolution_bit) {
	port_init();
	DelayMicro(250);
	if (ds18b20_Reset()){
		return 1; //FAIL DS18B20 NOT FOUND
	}

	//SKIP ROM
	ds18b20_WriteByte(0xCC);
	//WRITE SCRATCHPAD
	ds18b20_WriteByte(0x4E);
	//TH REGISTER 100
	ds18b20_WriteByte(0x64);
	//TL REGISTER - 30
	ds18b20_WriteByte(0x9E);
	//Resolution 12 bit
	ds18b20_WriteByte(resolution_bit);

	return 0;
}
//----------------------------------------------------------
uint8_t ds18b20_MeasureTemperCmd(void) {
	if (ds18b20_Reset()){
		return 1;
	}

	//SKIP ROM
	ds18b20_WriteByte(0xCC);

	ds18b20_WriteByte(0x44);

	return 0;
}
//----------------------------------------------------------
uint8_t ds18b20_ReadStratcpad(void) {
	uint8_t i;
	
	if (ds18b20_Reset()){
		return 1;
	}

	//SKIP ROM
	ds18b20_WriteByte(0xCC);

	//READ SCRATCHPAD
	ds18b20_WriteByte(0xBE);


	for (i = 0; i < 8; i++) {
		DS_SCRATCHPAD[i] = ds18b20_ReadByte();
	}
	return 0;
}

//----------------------------------------------------------
void ds18b20_Convert_int8(void) {

	DS_TEMP = (DS_SCRATCHPAD[1] << 4) | (DS_SCRATCHPAD[0] >> 4);

}
//----------------------------------------------------------

uint8_t ds18b20_GetTemp(void) {

	if(ds18b20_MeasureTemperCmd()){
		return 1;
	}
	//putsUSART("ds18b20 mes temp delay\r\n");
	HAL_Delay(150);// 9bit resolution
//	HAL_Delay(250);// 10bit resolution
//	HAL_Delay(425);// 11bit resolution
	//HAL_Delay(800);// 12bit resolution

	if(ds18b20_ReadStratcpad()){
		return 2;
	}

	ds18b20_Convert_int8();

	return 0;
}
