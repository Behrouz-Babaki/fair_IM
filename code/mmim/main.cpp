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
void selectHeuristic(int, int, int, int, int, Graph);
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

    // string centerOption = "deg"; //Chooses the center
    // //cout << "Central close (cent), Max degree (deg), Min max dist (dist): ");
    // //cin >> option;
    int initSeed = pickCenter(netGraph, centerOption);
    cout << "Center: " << initSeed << endl;

    // //algDescription();
    // int alg; // Reads alg's Name
    // cout << "Enter alg's id: ";
    // cin >> alg;

    // //Set Simulation Variables
    // cout << "Enter variables: \nrep (1000), maxK (100), gap (5), minAlpha (0.1), maxAlpha (0.5)\n";
    // int rep, maxK, gap;
    // float minAlpha, maxAlpha;
    // cin >> rep >> maxK >> gap >> minAlpha >> maxAlpha;
    bool weightExp = false; //true;

    selectHeuristic(algorithm_id, initSeed, rep, k, gap, netGraph);

    // clock_t tAlph;
    // for (float alpha = minAlpha; alpha <= maxAlpha; alpha += 0.1)
    // {
    //     cout << "\n-----alpha = " << alpha << "-----\n";
    //     tAlph = clock();

    //     selectHeuristic(alg, initSeed, alpha, rep, maxK, gap, netGraph);

    //     cout << "Time: " << (float)(clock() - tAlph) / CLOCKS_PER_SEC << endl;
    // }
    // cout << "Time: " << (float)(clock() - tStart) / CLOCKS_PER_SEC << endl;

    return 0;
}

// Reads the network from file
// Format: Number of nodes - Direction of Graph ... Source - Destination
Graph readGraph(string file)
{
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

void selectHeuristic(int algID, int init, int rep, int k, int gap, Graph graph)
{
    vector<float> results;

    switch (algID)
    {
    case 1:
        results = random(init, rep, k, gap, graph);
        writeOnFile(results, "random", k, gap);
        break;
    case 2:
        results = max_deg(init, rep, k, gap, graph);
        writeOnFile(results, "maxdeg", k, gap);
        break;
    case 3:
        results = min_deg(init, rep, k, gap, graph);
        writeOnFile(results, "mindeg", k, gap);
        break;
    case 4:
        results = k_gonz(init, rep, k, gap, graph);
        writeOnFile(results, "gonzalez", k, gap);
        break;
    case 5:
        results = naiveMyopic(init, rep, k, gap, graph);
        writeOnFile(results, "naivemyopic", k, gap);
        break;
    case 6:
        results = myopic(init, rep, k, gap, graph);
        writeOnFile(results, "myopic", k, gap);
        break;
    case 7:
        results = naiveGreedy_Reach(init, rep, k, gap, graph, true);
        writeOnFile(results, "naivegreedy", k, gap);
        break;
    case 8:
        results = greedy_Reach(init, rep, k, gap, graph, true);
        writeOnFile(results, "greedy", k, gap);
        break;
    case 9:
        results = naiveGreedy_Reach(init, rep, k, gap, graph, false);
        writeOnFile(results, "naivereach", k, gap);
        break;
    case 10:
        results = greedy_Reach(init, rep, k, gap, graph, false);
        writeOnFile(results, "reach", k, gap);
    }
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
