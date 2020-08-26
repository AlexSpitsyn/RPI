#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <time.h>
#include <stdint.h>

typedef struct{
  uint32_t addr;
  uint8_t state;
  int16_t val;
}WTS;
uint8_t wts_num =2;
WTS wts ={1,1,20};
int main(){
        FILE *fp;
        int c;
        int cnt=0;
		time_t rawtime;
		struct tm * timeinfo;
		time ( &rawtime );
		timeinfo = localtime ( &rawtime );
		//printf ( "Текущее время и дата: %s", asctime (timeinfo) );
		//return 0;
		//data
		fp = fopen("wts_data.txt", "w");
		if (fp == NULL){
			printf("Error opening file!\n");
			exit(1);
			return 1;
		}else{

		//fprintf(fp, "WTSN;STATE;VAL\r\n" );
		fprintf(fp, "%d;%d;%d",wts_num, wts.val, wts.state);	
		fclose(fp);
		}
		
        fp = fopen("wts_log.txt", "at");
        if (fp == NULL){
                        printf("Error opening file!\n");
                        exit(1);
        }else{                 

                //fprintf(fp, "WTSN;STATE;VAL\r\n" );
                fprintf(fp, "WTS%d %d %d %s",1, 20, 1, asctime (timeinfo));
                fclose(fp);
        }

        //fprintf(fp, "WTSN;STATE;VAL\r\n" );
        //fprintf(fp, "%d;%d;%d\r\n",wts_num, wts.state, wts.val);
        //fclose(fp);
        return 0;
}
