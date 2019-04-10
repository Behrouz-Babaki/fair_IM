// Greedy Heuristics: ...

#ifndef GREEDY_HPP
#define GREEDY_HPP

#include <vector>
#include "graph.hpp"

std::vector<float> myopic(int init, int rep, int k, int gap, Graph &graph);
std::vector<float> naiveMyopic(int init, int rep, int k, int gap, Graph &graph);
std::vector<float> greedy_Reach(int init, int rep, int k, int gap, Graph &graph, bool obj);
std::vector<float> naiveGreedy_Reach(int init, int rep, int k, int gap, Graph &graph, bool obj);

#endif // GREEDY_HPP