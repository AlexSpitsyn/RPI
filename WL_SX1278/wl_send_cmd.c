
//#include <cstdlib>
//#include <iostream>
//#include <fstream>
//#include <sstream>
#include <string.h>
//#include <unistd.h>
#include <stdlib.h>
#include "crc32.h"
#include <time.h>
#include "wlan_packet_proc.h"
#include "LoRa.h"


//using namespace std;

#define PLOAD_WIDTH  20

WL_ADDRESS WL_ADDR = { .S = "HOST" };
uint8_t data_received=0;

 void tx_f(txData *tx){
    LoRa_ctl *modem = (LoRa_ctl *)(tx->userPtr);
    printf("tx done;\r\n");
    //printf("sent string: \"%s\"\n\n", tx->buf);//Data we've sent
    
    LoRa_receive(modem);
}

void rx_f(rxData *rx){
    LoRa_ctl *modem = (LoRa_ctl *)(rx->userPtr);
    LoRa_stop_receive(modem);//manually stoping RxCont mode
    printf("rx done;\r\n");
    printf("CRC error: %d;\r\n", rx->CRC);
    printf("Data size: %d;\r\n", rx->size);
    //printf("received string: \"%s\";\r\n", rx->buf);//Data we've received
    printf("RSSI: %d;\r\n", rx->RSSI);
    printf("SNR: %f\r\n", rx->SNR);
    data_received=1;
    LoRa_sleep(modem);
} 



int main(int argc, char** argv) {
	//addr cmd var val

	int tx_addr=0;
	int tx_cmd=0;
	int tx_var=0;
	int tx_val=0;
	//ADDR
	if(argc<2){
		printf("ERROR: addr not specified\r\n");
		return 1;
	}else{
		if(sscanf(argv[1], "%d", &tx_addr)!=1){
			fprintf(stderr, "Bad number: %s\r\n", argv[1]);
			return 1;
		}else{
			printf("TX_ADDR = %d\n\r", tx_addr);
		}
	}
	//CMD
	if(argc<3){
		printf("ERROR: cmd not specified\r\n");
		return 1;
	}else{
		if(sscanf(argv[2], "%d", &tx_cmd)!=1){
			fprintf(stderr, "Bad number: %s\r\n", argv[2]);
			return 1;
		}else{
			printf("TX_CMD = %d\n\r", tx_cmd);
		}
	}
	//VAR
	if(argc<4){
		printf("WARNING: var not specified. Default 0\r\n");	
	}else{
		if(sscanf(argv[3], "%d", &tx_var)!=1){
			fprintf(stderr, "Bad number: %s\r\n", argv[3]);
			return 1;
		}else{
			printf("TX_VAR = %d\n\r", tx_var);
		}	
	}
	//VAL
	if(argc<5){
		printf("WARNING: val not specified. Default 0\r\n");		
	}else{
		if(sscanf(argv[4], "%d", &tx_val)!=1){
			fprintf(stderr, "Bad number: %s\r\n", argv[4]);
			return 1;
		}else{
			printf("TX_VAL = %d\n\r", tx_val);
		}	
	}

	
	LoRa_ctl modem;
	
	uint32_t CRC;	
	WL_Packet rx_pack, tx_pack;
	char txbuf[PLOAD_WIDTH];
    char rxbuf[PLOAD_WIDTH];	
	
	time_t send_time, send_timeout;
	
	time_t rawtime;
	struct tm * timeinfo;
	time ( &rawtime );
	timeinfo = localtime ( &rawtime );
	

	tx_pack.src_addr = WL_ADDR.Val;
	tx_pack.dest_addr = (uint32_t)tx_addr;
	tx_pack.state = PS_NEW;
	tx_pack.cmd = (uint8_t)tx_cmd;
	tx_pack.var = (uint8_t)tx_var;
	tx_pack.val = (uint16_t)tx_val;
	tx_pack.pack_ID = (uint16_t)clock();
	tx_pack.crc= Crc32(&tx_pack,16);	
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
    modem.eth.preambleLen=12;
    modem.eth.bw = BW125;
    modem.eth.sf = SF8;
    modem.eth.ecr = CR5;
    modem.eth.CRC = 1;//Turn on CRC checking
    modem.eth.freq = 434000000;
    modem.eth.resetGpioN = 25;//lora RESET pin
    modem.eth.dio0GpioN = 24;//lora DIO0 pin to control Rxdone and Txdone interrupts
    modem.eth.outPower = OP7;//Output power
    modem.eth.powerOutPin = PA_BOOST;//Power Amplifire pin
    modem.eth.AGC = 1;//Auto Gain Control
    modem.eth.OCP = 240;// 45 to 240 mA. 0 to turn off protection
    modem.eth.implicitHeader = 0;//Explicit header mode
    modem.eth.syncWord = 0x12;	
	
	//memcpy(modem.tx.data.buf, tx_f, PLOAD_WIDTH);
	LoRa_begin(&modem);
	//LoRa_print_state(&modem);	
	printf("\n\rTX PACKET:\n\r");
	print_packet(&tx_pack);

	while(send_cnt<3){
		LoRa_send(&modem);
		time(&send_time);
		printf("\n\rSent to %08X\n\rTry: %d\n\r", tx_addr, send_cnt+1);
		printf("Start listening...\n\r");
				
		data_received=0;
		  
		while(difftime(send_timeout,send_time)<5 ){
						
			if (data_received) {				
				
				printf( "Data: [");
				for (uint8_t i = 0; i < PLOAD_WIDTH; ++i) {
					if (i == 0) {
					  printf("%02X", rxbuf[i]);
					} else {
					  printf(", %02X", rxbuf[i]);
					}
				}   
				printf( "]");

				convert_data_to_pack(rxbuf, &rx_pack);				
				printf("\n\rRX PACKET:\n\r");
				print_packet(&rx_pack);
				CRC = Crc32(rxbuf,16);			
					
				if(CRC!=rx_pack.crc){		
					printf("CRC: BAD\n\r");				
					if(send_cnt==3){
						return WL_CRC_BAD;
					}
					send_cnt++;
					//delay(3000);
							
				}else{
					
					if(rx_pack.src_addr!=tx_pack.dest_addr | rx_pack.dest_addr!=WL_ADDR.Val){		
						printf("WRONG ADDR\n\r");				
						if(send_cnt==3){
							return WL_ADDRESS_FAIL;
					}
					send_cnt++;
					//delay(3000);
							
					}else{
					
						printf("CRC: OK\r\n" );
						printf("ADDR PASS\n\r");	
						printf("Pack state: %d\r\n", rx_pack.state);
						
						FILE *fp;
						//data
						fp = fopen("retpack.txt", "w");
						if (fp == NULL){
							printf("Error opening file!\n");
							exit(1);
							return WL_ERROR;
						}else{
				
							//fprintf(fp, "ADDR;STATE;CMD;VAR;VAL\r\n" );
							fprintf(fp, "%d;%d;%d;%d;%d",rx_pack.src_addr, rx_pack.state, rx_pack.cmd,rx_pack.var, rx_pack.val);	
							fclose(fp);
						}
						
						
						//LOG
						fp = fopen("wl_log.txt", "at");
						if (fp == NULL){
							printf("Error opening file!\n");
							exit(1);
							return WL_ERROR;
						}	
						//fprintf(fp, "WTSN;STATE;VAL\r\n" );
							
						fprintf(fp, "%d %d %d %d %d %s", rx_pack.src_addr, rx_pack.state, rx_pack.cmd, rx_pack.var, rx_pack.val, asctime (timeinfo));	
						fclose(fp);			
						return WL_OK;
					}
					
				}	
			}
			sleep(1);
			time(&send_timeout);
		}				
		
		printf ("====Data NOT Recieved====\n\r");
		send_cnt++;
		
	}    
	
	return WL_OFFLINE; 
}

