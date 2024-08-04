# MPI Benchmarking on Kubernetes

## Overview
This project demonstrates the deployment and execution of MPI benchmarks on a Kubernetes cluster. The benchmarks include point-to-point and broadcast latencies measured using the OSU Micro-Benchmarks suite. The setup utilizes Minikube for creating a local Kubernetes cluster and the MPI Operator to manage MPI jobs.

## Table of Contents
- [Overview](#overview)
- [Environment Setup](#environment-setup)
- [Implementation](#implementation)
  - [Deployment Configuration](#deployment-configuration)
  - [MPI Job Configuration](#mpi-job-configuration)
- [Results](#results)
  - [Point-to-Point Latency](#point-to-point-latency)
  - [Broadcast Latency](#broadcast-latency)
- [Challenges and Difficulties](#challenges-and-difficulties)
- [Conclusion](#conclusion)

## Environment Setup
To set up the environment, follow these steps:

1. **Start Minikube with appropriate resources:**
    ```bash
    minikube start --cpus=4 --memory=8192
    ```

2. **Clone the MPI Operator repository:**
    ```bash
    git clone https://github.com/kubeflow/mpi-operator.git
    cd mpi-operator
    ```

3. **Checkout a stable version of the MPI Operator:**
    ```bash
    git checkout v0.3.0
    ```

4. **Apply the MPI Operator YAML to create necessary resources:**
    ```bash
    kubectl apply -f deploy/v2beta1/mpi-operator.yaml
    ```

5. **Verify that MPI Operator pods are running:**
    ```bash
    kubectl get pods -n mpi-operator
    ```

## Implementation

### Deployment Configuration
The deployment configuration is specified in the `osu-benchmarks-deployment.yaml` file. This configuration sets up the necessary Kubernetes resources to run the MPI benchmarks.

### MPI Job Configuration
Two MPI job configurations are provided:
- `osu-benchmarks-mpijob.yaml`: For point-to-point latency measurement.
- `mpi-bcast-job-diff-nodes.yaml`: For broadcast latency measurement.

### Example YAML Files
- **osu-benchmarks-deployment.yaml**
    ```yaml
    # YAML content here
    ```

- **osu-benchmarks-mpijob.yaml**
    ```yaml
    # YAML content here
    ```

- **mpi-bcast-job-diff-nodes.yaml**
    ```yaml
    # YAML content here
    ```

## Results

### Point-to-Point Latency
The point-to-point latency was measured using the OSU MPI Latency Test. The results are as follows:
```plaintext
# OSU MPI Latency Test v5.7.1
# Size          Latency (us)
0               4.77
1               4.91
2               4.90
...
4194304      6453.01
