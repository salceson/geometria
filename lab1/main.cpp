#include <iostream>
#include <cstring>
#include <fstream>

extern "C" {
#include "predicates.h"
};

#include "utils.h"
#include "generate_points.h"

using namespace std;

void usage() {
    cerr << "Usage: " << endl;
    cerr << "\t* to generate points in square: ./lab1 generate1 <n> <start> <end> <filename>" << endl;
    cerr << "\t* to generate points on circle: ./lab1 generate2 <n> <center_x>"
            " <center_y> <radius> <filename>" << endl;
    cerr << "\t* to generate points on line: ./lab1 generate3 <n> <start> <end> <point1_x>"
            " <point1_y> <point2_x> <point2_y> <filename>" << endl;
    cerr << "\t* to calculate orientation: ./lab1 orient <func> <n> <point1_x>"
            " <point1_y> <point2_x> <point2_y> <file_in> <file_out>" << endl;
    cerr << endl;
}

int main(int argc, char **argv) {
    exactinit();

    if (argc < 5) {
        usage();
        return 1;
    }

    if (strcmp(argv[1], "generate1") == 0) {
        int n = atoi(argv[2]);
        REAL start = (REAL) atof(argv[3]);
        REAL end = (REAL) atof(argv[4]);
        char *filename = argv[5];

        ofstream filestream(filename);

        vector<pair<REAL, REAL>> points = generatePointsInSquare(n, start, end);

        for (auto point : points) {
            filestream << point.first << " " << point.second << endl;
        }

        filestream.close();
    }

    else if (strcmp(argv[1], "generate2") == 0) {
        int n = atoi(argv[2]);
        REAL centerX = (REAL) atof(argv[3]);
        REAL centerY = (REAL) atof(argv[4]);
        REAL radius = (REAL) atof(argv[5]);
        pair<REAL, REAL> center = make_pair(centerX, centerY);

        char *filename = argv[6];

        ofstream filestream(filename);

        vector<pair<REAL, REAL>> points = generatePointsOnCircle(n, radius, center);

        for (auto point : points) {
            filestream << point.first << " " << point.second << endl;
        }

        filestream.close();
    }

    else if (strcmp(argv[1], "generate3") == 0) {
        int n = atoi(argv[2]);
        REAL start = (REAL) atof(argv[3]);
        REAL end = (REAL) atof(argv[4]);
        REAL point1X = (REAL) atof(argv[5]);
        REAL point1Y = (REAL) atof(argv[6]);
        REAL point2X = (REAL) atof(argv[7]);
        REAL point2Y = (REAL) atof(argv[8]);
        pair<REAL, REAL> point1 = make_pair(point1X, point1Y);
        pair<REAL, REAL> point2 = make_pair(point2X, point2Y);

        char *filename = argv[9];

        ofstream filestream(filename);

        vector<pair<REAL, REAL>> points = generatePointsOnLine(n, start, end, point1, point2);

        for (auto point : points) {
            filestream << point.first << " " << point.second << endl;
        }

        filestream.close();
    }

    else if (strcmp(argv[1], "orient") == 0) {
        OrientationFunction function = 0;
        if (strcmp(argv[2], "myorient2d") == 0) {
            function = myOrient2d;
        } else if (strcmp(argv[2], "orient2dfast") == 0) {
            function = orient2dFastWrapper;
        } else if (strcmp(argv[2], "orient2dslow") == 0) {
            function = orient2dSlowWrapper;
        } else if (strcmp(argv[2], "orient2dexact") == 0) {
            function = orient2dExactWrapper;
        } else {
            return 3;
        }

        int n = atoi(argv[3]);
        REAL point1X = (REAL) atof(argv[4]);
        REAL point1Y = (REAL) atof(argv[5]);
        REAL point2X = (REAL) atof(argv[6]);
        REAL point2Y = (REAL) atof(argv[7]);

        POINT point1 = make_pair(point1X, point1Y);
        POINT point2 = make_pair(point2X, point2Y);

        char *filenameIn = argv[8];
        char *filenameOut = argv[9];

        ifstream fileIn(filenameIn);
        ofstream fileOut(filenameOut);

        REAL x, y;

        for (int i = 0; i < n; ++i) {
            fileIn >> x >> y;
            fileOut << x << " " << y << " " << function(point1, point2, make_pair(x, y)) << endl;
        }

        fileIn.close();
        fileOut.close();
    }

    else {
        usage();
        return 2;
    }

    return 0;
}
