#include <iostream>
#include <vector>
#include "simulation.hpp"

using std::cout;
using std::endl;
using std::vector;

// Each rounds adds a seed: Min probable
vector<int> myopic(int init, int rep, int k, Graph &graph)
{

    vector<int> seeds;
    seeds.push_back(init);

    simRes result = simulation(seeds, rep, graph);

    for (int i = 2; i <= k; i++)
    {
        seeds.push_back(result.node);
        result = simulation(seeds, rep, graph);
    }

    return seeds;
}

// Add k Min Probables
vector<int> naiveMyopic(int init, int rep, int k, Graph &graph)
{
    int numV = graph.n;

    vector<int> seeds;
    seeds.push_back(init);

    simRes result = simulation(seeds, rep, graph);

    bool *isSeed = new bool[numV]{};
    isSeed[init] = true;
    int nextSeed = -1;
    float minPr;
    for (int i = 2; i <= k; i++)
    {
        minPr = rep + 1;
        for (int iter = 0; iter < numV; iter++)
            if (minPr > graph.prob[iter] && !isSeed[iter])
            {
                minPr = graph.prob[iter];
                nextSeed = iter;
            }
        seeds.push_back(nextSeed);
        isSeed[nextSeed] = true;

    }

    delete[] isSeed;
    return seeds;
}

// Each round adds a seed: That Increase the Min Probability the Most (true)
// Each round adds a seed: That Increase the Average Probability the Most (false)
vector<int> greedy_Reach(int init, int rep, int k, Graph &graph, bool obj)
{

    int numV = graph.n;

    vector<int> seeds;
    seeds.push_back(init);

    simRes result = simulation(seeds, rep, graph);

    bool *isSeed = new bool[numV]{};
    isSeed[init] = true;

    int candidate;
    float maxProb, temp;
    for (int i = 2; i <= k; i++)
    {
        candidate = -1;
        maxProb = -1;
        for (int r = 0; r < numV; r++)
        {
            if (isSeed[r])
                continue;
            seeds.push_back(r);
            result = simulation(seeds, rep, graph);
            if (obj)
                temp = result.minPr;
            else
                temp = result.avePr;
            if (temp > maxProb)
            {
                maxProb = temp;
                candidate = r;
            }
            seeds.pop_back();
        }
        seeds.push_back(candidate);
        isSeed[candidate] = true;
    }

    delete[] isSeed;
    return seeds;
}

// Adds k Seeds That Increase the Min Probability the Most (true)
// Adds k Seeds That Increase the Average Probability the Most (false)
vector<int> naiveGreedy_Reach(int init, int rep, int k, Graph &graph, bool obj)
{
    int numV = graph.n;

    vector<int> seeds;
    seeds.push_back(init);

    simRes result = simulation(seeds, rep, graph);

    bool *isSeed = new bool[numV]{};
    isSeed[init] = true;

    float *nextProbs = new float[numV]{};
    for (int i = 0; i < numV; i++)
    {
        if (isSeed[i])
            continue;
        seeds.push_back(i);
        result = simulation(seeds, rep, graph);
        if (obj)
            nextProbs[i] = result.minPr;
        else
            nextProbs[i] = result.avePr;
        seeds.pop_back();
    }

    int candidate = 0;
    float maxProb;
    for (int i = 2; i <= k; i++)
    {
        maxProb = 0;
        for (int r = 0; r < numV; r++)
        {
            if (isSeed[r])
                continue;
            if (maxProb < nextProbs[r])
            {
                maxProb = nextProbs[r];
                candidate = r;
            }
        }
        seeds.push_back(candidate);
        isSeed[candidate] = true;

        result = simulation(seeds, rep, graph);
    }

    delete[] isSeed;
    delete[] nextProbs;

    return seeds;
}
