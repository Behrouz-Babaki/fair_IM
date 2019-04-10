// Heuristics: Random, Max-Degree, K-Center

#ifndef ALGORITHMS_HPP
#define ALGORITHMS_HPP

#include <vector>
#include "graph.hpp"

std::vector<float> random(int init, float alpha, int rep, int k, int gap, Graph &graph);
std::vector<float> max_deg(int init, float alpha, int rep, int k, int gap, Graph &graph);
std::vector<float> max_deg_adv(int init, float alpha, int rep, int k, int gap, Graph &graph);
std::vector<float> min_deg(int init, float alpha, int rep, int k, int gap, Graph &graph);
std::vector<float> min_deg_adv(int init, float alpha, int rep, int k, int gap, Graph &graph);
std::vector<float> k_gonz(int init, float alpha, int rep, int k, int gap, Graph graph);

#endif // ALGORITHMS_HPP
