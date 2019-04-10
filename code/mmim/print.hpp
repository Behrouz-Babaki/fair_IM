//Print on file

#ifndef PRINT_HPP
#define PRINT_HPP

#include <vector>
#include <string>
#include "graph.hpp"

void printProbs(Graph &netGraph, std::string algName, int k, float alpha, int rep);
void writeOnFile(std::vector<float> results, std::string algName, float alpha, int k, int gap);

#endif // PRINT_HPP