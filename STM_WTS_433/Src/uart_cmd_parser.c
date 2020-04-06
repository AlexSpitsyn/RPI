#include "uart_cmd_parser.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include "stdarg.h"
#include "wireless_ctrl.h"
#include "usart.h"



void uartInit(void) {  

  putsUSART("\r\n");
  putsUSART("\r\n");
  putsUSART("             |||||||||||||||\r\n");
  putsUSART("         ||||||||||||||||||||||\r\n");
  putsUSART("       ||||||||||||||||||||||||||\r\n");
  putsUSART("      ||||     |||||||||      |||||\r\n");
  putsUSART("    ||||     ||||||||||||||    |||||\r\n");
  putsUSART("   |||||  ||||||||||||||||||||  |||||\r\n");
  putsUSART("   ||||| |||||||||     |||||||| ||||||\r\n");
  putsUSART("  ||||||||||||              |||||||||||\r\n");
  putsUSART("  ||||||||||                  |||||||||\r\n");
  putsUSART(" |||||||||                      |||||||\r\n");
  putsUSART(" ||||||||                        ||||||\r\n");
  putsUSART(" |||||||                          |||||\r\n");
  putsUSART("  ||||||                          |||||\r\n");
  putsUSART("  |||||                           |||||\r\n");
  putsUSART("  |||||                           ||||\r\n");
  putsUSART("   ||||                           ||||\r\n");
  putsUSART("    ||||          |||||||||       |||\r\n");
  putsUSART("     ||||    ||  |||||||||||||   |||\r\n");
  putsUSART("       ||||||||  |||||||||||||||||\r\n");
  putsUSART("        |||||||  |||||||||||||||\r\n");
  putsUSART("           |||||||||||||||||||\r\n");
  putsUSART("               |||||||||||\r\n");
  putsUSART("                                    ||||\r\n");
  putsUSART("       ||||||    ||||||        |||||||||\r\n");
  putsUSART("      |||||||  ||||||||||    |||||||||||\r\n");
  putsUSART("     |||||    ||||||||||||  ||||||||||||\r\n");
  putsUSART("     ||||     ||||    ||||| ||||    ||||\r\n");
  putsUSART("    |||||     ||||    ||||| ||||    ||||\r\n");
  putsUSART("||||||||       ||||||||||||  |||||||||||\r\n");
  putsUSART("|||||||         |||||||||||   ||||||||||\r\n");
  putsUSART("Wireless Temp Sensor v.2\r\n> ");

}


#define UVARS_CNT 10
#define DEC_STR 10
#define HEX_STR 16

#define CMD_CNT 8

static const char* commands[CMD_CNT] = {							
		"help",         // 0                      
		"init",     		// 1
		"send",      	  // 2
		"set",       	  // 3
		"get state",		// 4
		"debug",				// 5
		"clear irq",		// 6
		"rx handler"		// 7
											
	}; 
#define PRM_CNT 5
static const char* param[PRM_CNT] = {							
		"addr",         // 0                      
		"pwr",     			// 1
		"bw",      	  	// 2
		"sf",       	  // 3
		"cr"						// 4
											
	}; 
void parseCommand(char *buf) {
  uint8_t i=0, l=0;
  char *pArg1 = NULL, *pArg2 = NULL, *pEnd = NULL;
  
  char answer[64] = "";

	uint32_t cmd, var, val, addr, tmp;





  for (i = 0; i < CMD_CNT; i++) {
    if (strncmp(buf, commands[i], strlen(commands[i])) == 0) {
      l = strlen(commands[i]);
      pArg1 = buf + l + 1;
      break;
    }
  }

  switch (i) {
    

    case 0:  // help
putsUSART(
          "\r\n"
          "help\r\n"          
          "init\r\n"	
					"send addr(0x00000000-0xFFFFFFFF) cmd(0-1) var(0-1) val\r\n"		
					"set /addr [0x00000000-0xFFFFFFFF] / pwr [0-3] / bw [0-9] / sf [6-12] / cr [0-4]\r\n");
putsUSART("get state\r\n"
					"debug [sx / wl]\r\n"
					"rx handler [on / off]\r\n"
					"cmd 0 - present addr\r\n"
					"cmd 1 - get\r\n"
					"var 0 - temp\r\n");
      break;

    case 1:  // init
			
      SX1278_defaultConfig();
		putsUSART("\r\nSX1278 init: OK\r\n");

      break;

    case 2:  // send
      if (*(pArg1) == 0) {
        putsUSART("wrong var");
      } else {
				if(str_to_int32( pArg1,&pEnd,HEX_STR,&addr,0x00000000, 0xFFFFFFFF) | str_to_int32(pEnd,&pEnd,DEC_STR,&cmd,0, 255) | str_to_int32(pEnd,&pEnd,DEC_STR,&var,0, 255) | str_to_int32(pEnd,&pEnd,DEC_STR,&val,0, 0xFFFF)){
					putsUSART("wrong parameters");		
				}else{					
					sprintf(answer, "SEND CODE: %s",PACK_STATE_STR[WL_Send_Packet(0, PS_NEW, addr, (uint8_t)cmd,  (uint8_t)var,  (uint16_t)val)]);		
					putsUSART(answer);	
				}	

      }
      break;

    case 3:  // set 
			if (*(pArg1) == 0) {
        putsUSART("wrong var");
      } else {
				for (i = 0; i < PRM_CNT; i++) {
					if (strncmp(pArg1, param[i], strlen(param[i])) == 0) {
						l = strlen(param[i]);
						pArg2 = pArg1 + l + 1;
						break;
					}
				}
				if (*(pArg2) == 0) {
            putsUSART("wrong param value");
        } else {
					switch (i){
						//addr [0x00000000-0xFFFFFFFF] / pwr [0-3] / bw [0-9] / sf [6-12] / cr [0-4]\r\n");
						case 0://addr
							if(str_to_int32(pArg2,&pEnd,HEX_STR,&tmp,0x00000000, 0xFFFFFFFF)){
								putsUSART("Wrong WL ADDR value [0x00000000-0xFFFFFFFF]");		
							}else{
								WL_ADDR.Val = tmp;
								sprintf(answer, "Set WL ADDR: 0x%08X / %s", WL_ADDR.Val, WL_ADDR.S);
								putsUSART(answer);
							}	
							break;
							
						case 1://power
							if(str_to_int32(pArg2,&pEnd,DEC_STR,&tmp,0, 3)){
								putsUSART("Wrong POWER value [0-3]");		
							}else{
								SX1278.POWER = (uint8_t)tmp;
								sprintf(answer, "Set SX1278 POWER: %s dBm", SX1278_Power_s[(uint8_t)tmp]);
								putsUSART(answer);
							}
							break;
							
						case 2://bw
							if(str_to_int32(pArg2,&pEnd,DEC_STR,&tmp,0, 9)){
								putsUSART("Wrong Bandwidth value [0-9]");		
							}else{
								SX1278.BW = (uint8_t)tmp;
								sprintf(answer, "Set SX1278 Bandwidth: %s kHz", SX1278_LoRaBandwidth_s[SX1278.BW]);
								putsUSART(answer);
							}
							break;
							
						case 3://sf
							if(str_to_int32(pArg2,&pEnd,DEC_STR,&tmp,6, 12)){
								putsUSART("Wrong SF value [6-12]");		
							}else{
								SX1278.SF = (uint8_t)tmp-6;
								sprintf(answer, "Set SX1278 SF: %d", SX1278_SpreadFactor[SX1278.SF]);
								putsUSART(answer);
							}							
							break;
							
						case 4://cr
							if(str_to_int32(pArg2,&pEnd,DEC_STR,&tmp,0, 3)){
								putsUSART("Wrong Coding Rate value [0-3]");		
							}else{
								SX1278.CR = (uint8_t)tmp+1;
								sprintf(answer, "Set SX1278 Coding Rate: %s", SX1278_CR_s[SX1278.CR]);
								putsUSART(answer);
							}
							break;
							
						default:
							putsUSART("wrong param type");
							break;
						
					}	
					putsUSART("\r\n");	
					SX1278_defaultConfig();
				}
			}
			break;       

			case 4:  // get state
				putsUSART("\r\n-----  WL STATE  ----\r\n");	
				sprintf(answer, "WL ADDR: 0x%08X / %s", WL_ADDR.Val, WL_ADDR.S);
				putsUSART(answer);
				putsUSART("\r\n-----  SX1278 STATE  ----\r\n");	
				SX1278_Get_State();
				putsUSART("\r\n-----  DS STATE  ----\r\n");
				if(ds18b20_Reset()){
					putsUSART("STATE: FAIL");
				}else{
					ds18b20_GetTemp();
					sprintf(answer, "STATE: OK\r\nTEMP: %d'C", DS_TEMP);
					putsUSART(answer);
				}			
				break;

    	case 5:// debug
				if (*(pArg1) == 0) {
					putsUSART("wrong var");
				} else {
					if (strncmp(pArg1,"wl", 2) == 0) {
						WL_DEBUG_PRINT^=1;
						if(WL_DEBUG_PRINT){
							putsUSART("DEBUG SET");
						}else{
							putsUSART("DEBUG RESET");
						}							
					}else if(strncmp(pArg1,"sx", 2)==0) {
						SX1278_DBG_PRINT_F^=1;
						if(SX1278_DBG_PRINT_F){
							putsUSART("SX1278 DEBUG SET");
						}else{
							putsUSART("SX1278 DEBUG RESET");
						}
					}else{
						putsUSART("wrong command");						
					}
      }
				break;
				
			case 6: //rx handler
				SX1278_clearIrq();
				putsUSART("IRQ Clear: OK");
				break;				

			case 7:// r
				if (*(pArg1) == 0) {
					putsUSART("wrong var");
				} else {
					if (strncmp(pArg1,"on", 2) == 0) {
						rx_handler=1;
						if(WL_DEBUG_PRINT){
							putsUSART("rx handler SET");
						}						
					}else if(strncmp(pArg1,"off", 3)==0) {
						rx_handler=0;
						if(WL_DEBUG_PRINT){
							putsUSART("rx handler RESET");
						}
					}else{
						putsUSART("wrong command");						
					}
      }
				break;
    
			default:
				putsUSART("command unknown");
				break;
  }

  putsUSART("\r\n>");
}

uint8_t str_to_int32(char* str, char** end, uint8_t str_format, uint32_t* val, uint32_t vmin, uint32_t vmax){
	uint32_t conv_val;			
	conv_val=strtol(str, end, str_format);
	if((conv_val>=vmin)&&(conv_val<=vmax)){
		*val=conv_val;
		return 0;
		
	}else{
		return 1;
	}
}


