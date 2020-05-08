#include "wlan_packet_proc.h"

void print_packet(WL_Packet* pack){
  printf("CMD: 0x%02X\n\r",pack->cmd);
  printf("VAR: 0x%02X\n\r",pack->var);
  printf("VAL: 0x%04X\n\r",pack->val);
  printf("P_ID: 0x%04X\n\r",pack->pack_ID);
  printf("DEST ADDR: 0x%08X\n\r",pack->dest_addr);
  printf("SRC ADDR: 0x%08X\n\r",pack->src_addr);
  printf("STATE: 0x%02X\n\r",pack->state);
  printf("CRC: 0x%08X\n\r",pack->crc);
}

void convert_data_to_pack(uint8_t* data, WL_Packet* pack){
	
	pack->src_addr = (uint32_t)(data[3]<<24) | (uint32_t)(data[2]<<16) | (uint32_t)(data[1]<<8) | (uint32_t)data[0];
	pack->dest_addr = (uint32_t)(data[7]<<24) | (uint32_t)(data[6]<<16) | (uint32_t)(data[5]<<8) | (uint32_t)data[4];
	pack->flags = data[8];
	pack->state = data[9];
	pack->cmd = data[10];
	pack->var = data[11];
	pack->val = (uint16_t)(data[13]<<8) | (uint16_t)data[12];
	pack->pack_ID = (uint16_t)(data[15]<<8) | (uint16_t)data[14];
	pack->crc = (uint32_t)(data[19]<<24) | (uint32_t)(data[18]<<16) | (uint32_t)(data[17]<<8) | (uint32_t)data[16];
	
}

void convert_pack_to_data(uint8_t* data, WL_Packet* pack){
  //src_addr
  data[0] = (uint8_t)pack->src_addr;
  data[1] = (uint8_t)(pack->src_addr>>8);
  data[2] = (uint8_t)(pack->src_addr>>16);
  data[3] = (uint8_t)(pack->src_addr>>24);
  //dest_addr
  data[4] = (uint8_t)pack->dest_addr;
  data[5] = (uint8_t)(pack->dest_addr>>8);
  data[6] = (uint8_t)(pack->dest_addr>>16);
  data[7] = (uint8_t)(pack->dest_addr>>24);
  //flags not used
  data[8] = pack->flags;
  //state
  data[9] = (uint8_t)pack->state;
  //cmd
  data[10] = pack->cmd;
  //var
  data[11] = (uint8_t)pack->var;
  //val
  data[12] = (uint8_t)pack->val;
  data[13] = (uint8_t)(pack->val>>8);
  //pack ID
  data[14] = (uint8_t)pack->pack_ID;
  data[15] = (uint8_t)(pack->pack_ID>>8);
  //CRC
  data[16] = (uint8_t)pack->crc;
  data[17] = (uint8_t)(pack->crc>>8);
  data[18] = (uint8_t)(pack->crc>>16);
  data[19] = (uint8_t)(pack->crc>>24);
 
}

