CC=g++
#CFLAGS=-c -O3 
CFLAGS=-c
DEBFLAGS=-c -g

all: InfluenceModels

InfluenceModels: common.o anyoption.o MC.o InfluenceModels.o 
	$(CC) common.o anyoption.o MC.o InfluenceModels.o -o InfluenceModels
#	$(CC) -O3 common.o anyoption.o MC.o InfluenceModels.o -o InfluenceModels

common.o: common.cc
	$(CC) $(CFLAGS) common.cc	

anyoption.o: anyoption.cc
	$(CC) $(CFLAGS) anyoption.cc 

MC.o: MC.cc
	$(CC) $(CFLAGS) MC.cc

InfluenceModels.o: InfluenceModels.cc
	$(CC) $(CFLAGS) InfluenceModels.cc

debug: common_debug.o anyoption_debug.o MC_debug.o InfluenceModels_debug.o
	$(CC) -g common.o anyoption.o MC.o InfluenceModels.o -o InfluenceModels_debug

common_debug.o: common.cc
	$(CC) $(DEBFLAGS) common.cc

anyoption_debug.o: anyoption.cc
	$(CC) $(DEBFLAGS) anyoption.cc 

MC_debug.o: MC.cc
	$(CC) $(DEBFLAGS) MC.cc

InfluenceModels_debug.o: InfluenceModels.cc
	$(CC) $(DEBFLAGS) InfluenceModels.cc

clean:
	rm -rf core *.o *~ InfluenceModels InfluenceModels_debug output temp

test: InfluenceModels
	./InfluenceModels -c config_test.txt

