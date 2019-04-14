// Greedy Heuristics: ...

#ifndef GREEDY_HPP
#define GREEDY_HPP

#include <vector>
#include "graph.hpp"

std::vector<int> myopic(int init, int rep, int k, Graph &graph);
std::vector<int> naiveMyopic(int init, int rep, int k, Graph &graph);
std::vector<int> greedy_Reach(int init, int rep, int k, Graph &graph, bool obj);
std::vector<int> naiveGreedy_Reach(int init, int rep, int k, Graph &graph, bool obj);

#endif // GREEDY_HPP