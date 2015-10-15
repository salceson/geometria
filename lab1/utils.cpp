#include "utils.h"

REAL *pairToRealArray(pair<REAL, REAL> point) {
    REAL *pointArray = (REAL *) malloc(2 * sizeof(REAL));
    pointArray[0] = point.first;
    pointArray[1] = point.second;
    return pointArray;
}
