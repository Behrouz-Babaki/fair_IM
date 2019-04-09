// Distance of every node to its nearest source
// Finds the first source using differenct approaches

#ifndef computation_h
#define computation_h

#include <queue>

// Returns distance of every nodes from nearest source
int* calcDist(vector<int>& seeds, Graph& g) {
    // Breadth First Search (BFS)
    int numb_v = g.n;
    int* dist = new int [numb_v]{};
    bool* isVisit = new bool [numb_v]{};
    queue<int> bfs, empty;
    
    // Initialize
    for(int i = 0; i < seeds.size(); i++) {
        isVisit[seeds[i]] = true;
        bfs.push(seeds[i]);
    }
    
    int rounds = 1, lastNode = bfs.front();
    AdjListNode* iter;
    // Runs until there's no node to see
    while(!bfs.empty()) {
        iter = g.neighbors[bfs.front()].head;// Neighbors of them
        while(iter) {
            if(isVisit[iter->id]) { iter = iter->next; continue; }
            isVisit[iter->id] = true;
            dist[iter->id] = rounds;
            bfs.push(iter->id);
            iter = iter->next;
        }
        if(bfs.front() == lastNode) {
            lastNode = bfs.back();
            rounds++;
        }
        bfs.pop();
    }
    
    swap(bfs, empty);
    delete[] isVisit;
    return dist;
}

// Deg: node with Max Degree
// Dist: node with Min Max Distance
// Cent: node with Min Average Distance from all
int pickCenter(Graph& g, string option) {
    int init = 0, numV = g.n;
    
    if(option == "deg") {
        int maxDeg = 0;
        for(int node = 0; node < numV; node++)
            if(g.degree[node] >= maxDeg) {
                maxDeg = g.degree[node];
                init = node;
            }
        return init;
    }
    
    //Breadth First Search (BFS)
    queue<int> bfs, empty;
    bool* isVisit = new bool[numV];
    int* maxDist = new int[numV]{};
    int* totalDist = new int[numV]{};
    AdjListNode* iter;
    
    int rounds, lastNode;
    // Computes for each node:
    for(int s = 0; s < numV; s++) {
        isVisit = {};
        isVisit[s] = true;
        swap(bfs, empty);
        bfs.push(s);
        
        rounds = 1;
        lastNode = bfs.front();
        // Runs until all nodes are seen
        while(!bfs.empty()) {
            iter = g.neighbors[bfs.front()].head;// Neighbors of them
            while(iter) {
                if(isVisit[iter->id]) { iter = iter->next; continue; }
                isVisit[iter->id] = true;
                totalDist[s] += rounds;
                bfs.push(iter->id);
            }
            if(bfs.front() == lastNode) {
                lastNode = bfs.back();
                rounds++;
            }
            bfs.pop();
        }
        maxDist[s] = rounds-1;
    }
    
    //Find the Min
    if(option == "dist") {
        int minim = maxDist[0];
        for(int i = 1; i < numV; i++)
            if(minim > maxDist[i]) {
                minim = maxDist[i];
                init = i;
            }
    }
    if(option == "cent") {
        int minim = totalDist[0];
        for(int i = 1; i < numV; i++)
            if(minim > totalDist[i]) {
                minim = totalDist[i];
                init = i;
            }
    }
    
    swap(bfs, empty);
    delete[] isVisit;
    delete[] maxDist;
    delete[] totalDist;
    return init;
}

#endif /* computation_h */
