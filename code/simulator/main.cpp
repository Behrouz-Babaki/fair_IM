#include <iostream>
#include <vector>
#include <utility>
#include <queue>
#include <ctime>
#include <cstdlib>
#include <fstream>
#include <string>

#include "argh.hpp"

using std::cout;
using std::endl;
using std::make_pair;
using std::pair;
using std::queue;
using std::string;
using std::vector;

class Graph
{
  public:
    Graph(string);
    int n_nodes;
    int n_edges;
    vector<vector<pair<int, double>>> edges;
};

Graph::Graph(string filename)
{

    std::ifstream graph_file(filename);
    if (!graph_file.is_open())
    {
        cout << "error opening file " << filename << endl;
        exit(EXIT_FAILURE);
    }

    int num_nodes, num_edges;
    graph_file >> num_nodes >> num_edges;

    this->n_nodes = num_nodes;
    this->n_edges = num_edges;

    edges.assign(num_nodes, vector<pair<int, double>>());

    for (int i = 0; i < num_edges; i++)
    {
        int u, v;
        double p;
        graph_file >> u >> v >> p;
        edges[u].push_back(make_pair(v, p));
    }

    graph_file.close();
}

vector<double> simulate(const Graph &graph, const vector<int> &seeds, int n_reps)
{
    std::srand(std::time(nullptr));
    int n_nodes = graph.n_nodes;

    vector<double> hits(n_nodes, 0);
    vector<bool> is_active(n_nodes);
    queue<int> Q, empty_q;

    for (int i = 0; i < n_reps; i++)
    {

        is_active.assign(n_nodes, false);

        for (auto seed : seeds)
        {
            Q.push(seed);
            is_active[seed] = true;
        }

        while (!Q.empty())
        {
            int u = Q.front();
            Q.pop();

            for (auto edge : graph.edges[u])
            {
                int v = edge.first;
                if (is_active[v])
                    continue;

                double p = edge.second;
                double toss = ((double)(std::rand() % 1001)) / (double)1000;
                if (p >= toss)
                {
                    is_active[v] = true;
                    Q.push(v);
                }
            }
        }

        for (int u = 0; u < n_nodes; u++)
            if (is_active[u])
                hits[u]++;

        swap(Q, empty_q);
    }

    for (int i = 0; i < n_nodes; i++)
        hits[i] /= static_cast<double>(n_reps);

    return hits;
}

void print_usage()
{
    cout << "usage: simulate"
         << " --graph-file [GRAPH FILE]"
         << " --seed-file [SEED FILE]"
         << " --num-simulations [NUMBER OF SIMULATIONS]"
         << " --output-file [OUTPUT FILE]"
         << endl;
}

void write_results(vector<double> results, string filename)
{
    std::ofstream result_file(filename);
    if (!result_file.is_open())
    {
        cout << "error opening file " << filename << endl;
        exit(EXIT_FAILURE);
    }

    for (int i = 0, s = results.size(); i < s; i++)
        result_file << results[i] << endl;

    result_file.close();
}

vector<int> read_seeds(string filename)
{
    std::ifstream seed_file(filename);
    if (!seed_file.is_open())
    {
        cout << "error opening file " << filename << endl;
        exit(EXIT_FAILURE);
    }

    vector<int> seeds;
    int s;
    while (seed_file >> s)
        seeds.push_back(s);

    seed_file.close();
    return seeds;
}

int main(int argc, char **argv)
{

    argh::parser cmdl;
    cmdl.parse(argc, argv, argh::parser::PREFER_PARAM_FOR_UNREG_OPTION);
    string graph_file;
    string seed_file;
    string output_file;
    int num_simulations;
    if (!(cmdl({"-g", "--graph-file"}) >> graph_file) ||
        !(cmdl({"-s", "--seed-file"}) >> seed_file) ||
        !(cmdl({"-s", "--num-simulations"}) >> num_simulations) ||
        !(cmdl({"-o", "--output-file"}) >> output_file))
    {
        print_usage();
        exit(EXIT_FAILURE);
    }

    Graph graph(graph_file);
    vector<int> seeds = read_seeds(seed_file);
    vector<double> simulation_results = simulate(graph, seeds, num_simulations);

    write_results(simulation_results, output_file);
}
