#ifndef GENERATE_POINTS
#define GENERATE_POINTS

#include <vector>
#include <utility>

extern "C" {
#include "predicates.h"
};

#include "utils.h"

using namespace std;

vector<POINT> generatePointsInSquare(int n, REAL start, REAL end);

vector<POINT> generatePointsOnCircle(int n, REAL radius, POINT center);

vector<POINT> generatePointsOnLine(int n, REAL start, REAL end, POINT point1, POINT point2);

#endif //GENERATE_POINTS
