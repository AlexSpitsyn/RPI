CC=g++
CFLAGS=-march=armv6zk -mtune=arm1176jzf-s -mfpu=vfp -mfloat-abi=hard -Ofast -Wall -pthread -lbcm2835 -lwiringPi -lrt -lpigpio 

all: read_wts_num

read_wts_num: read_wts_num.o crc32.o wlan_packet_proc.o LoRa.o 
	$(CC) $(CFLAGS) wlan_packet_proc.o read_wts_num.o crc32.o -o read_wts_num -lm


crc32.o: crc32.cpp
	$(CC) $(CFLAGS) -c crc32.cpp

read_wts_num.o: read_wts_num.cpp
	$(CC) $(CFLAGS) -c read_wts_num.cpp

wlan_packet_proc.o: wlan_packet_proc.cpp
	$(CC) $(CFLAGS) -c wlan_packet_proc.cpp

nrf_config.o: LoRa.cpp
	$(CC) $(CFLAGS) -c nrf_config.cpp

clean:
	rm -rf *.o read_wts_num 
install:
	install  ./read_wts_num /usr/local/bin
#	cp read_wts_num /usr/local/bin/read_wts_num
uninstall:
	rm -f /usr/local/bin/read_wts_num
#	rm -f /usr/local/bin/nrf_init
