#include <iostream>
#include <random>
#include <climits>
#include "graph.hpp"

using std::cout;
using std::endl;
using std::random_device;
using std::mt19937;
using std::uniform_int_distribution;

Graph::Graph(int n)
{
    this->n = n;
    degree = new int[n];
    in_degree = new int[n];
    prob = new int[n];
    weight = new float[n];
    group = new int[n];
    neighbors = new AdjList[n];
    for (int i = 0; i < n; ++i)
    {
        neighbors[i].head = NULL;
        degree[i] = in_degree[i] = prob[i] = 0;
        weight[i] = 1;
        group[i] = 1;
    }
}

void Graph::setRand()
{
    random_device rand_dev;
    mt19937 generator(rand_dev());
    uniform_int_distribution<int> distrW(0, INT_MAX);
    uniform_int_distribution<int> distrG(0, 1);

    for (int i = 0; i < n; ++i)
    {
        weight[i] = (float)distrW(generator) / INT_MAX;
        group[i] = distrG(generator);
        uniform_int_distribution<int> distrT(0, in_degree[i]);
    }
}

AdjListNode *Graph::newAdjListNode(int id)
{
    AdjListNode *newNode = new AdjListNode;
    newNode->id = id;
    newNode->next = NULL;
    return newNode;
}

void Graph::addEdge(int src, int dest, bool dir)
{
    degree[src]++;
    in_degree[dest]++;
    AdjListNode *newNode = newAdjListNode(dest);
    newNode->next = neighbors[src].head;
    neighbors[src].head = newNode;
    if (dir)
    {
        return;
    }
    degree[dest]++;
    newNode = newAdjListNode(src);
    newNode->next = neighbors[dest].head;
    neighbors[dest].head = newNode;
}

void Graph::printGraph()
{
    for (int v = 0; v < n; ++v)
    {
        AdjListNode *iter = neighbors[v].head;
        cout << "Vertex " << v << ":";
        while (iter)
        {
            cout << " " << iter->id;
            iter = iter->next;
        }
        cout << endl;
    }
}
