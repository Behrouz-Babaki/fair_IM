// Heuristics: Random, Max-Degree, K-Center

#ifndef ALGORITHMS_HPP
#define ALGORITHMS_HPP

#include <vector>
#include "graph.hpp"

std::vector<int> random(int init, int rep, int k, Graph &graph);
std::vector<int> max_deg(int init, int rep, int k, Graph &graph);
std::vector<int> max_deg_adv(int init, int rep, int k, Graph &graph);
std::vector<int> min_deg(int init, int rep, int k, Graph &graph);
std::vector<int> min_deg_adv(int init, int rep, int k, Graph &graph);
std::vector<int> k_gonz(int init, int rep, int k, Graph graph);

#endif // ALGORITHMS_HPP
