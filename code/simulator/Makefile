.PHONY: clean
 
simulator: main.cpp argh.hpp
	$(CXX) --std=c++11 $< -o $@

clean:
	@rm -f simulator *~

test: simulator
	@./simulator                                      \
		--graph-file       example/karate.txt         \
		--seed-file        example/karate_seeds.txt   \
		--output-file      example/karate.out         \
		--num-simulations  1000
	@ cat example/karate.out
