#include <iostream>
#include <chrono>
#include <cmath>
#include <string>
bool isPrime(unsigned long long int number) {
    if (number <= 1) return false;
    if (number == 2) return true;
    if (number % 2 == 0) return false;
    for (unsigned long long int i = 3; i <= sqrt(number); i += 2) {
        if (number % i == 0) {
            return false;
        }
    }
    return true;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        std::cout << "Usage: ./primes number\n";
        return 1;
    }

    unsigned long long int number = std::stoull(argv[1]);

    auto start = std::chrono::high_resolution_clock::now();
    bool result = isPrime(number);
    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double, std::milli> elapsed = end - start;

    if (result) {
        std::cout << number << " is prime\n";
    } else {
        std::cout << number << " is not prime\n";
    }

    std::cout << elapsed.count() << "\n";

    return 0;
}