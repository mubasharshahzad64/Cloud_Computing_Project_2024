import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data = pd.read_csv('latency_results.csv')

# Plot data
plt.figure(figsize=(12, 8))
sns.lineplot(data=data, x='size', y='latency', hue='node', marker='o')
plt.title('MPI Latency Test Results')
plt.xlabel('Message Size (bytes)')
plt.ylabel('Latency (us)')
plt.xscale('log')
plt.yscale('log')
plt.legend(title='Node')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.savefig('latency_plot.png')
# Save the plot to a file
plt.savefig('mpi_latency_plot.png')  # Save as a PNG file
