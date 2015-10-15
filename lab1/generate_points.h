#ifndef GENERATE_POINTS
#define GENERATE_POINTS

#include <vector>
#include <utility>

extern "C" {
#include "predicates.h"
};

using namespace std;

vector<pair<REAL, REAL>> generatePoints(int n, long start, long end);

#endif //GENERATE_POINTS
