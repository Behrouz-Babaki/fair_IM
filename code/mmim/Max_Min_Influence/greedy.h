// Greedy Heuristics: ...

#ifndef min_hill_h
#define min_hill_h

//#include <time.h> //#include <iostream> //#include <vector> //#include <algorithm>
#include "simulation.h"
#include "print.h"

using namespace std;

// Each rounds adds a seed: Min probable
vector<float> myopic(int init, float alpha, int rep, int k, int gap, Graph& graph) {
    cout << "\n===Myopic===\n";
    clock_t t = clock();
    
    vector<int> seeds;
    vector<float> output;
    seeds.push_back(init);
    
    simRes result = simulation(seeds, alpha, rep, graph);
    output.push_back(result.minPr);
    printProbs(graph, "myopic", 1, alpha, rep);
    cout << "Seed #1: " << init << endl;
    cout << "\nMin node: " << result.node << " -- prob: " << result.minPr << endl;
    
    for(int i = 2; i <= k; i++) {
        seeds.push_back(result.node);
        result = simulation(seeds, alpha, rep, graph);
        cout << "Seed #" << i << ": " << result.node << " -- prob " << result.minPr << endl;
        
        if(i % gap == 0) {
            output.push_back(result.minPr);
            printProbs(graph, "myopic", i, alpha, rep);
            cout << "\nMin node: " << result.node << " -- prob: " << result.minPr << endl;
            cout << "... Time: " << (float)(clock() - t)/CLOCKS_PER_SEC << endl << endl;
            t = clock();
        }
    }
    
    vector<int>().swap(seeds);
    return output;
}

// Add k Min Probables
vector<float> naiveMyopic(int init, float alpha, int rep, int k, int gap, Graph& graph) {
    cout << "\n ===Naive Myopic===\n";
    clock_t t = clock();
    
    int numV = graph.n;
    
    vector<int> seeds;
    vector<float> output;
    seeds.push_back(init);
    
    simRes result = simulation(seeds, alpha, rep, graph);
    output.push_back(result.minPr);
    printProbs(graph, "naivemyopic", 1, alpha, rep);
    cout << "Seed #1: " << init << endl;
    cout << "\nMin node: " << result.node << " -- prob: " << result.minPr << endl;
    
    bool* isSeed = new bool [numV]{};
    isSeed[init] = true;
    int nextSeed = 0;
    float minPr;
    for(int i = 2; i <= k; i++) {
        minPr = rep;
        for(int iter = 0; iter < numV; iter++)
            if(minPr > graph.prob[iter] && !isSeed[iter]) {
                minPr = graph.prob[iter];
                nextSeed = iter;
            }
        seeds.push_back(nextSeed);
        isSeed[nextSeed] = true;
        cout << "Seed #" << i << ": " << nextSeed << " -- prob " << float(minPr)/numV <<endl;
        
        if(i % gap == 0) {
            result = simulation(seeds, alpha, rep, graph);
            output.push_back(result.minPr);
            printProbs(graph, "naivemyopic", i, alpha, rep);
            cout << "\nMin node: " << result.node << " -- prob: " << result.minPr << endl;
            cout << "... Time: " << (float)(clock() - t)/CLOCKS_PER_SEC << endl << endl;
            t = clock();
        }
    }
    
    delete[] isSeed;
    vector<int>().swap(seeds);
    return output;
}

// Each round adds a seed: That Increase the Min Probability the Most (true)
// Each round adds a seed: That Increase the Average Probability the Most (false)
vector<float> greedy_Reach(int init, float alpha, int rep, int k, int gap, Graph& graph, bool obj) {
    if(obj) cout << "\n ===Greedy===\n";
    else cout << "\n ===Reach===\n";
    clock_t t = clock();
    
    int numV = graph.n;
    
    vector<int> seeds;
    vector<float> output;
    seeds.push_back(init);
    
    simRes result = simulation(seeds, alpha, rep, graph);
    output.push_back(result.minPr);
    if(obj) printProbs(graph, "greedy", 1, alpha, rep);
    else printProbs(graph, "reach", 1, alpha, rep);
    cout << "Seed #1: " << init << endl;
    cout << "\nMin node: " << result.node << " -- prob: " << result.minPr << endl;
    
    bool* isSeed = new bool [numV]{};
    isSeed[init] = true;
    
    int candidate;
    float maxProb, temp;
    for(int i = 2; i <= k; i++) {
        candidate = 0;
        maxProb = 0;
        for(int r = 0; r < numV; r++) {
            if(isSeed[r]) continue;
            seeds.push_back(r);
            result = simulation(seeds, alpha, rep, graph);
            if(obj) temp = result.minPr;
            else temp = result.avePr;
            if(temp > maxProb) {
                maxProb = temp;
                candidate = r;
            }
            seeds.pop_back();
        }
        seeds.push_back(candidate);
        isSeed[candidate] = true;
        cout << "Seed #" << i << ": " << candidate << " -- prob " << result.minPr << endl;
        
        if(i % gap == 0) {
            result = simulation(seeds, alpha, rep, graph);
            output.push_back(result.minPr);
            if(obj) printProbs(graph, "greedy", i, alpha, rep);
            else printProbs(graph, "reach", i, alpha, rep);
            cout << "\nMin node: " << result.node << " -- next prob: " << result.minPr << endl;
            cout << "... Time: " << (float)(clock() - t)/CLOCKS_PER_SEC << endl << endl;
            t = clock();
        }
    }
    
    delete[] isSeed;
    vector<int>().swap(seeds);
    return output;
}

// Adds k Seeds That Increase the Min Probability the Most (true)
// Adds k Seeds That Increase the Average Probability the Most (false)
vector<float> naiveGreedy_Reach(int init, float alpha, int rep, int k, int gap, Graph& graph, bool obj) {
    if(obj) cout << "\n ===Naive Greedy===\n";
    else cout << "\n ===Naive Reach===\n";
    clock_t t = clock();
    
    int numV = graph.n;
    
    vector<int> seeds;
    vector<float> output;
    seeds.push_back(init);
    
    simRes result = simulation(seeds, alpha, rep, graph);
    output.push_back(result.minPr);
    if(obj) printProbs(graph, "naivegreedy", 1, alpha, rep);
    else printProbs(graph, "naivereach", 1, alpha, rep);
    cout << "Seed #1: " << init << endl;
    cout << "\nMin node: " << result.node << " -- prob: " << result.minPr << endl;
    
    bool* isSeed = new bool [numV]{};
    isSeed[init] = true;
    
    float* nextProbs = new float [numV]{};
    for(int i = 0; i < numV; i++) {
        if(isSeed[i]) continue;
        seeds.push_back(i);
        result = simulation(seeds, alpha, rep, graph);
        if(obj) nextProbs[i] = result.minPr;
        else nextProbs[i] = result.avePr;
        seeds.pop_back();
    }
    
    int candidate = 0;
    float maxProb;
    for(int i = 2; i <= k; i++) {
        maxProb = 0;
        for(int r = 0; r < numV; r++) {
            if(isSeed[r]) continue;
            if(maxProb < nextProbs[r]) {
                maxProb = nextProbs[r];
                candidate = r;
            }
        }
        seeds.push_back(candidate);
        isSeed[candidate] = true;
        cout << "Seed #" << i << ": " << candidate << " -- next prob " << maxProb << endl;
        
        if(i % gap == 0) {
            result = simulation(seeds, alpha, rep, graph);
            output.push_back(result.minPr);
            if(obj) printProbs(graph, "naivegreedy", i, alpha, rep);
            else printProbs(graph, "naivereach", i, alpha, rep);
            cout << "\nMin node: " << result.node << " -- prob: " << result.minPr << endl;
            cout << "... Time: " << (float)(clock() - t)/CLOCKS_PER_SEC << endl << endl;
            t = clock();
        }
    }
    
    delete[] isSeed;
    delete[] nextProbs;
    vector<int>().swap(seeds);
    return output;
}

#endif /* min_hill_h */
