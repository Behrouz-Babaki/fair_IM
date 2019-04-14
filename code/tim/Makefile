all:
	g++ src/tim.cpp -Wall -std=c++11 -O3 src/sfmt/SFMT.c  -o tim

test: all
	./tim -model IC -dataset nethept/ -epsilon 0.1 -k 50

clean: 
	rm -f *~ tim