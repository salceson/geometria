#ifndef UTILS_H
#define UTILS_H

#include <utility>

extern "C" {
#include "predicates.h"
};

#include <cstdlib>

using namespace std;

typedef pair<REAL, REAL> POINT;

typedef double (*OrientationFunction)(POINT, POINT, POINT);

void pairToRealArray(POINT point, REAL *pointArray);

double orient2dFastWrapper(POINT point1, POINT point2, POINT point3);

double orient2dExactWrapper(POINT point1, POINT point2, POINT point3);

double orient2dSlowWrapper(POINT point1, POINT point2, POINT point3);

double myOrient2d3(POINT point1, POINT point2, POINT point3);

double myOrient2d2(POINT point1, POINT point2, POINT point3);


#endif //UTILS_H
