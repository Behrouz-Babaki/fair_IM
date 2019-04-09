.POHNY: clean all

%.o: %.cpp
	g++ --std=c++11 -c $< -o $@

main: main.o graph.o
	g++ $^ -o $@
