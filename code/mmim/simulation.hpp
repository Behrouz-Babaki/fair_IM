// Simulate the spread of information over network
// Also outputs the results

#ifndef SIMULATION_HPP
#define SIMULATION_HPP

#include <vector>
#include "graph.hpp"

struct simRes
{
    int node;
    float minPr;
    float minWeight;
    int minGroup;
    int nodeW;
    float minPrW;
    float minWeightW;
    int minGroupW;
    int rep;
    float avePr;
};

void print_result(std::vector<int> &, int, int, Graph, int *);
simRes simulation(std::vector<int> &seeds, float alpha, int rep, Graph graph);

#endif // SIMULATION_HPP
