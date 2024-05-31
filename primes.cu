#include <stdio.h>
#include <math.h>
#include <stdlib.h>

#define THREADS_PER_BLOCK 512

__global__ void isPrimeKernel(unsigned long long int number, bool *result) {
    __shared__ bool notPrime;
    if (threadIdx.x == 0) notPrime = false;
    __syncthreads();

    unsigned long long int index = threadIdx.x + blockIdx.x * blockDim.x;
    unsigned long long int stride = blockDim.x * gridDim.x;

    if (number % 2 == 0) {
        *result = false;
        return;
    }

    for (unsigned long long int i = max(index * 2 + 3, static_cast<unsigned long long int>(3)); i <= sqrtf((double)number); i += 2 * stride) {
        if (notPrime) return;
        if (number % i == 0) {
            notPrime = true;
            *result = false;
            return;
        }
    }
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: ./primes number\n");
        return 1;
    }

    unsigned long long int number = atoll(argv[1]);
    //unsigned long long int number = 7;
    bool result = true;
    bool *dev_result;

    cudaMalloc((void**)&dev_result, sizeof(bool));
    cudaMemcpy(dev_result, &result, sizeof(bool), cudaMemcpyHostToDevice);

    int blocks = 65535;

    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);

    cudaEventRecord(start, NULL);

    isPrimeKernel<<<blocks, THREADS_PER_BLOCK>>>(number, dev_result);

    cudaEventRecord(stop, NULL);
    cudaEventSynchronize(stop);
    float milliseconds = 0;
    cudaEventElapsedTime(&milliseconds, start, stop);

    cudaMemcpy(&result, dev_result, sizeof(bool), cudaMemcpyDeviceToHost);

    if (result) {
        printf("%llu is prime\n", number);
    } else {
        printf("%llu is not prime\n", number);
    }
    printf("%f\n", milliseconds);
    cudaFree(dev_result);

    return 0;
}