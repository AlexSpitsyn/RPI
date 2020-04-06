
#include "SX1278.h"
#include <string.h>
#include "usart.h"
#include "gpio.h"
#include "spi.h"	
#include <stdio.h>

SX1278_t SX1278;
//char buffer[64];
char dbg_str[64];
uint8_t dt_reg;

uint8_t SX1278_DBG_PRINT_F=0;



#define dbg_print(s) putsUSART(s)

__STATIC_INLINE void DelayMicro(__IO uint32_t micros) {

	micros *= (SystemCoreClock / 1000000) / 9;

	/* Wait till done */

	while (micros--)
		;

}

void SX1278_init(uint8_t POWER,	uint8_t SF, uint8_t BW, uint8_t CR ,uint8_t packetLength) {
	SX1278_NSS_SET; 	
	SX1278_reset();

	//SX1278.frequency = frequency;
	SX1278.POWER = POWER;
	SX1278.SF = SF;
	SX1278.BW = BW;
	SX1278.CR = CR;
	SX1278.packetLength = packetLength;
	SX1278_defaultConfig();

}

void SX1278_reset(void) {
	SX1278_NSS_SET;
	HAL_GPIO_WritePin(RESET_Port, RESET_Pin, GPIO_PIN_RESET);
	
	HAL_Delay(1);
	HAL_GPIO_WritePin(RESET_Port, RESET_Pin, GPIO_PIN_SET);
	HAL_Delay(100);
	
}

uint8_t SX1278_SPIReadReg(uint8_t addr) {
	uint8_t txByte = 0x00;
	uint8_t rxByte = 0x00;
	
	SX1278_NSS_RESET;
	HAL_SPI_Transmit(SX1278_SPI_PORT, &addr, 1, 1000);
	HAL_SPI_TransmitReceive(SX1278_SPI_PORT, &txByte, &rxByte, 1, 1000);
	SX1278_NSS_SET;
	return rxByte;
}

void SX1278_SPIWriteReg(uint8_t addr, uint8_t cmd) {
	addr |= 0x80;
	
	SX1278_NSS_RESET;
	HAL_SPI_Transmit(SX1278_SPI_PORT, &addr, 1, 1000);
	HAL_SPI_Transmit(SX1278_SPI_PORT, &cmd, 1, 1000);
	SX1278_NSS_SET;
}

void SX1278_SPIBurstRead(uint8_t addr, uint8_t* rxBuf, uint8_t length) {	
	if (length <= 1) {
		return;
	} else {
		SX1278_NSS_RESET;
		HAL_SPI_Transmit(SX1278_SPI_PORT, &addr, 1, 1000);		
		HAL_SPI_Receive(SX1278_SPI_PORT, rxBuf, length, 1000);
		SX1278_NSS_SET;
		
	}
}

void SX1278_SPIBurstWrite(uint8_t addr, uint8_t* txBuf, uint8_t length) {
	addr |= 0x80;
	
	if (length <= 1) {
		return;
	} else {
		SX1278_NSS_RESET;
		HAL_SPI_Transmit(SX1278_SPI_PORT, &addr, 1, 1000);
		DelayMicro(1);
		HAL_SPI_Transmit(SX1278_SPI_PORT, txBuf, length, 1000);		
		SX1278_NSS_SET;
	}
}

void SX1278_defaultConfig(void) {
	
	SX1278_config(SX1278.POWER, SX1278.SF, SX1278.BW, SX1278.CR);
}

void SX1278_config(uint8_t POWER, uint8_t SF, uint8_t BW, uint8_t CR) {
	SX1278_sleep(); //Change modem mode Must in Sleep mode
	HAL_Delay(15);

	SX1278_entryLoRa();
	//SX1278_SPIWrite(module, 0x5904); //?? Change digital regulator form 1.6V to 1.47V: see errata note

	SX1278_SPIBurstWrite(LR_RegFrMsb,(uint8_t*) SX1278_Frequency[SX1278_433MHZ], 3); //setting  frequency parameter

	//setting base parameter
	SX1278_SPIWriteReg(LR_RegPaConfig, SX1278_Power[POWER]); //Setting output power parameter

	SX1278_SPIWriteReg(LR_RegOcp, 0x0B);			//RegOcp,Close Ocp
	SX1278_SPIWriteReg(LR_RegLna, 0x23);		//RegLNA,High & LNA Enable
	if (SX1278_SpreadFactor[SF] == 6) {	//SFactor=6
		uint8_t tmp;
		SX1278_SPIWriteReg(LR_RegModemConfig1,((SX1278_LoRaBandwidth[BW] << 4) + (CR << 1) + 0x01)); 
		//Implicit Enable CRC Enable(0x02) & Error Coding rate 4/5(0x01), 4/6(0x02), 4/7(0x03), 4/8(0x04)

		SX1278_SPIWriteReg(LR_RegModemConfig2,((SX1278_SpreadFactor[SF] << 4) + (SX1278_CRC << 2)+ 0x03));

		tmp = SX1278_SPIReadReg(0x31);
		tmp &= 0xF8;
		tmp |= 0x05;
		SX1278_SPIWriteReg(0x31, tmp);
		SX1278_SPIWriteReg(0x37, 0x0C);
	} else {
		SX1278_SPIWriteReg(LR_RegModemConfig1,((SX1278_LoRaBandwidth[BW] << 4) + (CR << 1) + 0x00)); 
		//Explicit Enable CRC Enable(0x02) & Error Coding rate 4/5(0x01), 4/6(0x02), 4/7(0x03), 4/8(0x04)

		SX1278_SPIWriteReg(LR_RegModemConfig2,((SX1278_SpreadFactor[SF] << 4) + (SX1278_CRC << 2) + 0x03)); 
		//SFactor &  LNA gain set by the internal AGC loop
	}

	SX1278_SPIWriteReg(LR_RegSymbTimeoutLsb, 0xFF); //RegSymbTimeoutLsb Timeout = 0x3FF(Max)
	SX1278_SPIWriteReg(LR_RegPreambleMsb, 0x00); //RegPreambleMsb
	SX1278_SPIWriteReg(LR_RegPreambleLsb, 12); //RegPreambleLsb 8+4=12byte Preamble
	SX1278_SPIWriteReg(REG_LR_DIOMAPPING2, 0x01); //RegDioMapping2 DIO5=00, DIO4=01
	SX1278.readBytes = 0;
	SX1278_standby(); //Entry standby mode
	if(SX1278_DBG_PRINT_F){
		SX1278_Get_State();
	}
}

void SX1278_standby(void) {
	SX1278_SPIWriteReg(LR_RegOpMode, 0x09);
	SX1278.status = STANDBY;
}

void SX1278_sleep(void) {
	SX1278_SPIWriteReg(LR_RegOpMode, 0x08);
	SX1278.status = SLEEP;
}

void SX1278_entryLoRa(void) {
	SX1278_SPIWriteReg(LR_RegOpMode, 0x88);
}

void SX1278_clearIrq(void) {
	SX1278_SPIWriteReg(LR_RegIrqFlags, 0xFF);
}

int SX1278_LoRaEntryRx(uint8_t length, uint32_t timeout) {
	uint8_t addr;

	SX1278.packetLength = length;

	SX1278_defaultConfig();		//Setting base parameter
	SX1278_SPIWriteReg(REG_LR_PADAC, 0x84);	//Normal and RX
	SX1278_SPIWriteReg(LR_RegHopPeriod, 0xFF);	//No FHSS
	SX1278_SPIWriteReg(REG_LR_DIOMAPPING1, 0x01);//DIO=00,DIO1=00,DIO2=00, DIO3=01
	SX1278_SPIWriteReg(LR_RegIrqFlagsMask, 0x3F);//Open RxDone interrupt & Timeout
	SX1278_clearIrq();
	SX1278_SPIWriteReg(LR_RegPayloadLength, length);//Payload Length 21byte(this register must difine when the data long of one byte in SF is 6)
	addr = SX1278_SPIReadReg(LR_RegFifoRxBaseAddr); //Read RxBaseAddr
	SX1278_SPIWriteReg(LR_RegFifoAddrPtr, addr); //RxBaseAddr->FiFoAddrPtr
	SX1278_SPIWriteReg(LR_RegOpMode, 0x8d);	//Mode//Low Frequency Mode
	//SX1278_SPIWrite(LR_RegOpMode,0x05);	//Continuous Rx Mode //High Frequency Mode
	SX1278.readBytes = 0;

	while (1) {
		if ((SX1278_SPIReadReg(LR_RegModemStat) & 0x04) == 0x04) {	//Rx-on going RegModemStat
			SX1278.status = RX;
			return 1;
		}
		if (--timeout == 0) {
			SX1278_reset();
			SX1278_defaultConfig();
			return 0;
		}
		HAL_Delay(1);
	}
}

uint8_t SX1278_LoRaRxPacket(void) {
	unsigned char addr;
	unsigned char packet_size;

	if (HAL_GPIO_ReadPin(DIO0_Port, DIO0_Pin)) {
		memset(SX1278.rxBuffer, 0x00, SX1278_MAX_PACKET);

		addr = SX1278_SPIReadReg(LR_RegFifoRxCurrentaddr); //last packet addr
		SX1278_SPIWriteReg(LR_RegFifoAddrPtr, addr); //RxBaseAddr -> FiFoAddrPtr

		if (SX1278.SF == SX1278_LORA_SF_6) { //When SpreadFactor is six,will used Implicit Header mode(Excluding internal packet length)
			packet_size = SX1278.packetLength;
		} else {
			packet_size = SX1278_SPIReadReg(LR_RegRxNbBytes); //Number for received bytes
		}

		SX1278_SPIBurstRead(0x00, SX1278.rxBuffer, packet_size);
		SX1278.readBytes = packet_size;
		SX1278_clearIrq();
	}
	return SX1278.readBytes;
}

int SX1278_LoRaEntryTx(uint8_t length, uint32_t timeout) {
	uint8_t addr;
	uint8_t temp;

	SX1278.packetLength = length;

	SX1278_defaultConfig(); //setting base parameter
	SX1278_SPIWriteReg(REG_LR_PADAC, 0x87);	//Tx for 20dBm
	SX1278_SPIWriteReg(LR_RegHopPeriod, 0x00); //RegHopPeriod NO FHSS
	SX1278_SPIWriteReg(REG_LR_DIOMAPPING1, 0x41); //DIO0=01, DIO1=00,DIO2=00, DIO3=01
	SX1278_clearIrq();
	SX1278_SPIWriteReg(LR_RegIrqFlagsMask, 0xF7); //Open TxDone interrupt
	SX1278_SPIWriteReg(LR_RegPayloadLength, length); //RegPayloadLength 21byte
	addr = SX1278_SPIReadReg(LR_RegFifoTxBaseAddr); //RegFiFoTxBaseAddr
	SX1278_SPIWriteReg(LR_RegFifoAddrPtr, addr); //RegFifoAddrPtr

	while (1) {
		temp = SX1278_SPIReadReg( LR_RegPayloadLength);
		if (temp == length) {
			SX1278.status = TX;
			return 1;
		}

		if (--timeout == 0) {
			SX1278_reset();
			SX1278_defaultConfig();
			return 0;
		}
	}
}

int SX1278_LoRaTxPacket(uint8_t* txBuffer, uint8_t length, uint32_t timeout) {
	SX1278_SPIBurstWrite(0x00, txBuffer, length);
	SX1278_SPIWriteReg(LR_RegOpMode, 0x8b);	//Tx Mode
	while (1) {
		
		if(SX1278.tx_complete_f){
			SX1278.tx_complete_f=0;
			SX1278_standby();
			return 1;
		}
		
//		if (HAL_GPIO_ReadPin(DIO0_Port, DIO0_Pin)) { //if(Get_NIRQ()) //Packet send over
//			SX1278_SPIReadReg(LR_RegIrqFlags);
//			SX1278_clearIrq(); //Clear irq
//			SX1278_standby(); //Entry Standby mode
//			return 1;
//		}

		if (--timeout == 0) {
			SX1278_reset();
			SX1278_defaultConfig();
			return 0;
		}
		HAL_Delay(1);
	}
}


int SX1278_transmit(uint8_t* txBuf, uint8_t length, uint32_t timeout) {
	if (SX1278_LoRaEntryTx(length, timeout)) {
		return SX1278_LoRaTxPacket(txBuf, length, timeout);
	}
	return 0;
}

int SX1278_receive(uint8_t length, uint32_t timeout) {
	return SX1278_LoRaEntryRx(length, timeout);
}

uint8_t SX1278_available(void) {
	return SX1278_LoRaRxPacket();
}

uint8_t SX1278_readFIFO() {
	unsigned char addr;
	unsigned char packet_size;

	
		memset(SX1278.rxBuffer, 0x00, SX1278_MAX_PACKET);

		addr = SX1278_SPIReadReg(LR_RegFifoRxCurrentaddr); //last packet addr
		SX1278_SPIWriteReg(LR_RegFifoAddrPtr, addr); //RxBaseAddr -> FiFoAddrPtr

		if (SX1278.SF == SX1278_LORA_SF_6) { //When SpreadFactor is six,will used Implicit Header mode(Excluding internal packet length)
			packet_size = SX1278.packetLength;
		} else {
			packet_size = SX1278_SPIReadReg(LR_RegRxNbBytes); //Number for received bytes
		}

		SX1278_SPIBurstRead(0x00, SX1278.rxBuffer, packet_size);
		SX1278.readBytes = packet_size;
		return SX1278.readBytes;
}

uint8_t SX1278_RSSI_LoRa(void) {
	uint32_t temp = 10;
	temp = SX1278_SPIReadReg(LR_RegRssiValue); //Read RegRssiValue, Rssi value
	temp = temp + 127 - 137; //127:Max RSSI, 137:RSSI offset
	return (uint8_t) temp;
}

uint8_t SX1278_RSSI(void) {
	uint8_t temp = 0xff;
	temp = SX1278_SPIReadReg(0x11);
	temp = 127 - (temp >> 1);	//127:Max RSSI
	return temp;
}

void SX1278_Send(uint8_t *pBuf) {
	SX1278_transmit(pBuf, strlen((char*)pBuf), 1000);
}

void SX1278_RX_Mode(void) {
	SX1278_SPIWriteReg(REG_LR_DIOMAPPING1, 0x01);//DIO=00,DIO1=00,DIO2=00, DIO3=01
	SX1278_SPIWriteReg(LR_RegIrqFlagsMask, 0x3F);//Open RxDone interrupt & Timeout
	SX1278_clearIrq();
	SX1278_SPIWriteReg(LR_RegOpMode, 0x8d);	//Mode//Low Frequency Mode
}


void SX1278_IRQ_Callback(void) {
//0x01	CAD Detected
//0x02	FHSS change channel
//0x04	CAD complete
//0x08	FIFO Payload transmission complete
//0x10	Valid header received in Rx	
//0x20	Payload CRC error interrupt
//0x40	Packet reception complete
//0x80	Timeout interrupt
	
	uint8_t tmp;
	uint8_t irq_status = 0;
	irq_status=SX1278_SPIReadReg(LR_RegIrqFlags);
	if(SX1278_DBG_PRINT_F){
			sprintf(dbg_str, "\r\nIRQ reg: 0x%02X\r\n", irq_status);
			dbg_print(dbg_str);			
	}
	if(irq_status & 0x08){
		SX1278.tx_complete_f=1;
		if(SX1278_DBG_PRINT_F){
			dbg_print("\r\nIRQ: TX COMPL\r\n");
		}
	}
	if(irq_status & 0x40){
		
		SX1278.receive_f=1;
		tmp = SX1278_readFIFO();
		if(SX1278_DBG_PRINT_F){
			sprintf(dbg_str, "\r\nIRQ: RECEIVE %d bytes\r\n", tmp);
			dbg_print(dbg_str);	
		}
	}
	if(irq_status & 0x80){
		SX1278.timeout_f=1;
		if(SX1278_DBG_PRINT_F){
			dbg_print("\r\nIRQ: TIMEOUT\r\n");
		}
	}
	SX1278_clearIrq();
}

void SX1278_Get_State(void){
	dbg_print("SX1278 STATE:\r\n");
	
		dt_reg = SX1278_SPIReadReg(LR_RegIrqFlagsMask);
		sprintf(dbg_str, "RegIrqFlagsMask: 0x%02X\r\n", dt_reg);
		dbg_print(dbg_str);
	
		dt_reg = SX1278_SPIReadReg(LR_RegIrqFlags);
		sprintf(dbg_str, "RegIrqFlags: 0x%02X\r\n", dt_reg);
		dbg_print(dbg_str);
	
		dt_reg = SX1278_SPIReadReg(LR_RegOpMode);
		sprintf(dbg_str, "RegOpMode: 0x%02X\r\n", dt_reg);
		dbg_print(dbg_str);
		
		dt_reg = SX1278_SPIReadReg(LR_RegFrMsb);
		sprintf(dbg_str, "RegFrMsb: 0x%02X\r\n", dt_reg);
		dbg_print(dbg_str);
		
		dt_reg = SX1278_SPIReadReg(LR_RegPaConfig);
		sprintf(dbg_str, "RegPaConfig: 0x%02X\r\n", dt_reg);
		dbg_print(dbg_str);
		
		dt_reg = SX1278_SPIReadReg(LR_RegModemConfig1);
		sprintf(dbg_str, "RegModemConfig1: 0x%02X\r\n", dt_reg);
		dbg_print(dbg_str);
		
		dt_reg = SX1278_SPIReadReg(LR_RegModemConfig2);
		sprintf(dbg_str, "RegModemConfig2: 0x%02X\r\n", dt_reg);
		dbg_print(dbg_str);
		
		
		sprintf(dbg_str, "SF: %d\r\n", SX1278_SpreadFactor[SX1278.SF]);
		dbg_print(dbg_str);

		sprintf(dbg_str, "BW: %s\r\n", SX1278_LoRaBandwidth_s[SX1278.BW]);
		dbg_print(dbg_str);
		
		sprintf(dbg_str, "CR: %s\r\n", SX1278_CR_s[SX1278.CR-1]);
		dbg_print(dbg_str);
		
		sprintf(dbg_str, "POWER: %s\r\n", SX1278_Power_s[SX1278.POWER]);
		dbg_print(dbg_str);
}



