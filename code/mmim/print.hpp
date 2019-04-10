//Print on file

#ifndef PRINT_HPP
#define PRINT_HPP

#include <vector>
#include <string>
#include "graph.hpp"

void printProbs(Graph &netGraph, std::string prob_filename, int k, int rep);
void writeOnFile(std::vector<float> results, std::string prob_filename, int k, int gap);

#endif // PRINT_HPP