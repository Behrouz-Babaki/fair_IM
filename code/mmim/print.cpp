#include <string>
#include <iostream>
#include <fstream>
#include "print.hpp"

using std::string;
using std::ofstream;
using std::to_string;
using std::endl;
using std::vector;

void printProbs(Graph& netGraph, string algName, int k, float alpha, int rep) {
    string fileName = "../Exp/Results/" + algName + "_" + to_string(k) + "_" + to_string(int(alpha*10)) + ".txt";
    ofstream outMin (fileName);
    for(int i = 0; i < netGraph.n; i++)
        outMin << float(netGraph.prob[i])/rep << endl;
    outMin.close();
}

void writeOnFile(vector<float> results, string algName, float alpha, int k, int gap) {
    string fileName = "../Exp/Results/All_" + algName + "_" + to_string(int(alpha*10)) + "_min.txt";
    ofstream outMin (fileName);
    for(int i = 0; i <= k; i += gap)
        outMin << i << ": " << results[i/gap] << endl;
    outMin.close();
}
