// Information spreads from source nodes (seeds), over the network (IC model)
// Different heuristic implemented for choosing seeds to "Maximize the Minimum Probablity"

#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include "argh.hpp"
#include "graph.hpp"
#include "algorithms.hpp"
#include "greedy.hpp"
#include "computation.hpp"

using std::cin;
using std::cout;
using std::endl;
using std::ifstream;
using std::ofstream;
using std::string;
using std::vector;

Graph readGraph(string);
vector<int> run_heuristic(string, int, int, int, int, Graph);
void writeOnFile(vector<int> results, string prob_filename);
void print_usage();

int main(int argc, char **argv)
{
    clock_t tStart = clock();

    argh::parser cmdl;
    cmdl.parse(argc, argv, argh::parser::PREFER_PARAM_FOR_UNREG_OPTION);

    string graph_file;
    string solution_file;
    int k;
    string algorithm;

    if (!(cmdl({"-g", "--graph-file"}) >> graph_file) ||
        !(cmdl({"-k", "--number-of-seeds"}) >> k) ||
        !(cmdl({"-a", "--algorithm"}) >> algorithm) ||
        !(cmdl({"-o", "--solution-file"}) >> solution_file))
    {
        print_usage();
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

    vector<int> results = run_heuristic(algorithm, initSeed, rep, k, gap, netGraph);
    writeOnFile(results, solution_file);

    return 0;
}

/*
 Reads the network from file

 Format:
 ====================================
 number-of-nodes number-of-edges
 source destination edge-probability
 ...
 source destination edge-probability
 =====================================
*/
Graph readGraph(string file)
{
    ifstream input;
    input.open(file);

    int numV, numE;
    input >> numV >> numE; // number of nodes and edges
    Graph netGraph(numV);

    int from, to;
    double p;
    while (input >> from >> to >> p)
        netGraph.addEdge(int(from), int(to), p);
    input.close();

    return netGraph;
}

vector<int> run_heuristic(string algorithm, int init, int rep, int k, int gap, Graph graph)
{
    vector<int> results;

    if (algorithm == "random")
        results = random(init, rep, k, gap, graph);
    else if (algorithm == "max-degree")
        results = max_deg(init, rep, k, gap, graph);
    else if (algorithm == "min-degree")
        results = min_deg(init, rep, k, gap, graph);
    else if (algorithm == "Gonzalez")
        results = k_gonz(init, rep, k, gap, graph);
    else if (algorithm == "naive-myopic")
        results = naiveMyopic(init, rep, k, gap, graph);
    else if (algorithm == "myopic")
        results = myopic(init, rep, k, gap, graph);
    else if (algorithm == "naive-greedy")
        results = naiveGreedy_Reach(init, rep, k, gap, graph, true);
    else if (algorithm == "greedy")
        results = greedy_Reach(init, rep, k, gap, graph, true);
    else if (algorithm == "naive-reach")
        results = naiveGreedy_Reach(init, rep, k, gap, graph, false);
    else if (algorithm == "reach")
        results = greedy_Reach(init, rep, k, gap, graph, false);
    else
    {
        cout << algorithm << "is not a valid algorithm" << endl;
        print_usage();
        exit(EXIT_FAILURE);
    }

    return results;
}

void writeOnFile(vector<int> results, string prob_filename)
{
    ofstream outMin(prob_filename);
    for (int i = 1, k = results.size(); i <= k; i++)
        outMin << results[i] << endl;
    outMin.close();
}

void print_usage()
{
    cout << "Usage: "
         << "mmim "
         << " --graph-file GRAPH-FILE"
         << " --number-of-seeds K"
         << " --solution-file SOLUTION-FILE"
         << " --algorithm ALG"
         << " [--gap GAP (5)]"
         << " [--number-of-simulations REP (1000)]"
         << " [--center-option OPTION (deg)]"
         << endl;
    cout << "Description of algorithms:" << endl;
    cout << "'random':\n Randomly chooses k nodes" << endl;
    cout << "'max-degree':\n Picks k nodes with maximum degrees" << endl;
    cout << "'min-degree':\n Picks k nodes with minimum degrees" << endl;
    cout << "'Gonzalez':\n Each time pich the furthest node from sources -- repeat" << endl;
    cout << "'naive-myopic':\n Runs Simulation -- Picks k min probable nodes" << endl;
    cout << "'myopic':\n Runs Simulation -- Picks the min probable node -- repeat" << endl;
    cout << "'naive-greedy':\n Runs Simulation -- Picks the k nodes that increases min probability the most" << endl;
    cout << "'greedy':\n Runs Simulation -- Picks the node that increases min probability the most -- repeat" << endl;
    cout << "'naive-reach':\n Runs Simulation -- Picks the k nodes that increases average probability the most" << endl;
    cout << "'reach':\n Runs Simulation -- Picks the node that increases average probability the most -- repeat" << endl;
}
