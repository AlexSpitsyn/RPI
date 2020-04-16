#ifndef __WLAN_PACKET_PROC_H__
#define __WLAN_PACKET_PROC_H__
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include "crc32.h"

enum PACK_STATE{
  PS_NEW,
  PS_OK,
  PS_CMD_NOT_SUPPORTED,
  PS_VAR_NOT_SUPPORTED,
  PS_VAL_NOT_SUPPORTED,
  PS_CRC_BAD,
  PS_ERROR
};
enum WTS_STATE{
  WTS_OK=1,
  WTS_NA,//NOT AVALIBLE
  WTS_CMD_NOT_SUPPORTED,
  WTS_VAR_NOT_SUPPORTED,
  WTS_VAL_NOT_SUPPORTED,
  WTS_MAX_RT, //MAX RETRY, packet recived? but CRC BAD >3x
  WTS_ERROR
};

enum CMD_STATE{
	CMD_PRESENT,
	CMD_GET,
	CMD_SET,
	CMD_EEPROM_WR,
	CMD_ERR_CLR
};


typedef struct {//__attribute__((__packed__)){
uint32_t src_addr;
uint32_t dest_addr;
uint8_t flags;	
uint8_t state;
uint8_t cmd;
uint8_t var;	
int16_t val;	
uint16_t pack_ID;
	
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

void print_packet(WL_Packet* pack);
void convert_data_to_pack(uint8_t* data, WL_Packet* pack);
void convert_pack_to_data(uint8_t* data, WL_Packet* pack);
	
	
	
#endif
