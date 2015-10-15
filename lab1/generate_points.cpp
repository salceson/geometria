#include <random>
#include "generate_points.h"

vector<POINT> generatePointsInSquare(int n, REAL start, REAL end) {
    random_device randomDevice;
    mt19937 gen(randomDevice());
    uniform_real_distribution<REAL> dis(start, end);
    vector<POINT> points;

    for (int i = 0; i < n; ++i) {
        points.push_back(make_pair(dis(gen), dis(gen)));
    }

    return points;
}

vector<POINT> generatePointsOnCircle(int n, REAL radius, POINT center) {
    random_device randomDevice;
    mt19937 gen(randomDevice());
    uniform_real_distribution<REAL> dis(0, 2 * M_PI);
    vector<POINT> points;

    for (int i = 0; i < n; ++i) {
        REAL phi = dis(gen);
        points.push_back(make_pair(center.first + radius * cos(phi), center.second + radius * sin(phi)));
    }

    return points;
}

vector<POINT> generatePointsOnLine(int n, REAL start, REAL end, POINT point1, POINT point2) {
    random_device randomDevice;
    mt19937 gen(randomDevice());
    uniform_real_distribution<REAL> dis(start, end);
    vector<POINT> points;

    REAL a = (point2.second - point1.second) / (point2.first - point1.first);
    REAL b = point1.second - a * point1.first;

    for (int i = 0; i < n; ++i) {
        REAL x = dis(gen);
        points.push_back(make_pair(x, a * x + b));
    }

    return points;
}
