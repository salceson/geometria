#include <random>
#include "generate_points.h"

vector<pair<REAL, REAL>> generatePoints(int n, long start, long end) {
    random_device randomDevice;
    mt19937 gen(randomDevice());
    uniform_real_distribution<REAL> dis(start, end);
    vector<pair<REAL, REAL>> points;

    for (int i = 0; i < n; ++i) {
        points.push_back(make_pair(dis(gen), dis(gen)));
    }

    return points;
}
