#ifndef GRAPH_HPP
#define GRAPH_HPP

//Network Data Structure

// Adjacency List Node
struct AdjListNode
{
    int id;
    double p;
    struct AdjListNode *next;
};

// Adjacency List
struct AdjList
{
    struct AdjListNode *head;
};

// Class Graph
class Graph
{
  public:
    int n;
    int *degree, *in_degree;
    int *prob, *group;
    struct AdjList *neighbors;
    float *weight;

    Graph(int);
    AdjListNode *newAdjListNode(int, double);
    void addEdge(int src, int dest, double p);
    void printGraph();
};

#endif //GRAPH_HPP