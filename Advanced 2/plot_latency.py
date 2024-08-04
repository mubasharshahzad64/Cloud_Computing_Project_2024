import matplotlib.pyplot as plt

# Read the latency data from a file
with open('latency_data.txt', 'r') as file:
    lines = file.readlines()

# Extract sizes and latencies
sizes = []
latencies = []
for line in lines:
    parts = line.split()
    if len(parts) == 2:
        try:
            size = int(parts[0])
            latency = float(parts[1])
            sizes.append(size)
            latencies.append(latency)
        except ValueError:
            continue

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(sizes, latencies, marker='o')
plt.xlabel('Message Size (bytes)')
plt.ylabel('Latency (microseconds)')
plt.title('Broadcast Latency')
plt.xscale('log')
plt.yscale('log')
plt.grid(True, which="both", ls="--")
plt.savefig('broadcast_latency_plot.png')  # Save the plot to a file
plt.close()  # Close the plot to free up resources

