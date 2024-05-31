import pandas as pd
import matplotlib.pyplot as plt

# Load the data
cuda_times = pd.read_csv('cuda_times.csv')
seq_times = pd.read_csv('seq_times.csv')
omp_times = pd.read_csv('omp_times.csv')

# Group by order of magnitude and calculate min, mean, max
cuda_stats = cuda_times.groupby('Order of Magnitude')['Time'].agg(['min', 'mean', 'max'])
seq_stats = seq_times.groupby('Order of Magnitude')['Time'].agg(['min', 'mean', 'max'])

# Plotting
def plot_data(data, yscale, title):
    plt.figure(figsize=(10, 6))
    plt.plot(data['min'], label='Min Time')
    plt.plot(data['mean'], label='Average Time')
    plt.plot(data['max'], label='Max Time')
    plt.yscale(yscale)
    plt.xlabel('Order of Magnitude')
    plt.ylabel('Time in ms')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

# CUDA Times
plot_data(cuda_stats, 'linear', 'CUDA Times (Linear Scale)')
plot_data(cuda_stats, 'log', 'CUDA Times (Log Scale)')

# Sequential Times
plot_data(seq_stats, 'linear', 'Sequential Times (Linear Scale)')
plot_data(seq_stats, 'log', 'Sequential Times (Log Scale)')

# OMP Times
plt.figure(figsize=(10, 6))
plt.plot(omp_times['Order of Magnitude'], omp_times['Average Time'], label='Average Time')
plt.yscale('linear')
plt.xlabel('Order of Magnitude')
plt.ylabel('Time in ms')
plt.title('OMP Times (Linear Scale)')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(omp_times['Order of Magnitude'], omp_times['Average Time'], label='Average Time')
plt.yscale('log')
plt.xlabel('Order of Magnitude')
plt.ylabel('Time in ms')
plt.title('OMP Times (Log Scale)')
plt.legend()
plt.grid(True)
plt.show()

# Average Times Comparison
plt.figure(figsize=(10, 6))
plt.plot(cuda_stats['mean'], label='CUDA')
plt.plot(seq_stats['mean'], label='Sequential')
plt.plot(omp_times.set_index('Order of Magnitude')['Average Time'], label='OMP')
plt.yscale('linear')
plt.xlabel('Order of Magnitude')
plt.ylabel('Time in ms')
plt.title('Average Times Comparison (Linear Scale)')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(cuda_stats['mean'], label='CUDA')
plt.plot(seq_stats['mean'], label='Sequential')
plt.plot(omp_times.set_index('Order of Magnitude')['Average Time'], label='OMP')
plt.yscale('log')
plt.xlabel('Order of Magnitude')
plt.ylabel('Time in ms')
plt.title('Average Times Comparison (Log Scale)')
plt.legend()
plt.grid(True)
plt.show()

# Whisker Plots
def plot_whisker(data, yscale, title, filename):
    plt.figure(figsize=(10, 6))
    data.boxplot(column='Time', by='Order of Magnitude', grid=True)
    plt.yscale(yscale)
    plt.xlabel('Order of Magnitude')
    plt.ylabel('Time in ms')
    plt.title(title)
    plt.suptitle('')  # Suppress default title
    plt.show()

plot_whisker(cuda_times, 'linear', 'CUDA Times Whisker Plot (Linear Scale)', 'cuda_times_linear.png')
plot_whisker(cuda_times, 'log', 'CUDA Times Whisker Plot (Log Scale)', 'cuda_times_log.png')
plot_whisker(seq_times, 'linear', 'Sequential Times Whisker Plot (Linear Scale)', 'seq_times_linear.png')
plot_whisker(seq_times, 'log', 'Sequential Times Whisker Plot (Log Scale)', 'seq_times_log.png')
