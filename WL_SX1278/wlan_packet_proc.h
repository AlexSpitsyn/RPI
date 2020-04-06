#ifndef __WLAN_PACKET_PROC_H__
#define __WLAN_PACKET_PROC_H__
#include <stddef.h>
#include <stdint.h>
#include <cstdio>
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

typedef struct{
  uint8_t state;
  uint8_t host_addr;
  uint8_t cmd;
  uint8_t var;
  uint16_t val;
  uint16_t pack_ID;
  uint32_t crc;
}WL_Packet;

void print_packet(WL_Packet* pack);
void convert_data_to_pack(uint8_t* data, WL_Packet* pack);
void convert_pack_to_data(uint8_t* data, WL_Packet* pack);
	
	
	
#endif
