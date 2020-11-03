
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

#define PLOAD_WIDTH  36

WL_ADDRESS WL_ADDR = { .S = "HOST" };

uint8_t data_received=0;
int dbg =0;
int loging =0;

int print_log(char *s){
	FILE *fp;
	time_t rawtime;
	struct tm * timeinfo;
	char tmp[32];
	time ( &rawtime );	
	timeinfo = localtime ( &rawtime );
	sprintf(tmp, "\t%s", asctime (timeinfo));
	strcat(s,tmp);
	
	fp = fopen("wl_log.txt", "at");
	if (fp == NULL){
		exit(1);		
	}			
	fprintf(fp, s);	
	fclose(fp);
} 


 void tx_f(txData *tx){
    LoRa_ctl *modem = (LoRa_ctl *)(tx->userPtr);
    
    LoRa_receive(modem);
}

void rx_f(rxData *rx){
    LoRa_ctl *modem = (LoRa_ctl *)(rx->userPtr);
    LoRa_stop_receive(modem);//manually stoping RxCont mode
    //dbg_print("rx done;\r\n");
	//dbg_print("CRC error: %d;\r\n", rx->CRC);
	//dbg_print("Data size: %d;\r\n", rx->size);
	//dbg_print("RSSI: %d;\r\n", rx->RSSI);
	//dbg_print("SNR: %f\r\n", rx->SNR);
	
    data_received=1;
    LoRa_sleep(modem);
} 

 


int main(int argc, char** argv) {

	//addr cmd var val
	
	
	
	
	char log_str[256];
	char tmp_str[32];
	int tx_addr=0;
	int tx_cmd=0;
	int tx_var=0;
	int tx_val=0;
	FILE *fp;	
	FILE *dbg_fp;	
	
	
	if(argc>5){
		int a=5;
		while(argv[a]!= 0){		
			if(!strcmp(argv[a], "-d")){
				dbg=1;
				dbg_fp = fopen("wlsend_debug.txt", "at");
				if (dbg_fp == NULL){
					exit(1);					
				}						
				
			}
			if(!strcmp(argv[a], "-l")){
				loging=1;	
				if(dbg){
					if(loging)
						if(dbg) fprintf(dbg_fp, "LOG = ON\n\r");
					else
						if(dbg) fprintf(dbg_fp, "LOG = ON\n\r");
				}			
			}
			a++;
		}
	}
	
	//ADDR
	if(argc<2){
		if(dbg) fprintf(dbg_fp, "ERROR: addr not specified\r\n");
		printf("ERROR: addr not specified\r\n");
		return 101;
	}else{
		
		tx_addr = (int)strtol(argv[1], NULL, 0);
		if(tx_addr==0){
			if(dbg) fprintf(dbg_fp,  "wrong TX ADDR: %s\r\n", argv[1]);
			printf("Bad number: %s\r\n", argv[1]);
			return 102;
		}else{
			if(dbg) fprintf(dbg_fp, "TX ADDR = 0x%08X\n\r", tx_addr);
		}		
	}
	//CMD
	if(argc<3){
		if(dbg) fprintf(dbg_fp, "ERROR: cmd not specified\r\n");
		printf("ERROR: cmd not specified\r\n");
		return 103;
	}else{
		if(sscanf(argv[2], "%d", &tx_cmd)!=1){
			if(dbg) fprintf(dbg_fp, "wrong TX CMD: %s\r\n", argv[2]);
			printf("wrong TX CMD: %s\r\n", argv[2]);
			return 104;
		}else{
			if(dbg) fprintf(dbg_fp, "TX CMD = %d\n\r", tx_cmd);
		}
	}
	//VAR
	if(argc<4){
		if(dbg) fprintf(dbg_fp, "WARNING: var not specified. Default 0\r\n");
		tx_var=0;
	}else{
		if(sscanf(argv[3], "%d", &tx_var)!=1){
			fprintf(dbg_fp, "wrong TX VAR: %s\r\n", argv[3]);
			printf("wrong TX VAR: %s\r\n", argv[3]);
			return 105;
		}else{
			if(dbg) fprintf(dbg_fp, "TX VAR = %d\n\r", tx_var);
		}	
	}
	//VAL
	if(argc<5){
		if(dbg) fprintf(dbg_fp, "WARNING: val not specified. Default 0\r\n");
		tx_val=0;
	}else{
		if(sscanf(argv[4], "%d", &tx_val)!=1){
			fprintf(dbg_fp, "wrong TX VAL: %s\r\n", argv[4]);
			printf("wrong TX VAL: %s\r\n", argv[4]);
			return 106;
		}else{
			if(dbg) fprintf(dbg_fp, "TX VAL = %d\n\r", tx_val);
		}	
	}
	
	

	
	LoRa_ctl modem;
	
	uint32_t CRC;	
	WL_Packet rx_pack, tx_pack;
	char txbuf[PLOAD_WIDTH];
    char rxbuf[PLOAD_WIDTH];	
	
	time_t send_time, send_timeout;
	
	

	tx_pack.src_addr = WL_ADDR.Val;
	tx_pack.dest_addr = (uint32_t)tx_addr;
	tx_pack.state = 0;
	tx_pack.desc[0] = 0;
	tx_pack.cmd = (uint8_t)tx_cmd;
	tx_pack.var = (uint8_t)tx_var;
	tx_pack.val = (uint16_t)tx_val;
	tx_pack.pack_ID = (uint16_t)clock();
	tx_pack.crc= Crc32(&tx_pack,PLOAD_WIDTH-4);	
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
	
	LoRa_begin(&modem);
	
	if(dbg) fprintf(dbg_fp, "\n\rTX PACKET:\n\r");
	if(dbg) print_packet(&tx_pack, dbg_fp);
	

	if(loging) sprintf(log_str, "%d\t0x%08X\t%s\t%d\t%d", tx_pack.pack_ID, tx_pack.dest_addr, CMD_STR[tx_pack.cmd], tx_pack.var, tx_pack.val);			
			
	while(send_cnt<3){
		LoRa_send(&modem);
		time(&send_time);
		if(dbg) fprintf(dbg_fp, "\n\rSent to %08X\n\rTry: %d\n\r", tx_addr, send_cnt+1);
		if(dbg) fprintf(dbg_fp, "Start listening...\n\r");
				
		data_received=0;
		  
		while(difftime(send_timeout,send_time)<5 ){
						
			if (data_received) {				
				data_received=0;
				if(dbg){
					fprintf(dbg_fp,  "Data: [");
					for (uint8_t i = 0; i < PLOAD_WIDTH; ++i) {
						if (i == 0) {
						  fprintf(dbg_fp, "%02X", rxbuf[i]);
						} else {
						  fprintf(dbg_fp, ", %02X", rxbuf[i]);
						}
					}   
					fprintf(dbg_fp,  "]");
				}

				convert_data_to_pack(rxbuf, &rx_pack);				
				if(dbg){
					fprintf(dbg_fp, "\n\rRX PACKET:\n\r");
					print_packet(&rx_pack, dbg_fp);
				}
				CRC = Crc32(rxbuf,PLOAD_WIDTH-4);			
					
				if(CRC!=rx_pack.crc){		
					if(dbg) fprintf(dbg_fp, "CRC: BAD\n\r");				
					if(send_cnt==3){
						if(loging){
							strcat(log_str, "\t\t\tCRC BAD");
							print_log(log_str);
						}
						printf("CRC BAD\r\n");
						return WL_CRC_BAD;
					}
					send_cnt++;
					//delay(3000);
							
				}else{
					
					if(rx_pack.src_addr!=tx_pack.dest_addr | rx_pack.dest_addr!=WL_ADDR.Val){		
						if(dbg) fprintf(dbg_fp, "WRONG ADDR\n\r");
						if(send_cnt==3){
							if(loging){
								strcat(log_str, "\t\t\tWRONG ADDR");
								print_log(log_str);
							}
							printf("ADDRESS MISMATCH\r\n");
							return WL_ADDRESS_FAIL;
					}
					send_cnt++;
					//delay(3000);
							
					}else{
					
						if(dbg){
							fprintf(dbg_fp, "CRC: OK\r\n" );
							fprintf(dbg_fp, "ADDR PASS\n\r");	
							fprintf(dbg_fp, "Pack cmd state: %s\r\n", CMD_STATE_STR[rx_pack.state]);
													
							fprintf(dbg_fp, "ADDR;STATE;CMD;VAR;VAL;DESC:ERROR_CODE\r\n");
							fprintf(dbg_fp, "%d;%d;%d;%d;%d;%s;%d",rx_pack.src_addr, rx_pack.state, rx_pack.cmd, rx_pack.var, rx_pack.val, rx_pack.desc, rx_pack.dev_error_code);
							
						}
							
						
												
						if(loging){
							sprintf(tmp_str,"\t-\t%s\t%d\t%s\t%d", CMD_STATE_STR[rx_pack.state], rx_pack.val, rx_pack.desc,rx_pack.dev_error_code);
							strcat(log_str, tmp_str);
							print_log(log_str);
						}	
						if(rx_pack.state == CMD_DONE){	
							printf("%d;%d;%d;%d;%d;%s;%d",rx_pack.src_addr, rx_pack.state, rx_pack.cmd, rx_pack.var, rx_pack.val, rx_pack.desc, rx_pack.dev_error_code);							
							return WL_OK;
						}else{
							printf("ERROER! PACK STATE: %s\r\n", CMD_STATE_STR[rx_pack.state]);	
							return WL_ERROR;
						}
					}
					
				}	
			}
			sleep(1);
			time(&send_timeout);
		}				
		
		if(dbg) fprintf(dbg_fp, "====Data NOT Recieved====\n\r");
		send_cnt++;
			
		
		
	}    
	if(loging){			
		strcat(log_str, "\t\t\tData NOT Recieved");
		print_log(log_str);
	}	
	printf("OFFLINE\r\n");	
	return WL_OFFLINE; 
}

