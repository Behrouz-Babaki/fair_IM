#include <iostream>
#include <random>
#include <climits>
#include "graph.hpp"

using std::cout;
using std::endl;

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

AdjListNode *Graph::newAdjListNode(int id, double p)
{
    AdjListNode *newNode = new AdjListNode;
    newNode->id = id;
    newNode->next = NULL;
    return newNode;
}

void Graph::addEdge(int src, int dest, double p)
{
    degree[src]++;
    in_degree[dest]++;
    AdjListNode *newNode = newAdjListNode(dest, p);
    newNode->next = neighbors[src].head;
    neighbors[src].head = newNode;
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
