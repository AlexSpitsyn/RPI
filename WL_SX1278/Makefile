#CC=gcc
#CFLAGS=-march=armv6zk -mtune=arm1176jzf-s -mfpu=vfp -mfloat-abi=hard -Ofast -Wall -pthread -lbcm2835 -lwiringPi -lrt -lpigpio 

CC=gcc
CFLAGS=-lpigpio -lrt -pthread -lm

all: wl_send_cmd

wl_send_cmd: wl_send_cmd.o crc32.o wlan_packet_proc.o LoRa.o 
	$(CC) $(CFLAGS) wlan_packet_proc.o wl_send_cmd.o crc32.o LoRa.o -o wl_send_cmd 
	
crc32.o: crc32.c
	$(CC) $(CFLAGS) -c crc32.c

wl_send_cmd.o: wl_send_cmd.c
	$(CC) $(CFLAGS) -c wl_send_cmd.c

wlan_packet_proc.o: wlan_packet_proc.c
	$(CC) $(CFLAGS) -c wlan_packet_proc.c

LoRa.o: LoRa.c
	$(CC) $(CFLAGS) -c LoRa.c 

clean:
	rm -rf *.o wl_send_cmd 
	rm -rf *.o read_wts_num 
install:
	install  ./wl_send_cmd /usr/local/bin
	
uninstall:
	rm -f /usr/local/bin/wl_send_cmd

