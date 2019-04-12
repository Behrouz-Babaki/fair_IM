#include <iostream>
#include <vector>
#include "algorithms.hpp"
#include "simulation.hpp"
#include "computation.hpp"

using std::cout;
using std::endl;
using std::vector;

// Adds K random centers to the seeds
vector<int> random(int init, int rep, int k, int gap, Graph &graph)
{
    int numV = graph.n;

    vector<int> seeds;
    seeds.push_back(init);

    bool *isSeed = new bool[numV]{};
    isSeed[init] = true;

    srand(static_cast<unsigned int>(time(NULL)));

    int nextRand;
    for (int i = 2; i <= k; i++)
    {
        nextRand = (rand() % numV);
        //nextRand = distr(generator);
        while (isSeed[nextRand])
        {
            nextRand++;
            if (nextRand == numV)
                nextRand = 0;
        }
        seeds.push_back(nextRand);
        isSeed[nextRand] = true;
    }

    delete[] isSeed;
    return seeds;
}

// Each round adds a seed: that is connected to the most number of nodes
vector<int> max_deg(int init, int rep, int k, int gap, Graph &graph)
{
    int numV = graph.n;

    vector<int> seeds;
    seeds.push_back(init);

    bool *isSeed = new bool[numV]{};
    isSeed[init] = true;

    int maxDegree, nextMax = 0;
    for (int i = 2; i <= k; i++)
    {
        maxDegree = 0;
        for (int node = 0; node < numV; node++)
        {
            if (isSeed[node])
                continue;

            if (graph.degree[node] >= maxDegree)
            {
                maxDegree = graph.degree[node];
                nextMax = node;
            }
        }
        seeds.push_back(nextMax);
        isSeed[nextMax] = true;
    }

    delete[] isSeed;
    return seeds;
}

// Each round adds a seed: that is connected to the most number of non-seed nodes
vector<int> max_deg_adv(int init, int rep, int k, int gap, Graph &graph)
{
    int numV = graph.n;

    vector<int> seeds;
    seeds.push_back(init);

    bool *isSeed = new bool[numV]{};
    isSeed[init] = true;

    int maxDegree, minSeed, nextMax = 0;
    int seedDeg;
    AdjListNode *iter;
    for (int i = 2; i <= k; i++)
    {
        maxDegree = 0;
        minSeed = numV;
        for (int node = 0; node < numV; node++)
        {
            if (isSeed[node])
                continue;

            seedDeg = 0;
            iter = graph.neighbors[node].head;
            while (iter)
            {
                if (isSeed[iter->id])
                    seedDeg++;
                iter = iter->next;
            }

            if (seedDeg < minSeed)
            {
                minSeed = seedDeg;
                maxDegree = graph.degree[node] - seedDeg;
                nextMax = node;
            }
            else if (seedDeg == minSeed)
            {
                if (graph.degree[node] - seedDeg > maxDegree)
                {
                    maxDegree = graph.degree[node] - seedDeg;
                    nextMax = node;
                }
            }
        }
        seeds.push_back(nextMax);
        isSeed[nextMax] = true;
    }

    delete[] isSeed;
    return seeds;
}

// Each round adds a seed: that is connected to the most number of nodes
vector<int> min_deg(int init, int rep, int k, int gap, Graph &graph)
{
    int numV = graph.n;

    vector<int> seeds;
    seeds.push_back(init);

    bool *isSeed = new bool[numV]{};
    isSeed[init] = true;

    int minDegree, nextMin = 0;
    for (int i = 2; i <= k; i++)
    {
        minDegree = numV;
        for (int node = 0; node < numV; node++)
        {
            if (isSeed[node])
                continue;
            if (graph.degree[node] <= minDegree)
            {
                minDegree = graph.degree[node];
                nextMin = node;
            }
        }
        seeds.push_back(nextMin);
        isSeed[nextMin] = true;
    }

    delete[] isSeed;
    return seeds;
}

// Each round adds a seed: that is connected to the least number of seed nodes and then least number of non-seed nodes
vector<int> min_deg_adv(int init, int rep, int k, int gap, Graph &graph)
{
    int numV = graph.n;

    vector<int> seeds;
    seeds.push_back(init);

    bool *isSeed = new bool[numV]{};
    isSeed[init] = true;

    int minDegree, minSeed, nextMin = 0;
    int seedDeg;
    AdjListNode *iter;
    for (int i = 2; i <= k; i++)
    {
        minDegree = minSeed = numV;
        for (int node = 0; node < numV; node++)
        {
            if (isSeed[node])
                continue;

            seedDeg = 0;
            iter = graph.neighbors[node].head;
            while (iter)
            {
                if (isSeed[iter->id])
                    seedDeg++;
                iter = iter->next;
            }

            if (seedDeg < minSeed)
            {
                minSeed = seedDeg;
                minDegree = graph.degree[node] - seedDeg;
                nextMin = node;
            }
            else if (seedDeg == minSeed)
            {
                if (graph.degree[node] - seedDeg < minDegree)
                {
                    minDegree = graph.degree[node] - seedDeg;
                    nextMin = node;
                }
            }
        }
        seeds.push_back(nextMin);
        isSeed[nextMin] = true;
    }

    delete[] isSeed;
    return seeds;
}

// K-center: Minimize distance from seeds
// Gonzalez Algorithm
// Each round adds the furthest point to centers
vector<int> k_gonz(int init, int rep, int k, int gap, Graph graph)
{
    int numV = graph.n;

    vector<int> seeds;
    seeds.push_back(init);

    bool *isSeed = new bool[numV]{};
    isSeed[init] = true;

    int *dist = new int[numV];
    int maxDist, furthest = 0;

    for (int i = 2; i <= k; i++)
    {
        maxDist = 0;
        dist = calcDist(seeds, graph);
        for (int node = 0; node < numV; node++)
        {
            if (isSeed[node])
                continue;

            if (dist[node] > maxDist)
            {
                furthest = node;
                maxDist = dist[node];
            }
        }

        seeds.push_back(furthest);
        isSeed[furthest] = true;
    }

    delete[] isSeed;
    delete[] dist;
    return seeds;
}
