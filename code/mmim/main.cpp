// Information spreads from source nodes (seeds), over the network (IC model)
// Different heuristic implemented for choosing seeds to "Maximize the Minimum Probablity"

//configuration - libraries it include
//generate make file

#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include "argh.hpp"
#include "graph.hpp"
#include "algorithms.hpp"
#include "greedy.hpp"
#include "computation.hpp"
#include "print.hpp"

using std::cin;
using std::ifstream;
using std::cout;
using std::endl;
using std::string;
using std::vector;

Graph readGraph(string);
void selectHeuristic(int, int, float, int, int, int, Graph);
void algDescription();

int main() {
    clock_t tStart = clock();
    
    // Reads file's Name
    string fileName;
    cout << "Enter file's name: ";
    cin >> fileName;
    
    // Loads data in the graph
    Graph netGraph = readGraph(fileName);
    
    string centerOption = "deg"; //Chooses the center
    //cout << "Central close (cent), Max degree (deg), Min max dist (dist): ");
    //cin >> option;
    int initSeed = pickCenter(netGraph, centerOption);
    cout << "Center: " << initSeed << endl;
    
    //algDescription();
    int alg; // Reads alg's Name
    cout << "Enter alg's id: ";
    cin >> alg;
    
    //Set Simulation Variables
    cout << "Enter variables: \nrep (1000), maxK (100), gap (5), minAlpha (0.1), maxAlpha (0.5)\n";
    int rep, maxK, gap;
    float minAlpha, maxAlpha;
    cin >> rep >> maxK >> gap >> minAlpha >> maxAlpha;
    bool weightExp = false;//true;
    
    clock_t tAlph;
    for(float alpha = minAlpha; alpha <= maxAlpha; alpha += 0.1) {
        cout << "\n-----alpha = " << alpha << "-----\n";
        tAlph = clock();
        
        selectHeuristic(alg, initSeed, alpha, rep, maxK, gap, netGraph);
        
        cout << "Time: " << (float)(clock() - tAlph)/CLOCKS_PER_SEC << endl;
    }
    cout << "Time: " << (float)(clock() - tStart)/CLOCKS_PER_SEC << endl;
    
    return 0;
}

// Reads the network from file
// Format: Number of nodes - Direction of Graph ... Source - Destination
Graph readGraph(string file) {
    ifstream input;
    input.open(file);
    
    int numV;
    input >> numV; // Number of Nodes
    cout << "Number of Nodes: " << numV << endl;
    Graph netGraph(numV);
    
    //TODO remove this flag
    bool dir;
    input >> dir; // 0: Undirecrted, 1: Directed
    
    int from, to;
    double p;
    while (input >> from >> to >> p)
        netGraph.addEdge(int(from), int(to), p, dir);
    input.close();
    
    return netGraph;
}

void selectHeuristic(int algID, int init, float alpha, int rep, int k, int gap, Graph graph) {
    vector<float> results;
    
    switch(algID) {
        case 1:
            results = random(init, alpha, rep, k, gap, graph);
            writeOnFile(results, "random", alpha, k, gap);
            break;
        case 2:
            results = max_deg(init, alpha, rep, k, gap, graph);
            writeOnFile(results, "maxdeg", alpha, k, gap);
            break;
        case 3:
            results = min_deg(init, alpha, rep, k, gap, graph);
            writeOnFile(results, "mindeg", alpha, k, gap);
            break;
        case 4:
            results = k_gonz(init, alpha, rep, k, gap, graph);
            writeOnFile(results, "gonzalez", alpha, k, gap);
            break;
        case 5:
            results = naiveMyopic(init, alpha, rep, k, gap, graph);
            writeOnFile(results, "naivemyopic", alpha, k, gap);
            break;
        case 6:
            results = myopic(init, alpha, rep, k, gap, graph);
            writeOnFile(results, "myopic", alpha, k, gap);
            break;
        case 7:
            results = naiveGreedy_Reach(init, alpha, rep, k, gap, graph, true);
            writeOnFile(results, "naivegreedy", alpha, k, gap);
            break;
        case 8:
            results = greedy_Reach(init, alpha, rep, k, gap, graph, true);
            writeOnFile(results, "greedy", alpha, k, gap);
            break;
        case 9:
            results = naiveGreedy_Reach(init, alpha, rep, k, gap, graph, false);
            writeOnFile(results, "naivereach", alpha, k, gap);
            break;
        case 10:
            results = greedy_Reach(init, alpha, rep, k, gap, graph, false);
            writeOnFile(results, "reach", alpha, k, gap);
    }
}

void algDescription() {
    cout << "--- \nEnter 1 for 'Random':\n Randomly chooses k nodes" << endl;
    cout << "Enter 2 for 'Max Degree':\n Picks k nodes with maximum degrees" << endl;
    cout << "Enter 3 for 'Min Degree':\n Picks k nodes with minimum degrees" << endl;
    cout << "Enter 4 for 'Gonzalez':\n Each time pich the furthest node from sources -- repeat" << endl;
    cout << "Enter 5 for 'Naive Myopic':\n Runs Simulation -- Picks k min probable nodes" << endl;
    cout << "Enter 6 for 'Myopic':\n Runs Simulation -- Picks the min probable node -- repeat" << endl;
    cout << "Enter 7 for 'Naive Greedy':\n Runs Simulation -- Picks the k nodes that increases min probability the most" << endl;
    cout << "Enter 8 for 'Greedy':\n Runs Simulation -- Picks the node that increases min probability the most -- repeat" << endl;
    cout << "Enter 9 for 'Naive Reach':\n Runs Simulation -- Picks the k nodes that increases average probability the most" << endl;
    cout << "Enter 10 for 'Reach':\n Runs Simulation -- Picks the node that increases average probability the most -- repeat" << endl;
}
