// Distance of every node to its nearest source
// Finds the first source using differenct approaches

#ifndef COMPUTATION_HPP
#define COMPUTATION_HPP

#include <string>
#include <vector>
#include "graph.hpp"

int *calcDist(std::vector<int> &seeds, Graph &g);
int pickCenter(Graph &g, std::string option);

#endif /* computation_h */
