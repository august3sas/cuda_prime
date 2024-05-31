import subprocess
import sys
import time
import csv
import random

numbers = []
orders_of_magnitude = []
for i in range(3, 18):
    min_val = 10 ** i
    max_val = 10 ** (i + 1)
    for _ in range(100):
        while True:
            num = random.randrange(min_val, max_val)
            if num % 2 != 0 and str(num)[-1] in ['1', '3', '7', '9']:
                numbers.append(num)
                orders_of_magnitude.append(i)
                break


with open('cuda_times.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Number", "Order of Magnitude", "Time"])

    for number, order in zip(numbers, orders_of_magnitude):
        result = subprocess.run(["./primes", str(number)], capture_output=True, text=True)
        output_lines = result.stdout.splitlines()
        time_taken = float(output_lines[-1])
        writer.writerow([number, order, time_taken])
        print(f"Time taken for number {number} (order {order}): {time_taken} milliseconds")

with open('seq_times.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Number", "Order of Magnitude", "Time"])

    for number, order in zip(numbers, orders_of_magnitude):
        result = subprocess.run(["./primes_seq", str(number)], capture_output=True, text=True)
        output_lines = result.stdout.splitlines()
        time_taken = float(output_lines[-1])
        writer.writerow([number, order, time_taken])
        print(f"Time taken for number {number} (order {order}): {time_taken} milliseconds")