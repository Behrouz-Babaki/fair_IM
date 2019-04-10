#include <string>
#include <iostream>
#include <fstream>
#include "print.hpp"

using std::string;
using std::ofstream;
using std::to_string;
using std::endl;
using std::vector;

void printProbs(Graph& netGraph, string prob_filename, int k, int rep) {
    // ofstream outMin (prob_filename + "." + to_string(k));
    // for(int i = 0; i < netGraph.n; i++)
    //     outMin << float(netGraph.prob[i])/rep << endl;
    // outMin.close();
}

void writeOnFile(vector<float> results, string prob_filename, int k, int gap) {
    ofstream outMin (prob_filename);
    for(int i = 0; i <= k; i += gap)
        outMin << i << ": " << results[i/gap] << endl;
    outMin.close();
}
