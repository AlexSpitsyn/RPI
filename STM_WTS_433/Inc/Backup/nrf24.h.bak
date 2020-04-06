#ifndef NRF24_H_

#define NRF24_H_

//------------------------------------------------

#include "stm32f1xx_hal.h"
#include "spi.h"

#include <string.h>

//------------------------------------------------

//#define NRF24_SPI_HW_NSS
//------------------------------------------------
//extern SPI_HandleTypeDef hspi1;




#define NRF_SPI_PORT &hspi1

#ifndef NRF24_SPI_HW_NSS
//#define CS_GPIO_PORT CS1_GPIO_Port
//#define CS_PIN CS1_Pin
#define CS_GPIO_PORT GPIOA
#define CS_PIN GPIO_PIN_4

#endif

#define CE_GPIO_PORT CE_GPIO_Port
#define CE_PIN CE_Pin
#define IRQ_GPIO_PORT IRQ_GPIO_Port
#define IRQ_PIN IRQ_Pin





//------------------------------------------------

#ifndef NRF24_SPI_HW_NSS
#define CS_ON HAL_GPIO_WritePin(CS_GPIO_PORT, CS_PIN, GPIO_PIN_RESET)

#define CS_OFF HAL_GPIO_WritePin(CS_GPIO_PORT, CS_PIN, GPIO_PIN_SET)
#else
#define CS_ON 

#define CS_OFF 
#endif

#define CE_RESET HAL_GPIO_WritePin(CE_GPIO_PORT, CE_PIN, GPIO_PIN_RESET)

#define CE_SET HAL_GPIO_WritePin(CE_GPIO_PORT, CE_PIN, GPIO_PIN_SET)


#define IRQ HAL_GPIO_ReadPin(IRQ_GPIO_PORT, IRQ_PIN)


//------------------------------------------------

#define ACTIVATE 0x50 //

#define RD_RX_PLOAD 0x61 // Define RX payload register address

#define WR_TX_PLOAD 0xA0 // Define TX payload register address

#define FLUSH_TX 0xE1

#define FLUSH_RX 0xE2

//------------------------------------------------

#define CONFIG 0x00 //'Config' register address
//MASK_RX_DR 	6 
//MASK_TX_DS 	5 
//MASK_MAX_RT 4 
//EN_CRC 			3 
//CRCO 				2 
//PWR_UP 			1 
//PRIM_RX 		0 RX/TX mode (1/0)

#define EN_AA 0x01 //'Enable Auto Acknowledgment' register address

#define EN_RXADDR 0x02 //'Enabled RX addresses' register address

#define SETUP_AW 0x03 //'Setup address width' register address

#define SETUP_RETR 0x04 //'Setup Auto. Retrans' register address

#define RF_CH 0x05 //'RF channel' register address

#define RF_SETUP 0x06 //'RF setup' register address

#define STATUS 0x07 //'Status' register address

#define RX_ADDR_P0 0x0A //'RX address pipe0' register address

#define RX_ADDR_P1 0x0B //'RX address pipe1' register address

#define RX_ADDR_P2 0x0C //'RX address pipe2' register address

#define RX_ADDR_P3 0x0D //'RX address pipe3' register address

#define RX_ADDR_P4 0x0E //'RX address pipe4' register address

#define RX_ADDR_P5 0x0F //'RX address pipe5' register address

#define TX_ADDR 0x10 //'TX address' register address

#define RX_PW_P0 0x11 //'RX payload width, pipe0' register address

#define RX_PW_P1 0x12 //'RX payload width, pipe1' register address

#define RX_PW_P2 0x13 //'RX payload width, pipe2' register address

#define RX_PW_P3 0x14 //'RX payload width, pipe3' register address

#define RX_PW_P4 0x15 //'RX payload width, pipe4' register address

#define RX_PW_P5 0x16 //'RX payload width, pipe5' register address

#define FIFO_STATUS 0x17 //'FIFO Status Register' register address

#define DYNPD 0x1C

#define FEATURE 0x1D

//------------------------------------------------

#define PRIM_RX 0x00 //RX/TX control (1: PRX, 0: PTX)

#define PWR_UP 0x01 //1: POWER UP, 0:POWER DOWN

#define RX_DR 0x40 //Data Ready RX FIFO interrupt

#define TX_DS 0x20 //Data Sent TX FIFO interrupt

#define MAX_RT 0x10 //Maximum number of TX retransmits interrupt

//------------------------------------------------

#define W_REGISTER 0x20 //?????? ? ???????

//------------------------------------------------

#define STATUS 0x07 //'Status' register address 

#define OBSERVE_TX 0x08 //'Transmit observe' register

//--------------------------------------------------
#define ADR_WIDTH 4

#define TX_PLOAD_WIDTH 12 //bite in packet
extern volatile uint8_t nrf_rx_flag, nrf_tx_flag, nrf_tx_fail;

extern uint8_t NRF_TX_ADDR[ADR_WIDTH];// = { 0xb7, 0xb5, 0xa1 };
extern uint8_t NRF_RX_ADDR[ADR_WIDTH];// = { 0xb5, 0xb5, 0xa1 };
extern uint8_t NRF_RX_BUF[TX_PLOAD_WIDTH+1];
//extern uint8_t NRF_RF_CH;


extern uint8_t NRF_DBG_PRINT_F;


uint8_t NRF24_Init(void);
void NRF24_WriteReg(uint8_t addr, uint8_t dt);
uint8_t NRF24_ReadReg(uint8_t addr);
void NRF24_Read_Buf(uint8_t addr,uint8_t *pBuf,uint8_t bytes);
void NRF24_Write_Buf(uint8_t addr, uint8_t *pBuf, uint8_t bytes);
void NRF24_Send(uint8_t *pBuf);
void NRF24_IRQ_Callback(void);
void NRF24_Get_State(void);

//------------------------------------------------

#endif /* NRF24_H_ */
