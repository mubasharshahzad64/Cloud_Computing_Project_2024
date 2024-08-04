# OSU MPI Benchmarks on Kubernetes

This repository contains the implementation of the OSU MPI Benchmarks on a Kubernetes cluster using the Kubeflow MPI Operator. The objective of this project was to measure the MPI latency and visualize the results.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [Setting Up the Environment](#setting-up-the-environment)
  - [Building and Pushing Docker Image](#building-and-pushing-docker-image)
  - [Deploying Resources on Kubernetes](#deploying-resources-on-kubernetes)
  - [Setting Up MPI Operator](#setting-up-mpi-operator)
- [Running the Benchmarks](#running-the-benchmarks)
- [Results](#results)
- [Conclusion](#conclusion)
- [Challenges Faced](#challenges-faced)
- [Key Takeaways](#key-takeaways)

## Introduction

This project documents the implementation of the OSU MPI Benchmarks on a Kubernetes cluster. The benchmarks are used to measure the latency of MPI communications. The process involves setting up a Kubernetes cluster, deploying the necessary resources, running the benchmarks, and interpreting the results.

## Prerequisites

- Docker
- Minikube
- kubectl
- Python with Matplotlib

## Setup Instructions

### Setting Up the Environment

1. **Install Minikube**

    ```sh
    curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    chmod +x minikube
    sudo mv minikube /usr/local/bin/
    minikube start --driver=docker
    ```

2. **Install kubectl**

    ```sh
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    chmod +x kubectl
    sudo mv kubectl /usr/local/bin/
    kubectl version --client
    ```

### Building and Pushing Docker Image

1. **Build Docker image**

    ```sh
    docker build -t <your-dockerhub-username>/osu-benchmarks .
    ```

2. **Push Docker image to Docker Hub**

    ```sh
    docker push <your-dockerhub-username>/osu-benchmarks
    ```

### Deploying Resources on Kubernetes

1. **Create necessary directories**

    ```sh
    mkdir -p ~/cloud-advance-project/k8s-manifests
    ```

2. **Save the deployment YAML files**

    - `osu-benchmarks-deployment.yaml`
    - `osu-benchmarks-mpijob.yaml`

3. **Apply the YAML files**

    ```sh
    kubectl apply -f ~/cloud-advance-project/k8s-manifests/osu-benchmarks-deployment.yaml
    kubectl apply -f ~/cloud-advance-project/k8s-manifests/osu-benchmarks-mpijob.yaml
    ```

### Setting Up MPI Operator

1. **Clone the MPI Operator repository**

    ```sh
    git clone https://github.com/kubeflow/mpi-operator.git
    cd mpi-operator
    ```

2. **Checkout a stable version**

    ```sh
    git checkout v0.3.0
    ```

3. **Apply the MPI Operator YAML**

    ```sh
    kubectl apply -f deploy/v2beta1/mpi-operator.yaml
    ```

## Running the Benchmarks

1. **Submit the MPI job**

    ```sh
    kubectl apply -f ~/cloud-advance-project/k8s-manifests/osu-benchmarks-mpijob.yaml
    ```

2. **Check the status of the MPI job**

    ```sh
    kubectl get mpijobs
    kubectl get pods
    ```

3. **View the logs**

    ```sh
    kubectl logs <launcher-pod-name>
    ```

## Results

After running the OSU MPI Benchmarks, the latency results were obtained and plotted using the following Python script:

```python
import matplotlib.pyplot as plt

# Data
sizes = [0, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304]
latencies = [4.77, 4.91, 4.90, 4.89, 4.90, 5.17, 4.91, 5.00, 4.97, 4.98, 3.76, 7.90, 0.76, 5.04, 8.69, 42.89, 6.28, 47.14, 144.97, 348.78, 500.44, 1550.27, 3195.43, 6453.01]

# Plot
plt.figure(figsize=(10, 6))
plt.plot(sizes, latencies, marker='o')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Message Size (Bytes)')
plt.ylabel('Latency (us)')
plt.title('OSU MPI Latency Test')
plt.grid(True, which="both", ls="--")
plt.show()
```
## Conclusion
```
In this project, we successfully deployed OSU MPI Benchmarks on a Kubernetes cluster using the Kubeflow MPI Operator. The benchmarks provided detailed latency measurements for different message sizes.
```
## Challenges Faced
```
Configuring the Kubernetes cluster and ensuring all dependencies were properly installed.
Dealing with resource allocation issues, such as insufficient CPU availability on the Minikube node.
Resolving issues related to CRD (Custom Resource Definitions) for MPI jobs.
```
## Key Takeaways
```
Kubernetes, combined with Kubeflow, provides a powerful platform for running MPI workloads.
Proper resource allocation and management are crucial for the successful execution of high-performance computing tasks.
Visualizing performance metrics helps in understanding the efficiency and bottlenecks of MPI implementations.
```
