#ifndef __WLAN_PACKET_PROC_H__
#define __WLAN_PACKET_PROC_H__
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "crc32.h"

#define PACKET_SIZE		36

enum WL_CMD_STATE{								
	CMD_DONE,				//0
	CMD_NOT_SUPPORTED,		//1
	VAR_NOT_SUPPORTED,		//2
	VAL_NOT_SUPPORTED,		//3	
	CMD_ERROR				//4
};

#define CMD_STATE_STR_CNT	5
static const char* CMD_STATE_STR[CMD_STATE_STR_CNT] = { 		
		"DONE",		
		"CMD NOT SUPPORTED",
		"VAR NOT SUPPORTED",
		"VAL NOT SUPPORTED",		
		"ERROR"
};

enum WL_STATE{
  WL_OK ,   
  WL_ADDRESS_FAIL,
  WL_CRC_BAD, 
  WL_ERROR,
  WL_OFFLINE  
};


enum WL_CMD{
	CMD_PRESENT,
	CMD_GET,
	CMD_SET,
	CMD_EEPROM_WR,
	CMD_ERR_CLR
};

#define CMD_STR_CNT	5
static const char* CMD_STR[CMD_STR_CNT] = { 
		"PRESENT",
		"GET",
		"SET",
		"EEPROM_WR",
		"ERR_CLR"
		};



typedef struct {//__attribute__((__packed__)){
uint32_t src_addr;
uint32_t dest_addr;
uint8_t dev_error_code;	
uint8_t state;
uint8_t cmd;
uint8_t var;	
int16_t val;	
uint16_t pack_ID;	
uint8_t desc[16];		
uint32_t crc;		

}WL_Packet;

typedef union {
    
			uint32_t Val;
			char S[5];
		
}WL_ADDRESS;

typedef struct{
  uint32_t addr;
  uint8_t state;
  int16_t val;
}WTS;

void print_packet(WL_Packet* pack,FILE *fp);
void convert_data_to_pack(uint8_t* data, WL_Packet* pack);
void convert_pack_to_data(uint8_t* data, WL_Packet* pack);
	
	
	
#endif
