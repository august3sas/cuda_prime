#include <iostream>
#include <cmath>
#include <omp.h>
#include <vector>
#include <random>
#include <chrono>
#include <numeric>
#include <fstream>

bool isPrime(unsigned long long int number) {
    if (number <= 1) return false;
    if (number == 2) return true;
    if (number % 2 == 0) return false;

    unsigned long long int limit = sqrt(number);
    for (unsigned long long int i = 3; i <= limit; i += 2) {
        if (number % i == 0) {
            return false;
        }
    }

    return true;
}

int main() {
    omp_set_num_threads(omp_get_max_threads());
    std::vector<int> ends = {1, 3, 7, 9};
    std::random_device rd;
    std::mt19937 gen(rd());
    std::ofstream file("omp_times.csv"); // Open a file for output
    file << "Order of Magnitude,Average Time\n"; // Write the header

    for (int order = 3; order <= 18; order++) {
        unsigned long long int lower = 1;
        for (int i = 0; i < order; i++) {
            lower *= 10;
        }
        unsigned long long int upper = lower * 10 - 1;

        std::uniform_int_distribution<unsigned long long int> distrib(lower, upper);
        std::vector<unsigned long long int> numbers;
        std::vector<double> times;

        for (int i = 0; i < 100; i++) {
            unsigned long long int number;
            do {
                number = distrib(gen);
            } while (number%10 == 5 || number%10 == 0 || number%10 == 2 || number%10 == 4 || number%10 == 6 || number%10 == 8);
            numbers.push_back(number);
        }

        #pragma omp parallel for
        for (int i = 0; i < 100; i++) {
            auto start = std::chrono::high_resolution_clock::now();
            isPrime(numbers[i]);
            auto end = std::chrono::high_resolution_clock::now();
            std::chrono::duration<double, std::milli> elapsed = end - start;

            #pragma omp critical
            times.push_back(elapsed.count());
        }

        double average_time = std::accumulate(times.begin(), times.end(), 0.0) / times.size();
        std::cout << "Order of magnitude: " << order << ", Average time: " << average_time << " ms\n";
        file << order << "," << average_time << "\n"; // Write the data to the file

    }
    file.close();
    return 0;
}