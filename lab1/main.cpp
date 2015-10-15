#include <iostream>

extern "C" {
#include "predicates.h"
};

#include "utils.h"
#include "generate_points.h"

#define POINTS_NUM 1500

using namespace std;

int main(int argc, char **argv) {
    exactinit();

    vector<pair<REAL, REAL>> points = generatePoints(POINTS_NUM, 0, 1);

    for (auto point : points) {
        cout << point.first << " " << point.second << endl;
    }

    return 0;
}
