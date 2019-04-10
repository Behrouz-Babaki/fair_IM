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
using std::cout;
using std::endl;
using std::ifstream;
using std::string;
using std::vector;

Graph readGraph(string);
vector<float> run_heuristic(int, int, int, int, int, Graph);
void algDescription();

int main(int argc, char **argv)
{
    clock_t tStart = clock();

    argh::parser cmdl;
    cmdl.parse(argc, argv, argh::parser::PREFER_PARAM_FOR_UNREG_OPTION);

    string graph_file;
    string solution_file;
    int k;
    int algorithm_id;

    if (!(cmdl({"-g", "--graph-file"}) >> graph_file) ||
        !(cmdl({"-k", "--number-of-seeds"}) >> k) ||
        !(cmdl({"-a", "--algorithm-id"}) >> algorithm_id) ||
        !(cmdl({"-o", "--solution-file"}) >> solution_file))
    {
        cout << "Usage: " << argv[0]
             << " --graph-file GRAPH-FILE"
             << " --number-of-seeds K"
             << " --solution-file SOLUTION-FILE"
             << " --algorithm-id ID"
             << " [--gap GAP (5)]"
             << " [--number-of-simulations REP (1000)]"
             << " [--center-option OPTION (deg)]"
             << endl;
        cout << "Description of algorithms:" << endl;
        algDescription();
        exit(EXIT_FAILURE);
    }

    string centerOption;
    cmdl({"-c", "--center-option"}, "deg") >> centerOption;
    int gap;
    cmdl({"-g", "--gap"}, 5) >> gap;
    int rep;
    cmdl({"-r", "--number-of-simulations"}, 1000) >> rep;

    // Loads data in the graph
    Graph netGraph = readGraph(graph_file);
    int initSeed = pickCenter(netGraph, centerOption);
    cout << "Center: " << initSeed << endl;

    bool weightExp = false; //true;

    vector<float> results = run_heuristic(algorithm_id, initSeed, rep, k, gap, netGraph);
    writeOnFile(results, solution_file, k, gap);

    return 0;
}

// Reads the network from file
// Format:
// number-of-nodes number-of-edges
// source destination edge-probability
// ...
// source destination edge-probability
Graph readGraph(string file)
{
    ifstream input;
    input.open(file);

    int numV, numE;
    input >> numV >> numE; // number of nodes and edges
    cout << "number of nodes: " << numV << "\n"
         << "number of edges: " << numE << endl;
    Graph netGraph(numV);

    int from, to;
    double p;
    while (input >> from >> to >> p)
        netGraph.addEdge(int(from), int(to), p);
    input.close();

    return netGraph;
}

vector<float> run_heuristic(int algID, int init, int rep, int k, int gap, Graph graph)
{
    vector<float> results;

    switch (algID)
    {
    case 1:
        results = random(init, rep, k, gap, graph);
        break;
    case 2:
        results = max_deg(init, rep, k, gap, graph);
        break;
    case 3:
        results = min_deg(init, rep, k, gap, graph);
        break;
    case 4:
        results = k_gonz(init, rep, k, gap, graph);
        break;
    case 5:
        results = naiveMyopic(init, rep, k, gap, graph);
        break;
    case 6:
        results = myopic(init, rep, k, gap, graph);
        break;
    case 7:
        results = naiveGreedy_Reach(init, rep, k, gap, graph, true);
        break;
    case 8:
        results = greedy_Reach(init, rep, k, gap, graph, true);
        break;
    case 9:
        results = naiveGreedy_Reach(init, rep, k, gap, graph, false);
        break;
    case 10:
        results = greedy_Reach(init, rep, k, gap, graph, false);
    }

    return results;
}

void algDescription()
{
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
