#include "utils.h"

double point1Array[2], point2Array[2], point3Array[2];

void pairToRealArray(POINT point, REAL *pointArray) {
    pointArray[0] = point.first;
    pointArray[1] = point.second;
}

double orient2dFastWrapper(POINT point1, POINT point2, POINT point3) {
    pairToRealArray(point1, point1Array);
    pairToRealArray(point2, point2Array);
    pairToRealArray(point3, point3Array);
    return orient2dfast(point1Array, point2Array, point3Array);
}

double orient2dExactWrapper(POINT point1, POINT point2, POINT point3) {
    pairToRealArray(point1, point1Array);
    pairToRealArray(point2, point2Array);
    pairToRealArray(point3, point3Array);
    return orient2dexact(point1Array, point2Array, point3Array);
}

double orient2dSlowWrapper(POINT point1, POINT point2, POINT point3) {
    pairToRealArray(point1, point1Array);
    pairToRealArray(point2, point2Array);
    pairToRealArray(point3, point3Array);
    return orient2dslow(point1Array, point2Array, point3Array);
}

double myOrient2d3(POINT point1, POINT point2, POINT point3) {
    return point1.first * point2.second
           + point1.second * point3.first
           + point2.first * point3.second
           - point2.second * point3.first
           - point1.second * point2.first
           - point1.first * point3.second;
}

double myOrient2d2(POINT point1, POINT point2, POINT point3) {
    return (point1.first - point3.first) * (point2.second - point3.second)
           - (point2.first - point3.first) * (point1.second - point3.second);
}
