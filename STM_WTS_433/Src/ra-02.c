
#include "ra-02.h"


SX1278_hw_t SX1278_hw;
SX1278_t SX1278;
char buffer[64];

int RA02_init(){

	//initialize LoRa module
	SX1278_hw.dio0.port = DIO0_GPIO_Port;
	SX1278_hw.dio0.pin = DIO0_Pin;
	SX1278_hw.nss.port = NSS_GPIO_Port;
	SX1278_hw.nss.pin = NSS_Pin;
	SX1278_hw.reset.port = RESET_GPIO_Port;
	SX1278_hw.reset.pin = RESET_Pin;
	SX1278_hw.spi = &hspi1;

	SX1278.hw = &SX1278_hw;
	
	SX1278_begin(&SX1278, SX1278_433MHZ, SX1278_POWER_17DBM, SX1278_LORA_SF_8,SX1278_LORA_BW_20_8KHZ, 10);
	ret = SX1278_LoRaEntryTx(&SX1278, 16, 2000);

}

void RA02_TX_Mode(uint8_t *pBuf) {
}
void RA02_RX_Mode(void) {
}
void RA02_IRQ_Callback(void){	
	unsigned char addr;
	unsigned char packet_size;

	
		memset(SX1278.rxBuffer, 0x00, SX1278_MAX_PACKET);

		addr = SX1278_SPIRead(&SX1278, LR_RegFifoRxCurrentaddr); //last packet addr
		SX1278_SPIWrite(&SX1278, LR_RegFifoAddrPtr, addr); //RxBaseAddr -> FiFoAddrPtr

		if (SX1278.LoRa_Rate == SX1278_LORA_SF_6) { //When SpreadFactor is six,will used Implicit Header mode(Excluding internal packet length)
			packet_size = SX1278.packetLength;
		} else {
			packet_size = SX1278_SPIRead(&SX1278, LR_RegRxNbBytes); //Number for received bytes
		}

		SX1278_SPIBurstRead(&SX1278, 0x00, SX1278.rxBuffer, packet_size);
		SX1278.readBytes = packet_size;
		SX1278_clearLoRaIrq(&SX1278);
	
	return SX1278.readBytes;
	
}