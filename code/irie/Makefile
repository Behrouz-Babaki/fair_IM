CC=g++
CFLAGS+= -O3 -g -std=c++11 
CPP_FILES := $(wildcard src/*.cpp)
OBJ_FILES := $(patsubst src/%,obj/%,$(CPP_FILES:.cpp=.o))

bin/irie: $(OBJ_FILES)
	$(CC) $^ -o $@

obj/%.o: src/%.cpp
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -rf bin/* obj/* core *~ src/*~ data/*IRIE*

test: bin/irie
	./bin/irie -irie 50 0.1 0.9 data/sampleData.txt
