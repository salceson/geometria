#ifndef UTILS_H
#define UTILS_H

#include <utility>

extern "C" {
#include "predicates.h"
};

#include <cstdlib>

using namespace std;

REAL *pairToRealArray(std::pair<REAL, REAL> point);

#endif //UTILS_H
