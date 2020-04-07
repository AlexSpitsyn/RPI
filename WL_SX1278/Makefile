#CC=gcc
#CFLAGS=-march=armv6zk -mtune=arm1176jzf-s -mfpu=vfp -mfloat-abi=hard -Ofast -Wall -pthread -lbcm2835 -lwiringPi -lrt -lpigpio 

CC=gcc
CFLAGS=-lpigpio -lrt -pthread -lm

all: read_wts_num

read_wts_num: read_wts_num.o crc32.o wlan_packet_proc.o LoRa.o 
	$(CC) $(CFLAGS) wlan_packet_proc.o read_wts_num.o crc32.o LoRa.o -o read_wts_num 

crc32.o: crc32.c
	$(CC) $(CFLAGS) -c crc32.c

read_wts_num.o: read_wts_num.c
	$(CC) $(CFLAGS) -c read_wts_num.c

wlan_packet_proc.o: wlan_packet_proc.c
	$(CC) $(CFLAGS) -c wlan_packet_proc.c

LoRa.o: LoRa.c
	$(CC) $(CFLAGS) -c LoRa.c 

clean:
	rm -rf *.o read_wts_num 
install:
	install  ./read_wts_num /usr/local/bin
#	cp read_wts_num /usr/local/bin/read_wts_num
uninstall:
	rm -f /usr/local/bin/read_wts_num
#	rm -f /usr/local/bin/nrf_init
