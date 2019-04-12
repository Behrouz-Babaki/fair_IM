#!/bin/bash

../build/mingap                         \
    --graph-file karate.txt             \
    --number-of-seeds 5                 \
    --solution-file karate.out          \
    --algorithm random
