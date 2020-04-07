
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <unistd.h>
#include <stdlib.h>
#include "crc32.h"
#include <time.h>
#include "wlan_packet_proc.h"
#include "LoRa.h"


using namespace std;

#define PLOAD_WIDTH  20

WL_ADDRESS WL_ADDR = { .S = "WTSH" };
uint8_t data_recived=0;

 void tx_f(txData *tx){
    LoRa_ctl *modem = (LoRa_ctl *)(tx->userPtr);
    printf("tx done;\t");
    printf("sent string: \"%s\"\n\n", tx->buf);//Data we've sent
    
    LoRa_receive(modem);
}

void rx_f(rxData *rx){
    LoRa_ctl *modem = (LoRa_ctl *)(rx->userPtr);
    LoRa_stop_receive(modem);//manually stoping RxCont mode
    printf("rx done;\t");
    printf("CRC error: %d;\t", rx->CRC);
    printf("Data size: %d;\t", rx->size);
    printf("received string: \"%s\";\t", rx->buf);//Data we've received
    printf("RSSI: %d;\t", rx->RSSI);
    printf("SNR: %f\n", rx->SNR);
    data_recived=1;
    LoRa_sleep(modem);
} 



int main(int argc, char** wts_num) {

	if(argc<2){
		printf("WTS not specified\n\r");
		return 1;
	}


	int tmp;
	sscanf(wts_num[argc-1], "%d", &tmp);
	printf("WTS = %d\n\r", tmp);
	if(tmp<0){
		printf("Wrong WTS num\r\n");
		return 2;
	}
	if(tmp>16){
		printf("WTS num must be < 16\n\r");
		return 3;
	}
	
	WL_ADDRESS TX_ADDR = { .S = "WTS0" };
	TX_ADDR.S[3]=(uint8_t)tmp;
	
	LoRa_ctl modem;
	
	uint32_t CRC;	
	WL_Packet rx_pack, tx_pack;
	char txbuf[PLOAD_WIDTH];
    char rxbuf[PLOAD_WIDTH];	
	WTS wts={TX3_ADDR,0,0};
	time_t send_time, send_timeout;
	

	tx_pack.src_addr = WL_ADDR.Val;
	tx_pack.dest_addr = TX_ADDR.Val;
	tx_pack.state = PS_NEW;
	tx_pack.cmd = CMD_GET;
	tx_pack.var = 0;
	tx_pack.val = 1;
	tx_pack.pack_ID = (uint16_t)clock();
	convert_pack_to_data(txbuf, &tx_pack);
	
	
	uint8_t send_cnt=0;
    
    modem.spiCS = 0;//Raspberry SPI CE pin number
    modem.tx.callback = tx_f;
    modem.tx.data.buf = txbuf;
    modem.rx.callback = rx_f;
    modem.rx.data.buf = rxbuf;
    modem.rx.data.userPtr = (void *)(&modem);//To handle with chip from rx callback
    modem.tx.data.userPtr = (void *)(&modem);//To handle with chip from tx callback   
    modem.tx.data.size = PLOAD_WIDTH;//Payload len
    modem.eth.preambleLen=6;
    modem.eth.bw = BW20_8;
    modem.eth.sf = SF8;
    modem.eth.ecr = CR5;
    modem.eth.CRC = 1;//Turn on CRC checking
    modem.eth.freq = 434000000;
    modem.eth.resetGpioN = 25;//lora RESET pin
    modem.eth.dio0GpioN = 24;//lora DIO0 pin to control Rxdone and Txdone interrupts
    modem.eth.outPower = OP20;//Output power
    modem.eth.powerOutPin = PA_BOOST;//Power Amplifire pin
    modem.eth.AGC = 1;//Auto Gain Control
    modem.eth.OCP = 240;// 45 to 240 mA. 0 to turn off protection
    modem.eth.implicitHeader = 0;//Explicit header mode
    modem.eth.syncWord = 0x12;	
	
	memcpy(modem.tx.data.buf, sendData, PLOAD_WIDTH);
	LoRa_begin(&modem);
	
	//printf("\n\rTX PACKET:\n\r");
	print_packet(&tx_pack);
    
	while(send_cnt<3){
		
		time(&send_time);
		printf("\n\rSent to %s\n\rTry: %d\n\r", TX_ADDR.S,send_cnt+1);
		printf("Start listening...\n\r");
				
		data_recived=0;
		  
		while(difftime(send_timeout,send_time)<5 ){
						
			if (data_recived) {				
				
				cout << "Data: [";
				for (uint8_t i = 0; i < PLOAD_WIDTH; ++i) {
					if (i == 0) {
					  printf("%02X", rxbuf[i]);
					} else {
					  printf(", %02X", rxbuf[i]);
					}
				}   
				cout << "]" << endl;

				convert_data_to_pack(rxbuf, &rx_pack);
				printf("\n\rRX PACKET:\n\r");
				print_packet(&rx_pack);
				CRC = Crc32(rxbuf,16);			
					
				if(CRC!=rx_pack.crc){		
					printf("CRC: BAD\n\r");				
					if(send_cnt==3){
						wts.state = WTS_MAX_RT;
					}
					send_cnt++;
					//delay(3000);
							
				}else{
					printf("CRC: OK\r\n" );		
					switch(rx_pack.state){
						case PS_OK:
							wts.state = WTS_OK;
							wts.val = rx_pack.val;
							printf("Pack state: OK\r\n");
							printf("WTS%c Temp: %d'C\r\n", rx_pack.host_addr, wts.val);
							break;
						case PS_CRC_BAD:								
							send_cnt++;
							//delay(3000);
							break;
						case PS_CMD_NOT_SUPPORTED:
							wts.state = WTS_CMD_NOT_SUPPORTED;							
							printf("Pack state: CMD NOT SUPPORTED\n\r");														
							break;
						case PS_VAR_NOT_SUPPORTED:
							wts.state = WTS_VAR_NOT_SUPPORTED;							
							printf("Pack state: VAR NOT SUPPORTED\n\r");													 
							break;
						case PS_VAL_NOT_SUPPORTED:
							wts.state = WTS_VAL_NOT_SUPPORTED;							
							printf("Pack state: VAL NOT SUPPORTED\n\r" );
							break;
						case PS_ERROR:
							wts.state = WTS_ERROR;
							printf("Pack state: ERROR\n\r");
							break;
						default:
							wts.state = 0;
							printf("%s unknown error\n\r", WL_ADDR.S);
							break;
					}								
				}
			}
			delay(100);
			time(&send_timeout);
		}
		if(!data_recived){			
			wts.state = WTS_NA;
			printf ("Data NOT Recieved %d\n\r", send_cnt );
			send_cnt++;
		}else{
			break;
		}
	}
    
	
 
	std::ofstream out;          // поток для записи
    out.open("wts.csv"); // окрываем файл для записи
    if (out.is_open()){	
		out << "WTSN;STATE;VAL" << std::endl;
		out <<(int) wts.addr; 
		out <<";";
		out << (int)wts.state <<";";
		out << wts.val << std::endl;		
    }
	out.close();		
	return 0;
}

