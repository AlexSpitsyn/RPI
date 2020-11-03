#include "wlan_packet_proc.h"

void print_packet(WL_Packet* pack, FILE *fp){
  fprintf(fp, "CMD: 0x%02X\n\r",pack->cmd);
  fprintf(fp, "VAR: 0x%02X\n\r",pack->var);
  fprintf(fp, "VAL: 0x%04X\n\r",pack->val);
  fprintf(fp, "DESC: %s\n\r",pack->desc);
  fprintf(fp, "P_ID: 0x%04X\n\r",pack->pack_ID);
  fprintf(fp, "DEST ADDR: 0x%08X\n\r",pack->dest_addr);
  fprintf(fp, "SRC ADDR: 0x%08X\n\r",pack->src_addr);
  fprintf(fp, "DEV ERROR CODE: 0x%08X\n\r",pack->dev_error_code);
  fprintf(fp, "STATE: 0x%02X\n\r",pack->state);
  fprintf(fp, "CRC: 0x%08X\n\r",pack->crc);
}

void convert_data_to_pack(uint8_t* data, WL_Packet* pack){
		
	pack->src_addr = (uint32_t)(data[3]<<24) | (uint32_t)(data[2]<<16) | (uint32_t)(data[1]<<8) | (uint32_t)data[0];
	pack->dest_addr = (uint32_t)(data[7]<<24) | (uint32_t)(data[6]<<16) | (uint32_t)(data[5]<<8) | (uint32_t)data[4];
	pack->dev_error_code = data[8];
	pack->state = data[9];
	pack->cmd = data[10];
	pack->var = data[11];
	pack->val = (uint16_t)(data[13]<<8) | (uint16_t)data[12];
	pack->pack_ID = (uint16_t)(data[15]<<8) | (uint16_t)data[14];
	memcpy(pack->desc, &data[16], 16);
	pack->crc = (uint32_t)(data[35]<<24) | (uint32_t)(data[34]<<16) | (uint32_t)(data[33]<<8) | (uint32_t)data[32];
	
	//memcpy(pack, data, PACKET_SIZE);
	
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
  //dev_error_code not used
  data[8] = pack->dev_error_code;
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
  //desc
  memcpy(&data[16], pack->desc, 16);
  //CRC
  data[32] = (uint8_t)pack->crc;
  data[33] = (uint8_t)(pack->crc>>8);
  data[34] = (uint8_t)(pack->crc>>16);
  data[35] = (uint8_t)(pack->crc>>24);
  
 	//memcpy(data, pack, PACKET_SIZE);
 
 
}

