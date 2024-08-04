# MPI Benchmark in Kubernetes

## Overview

This project demonstrates how to port and run MPI (Message Passing Interface) workflows within a Kubernetes environment. The goal is to deploy an OSU benchmark across nodes in a Kubernetes cluster, measure latency, and compare results from different configurations.

## Prerequisites

- A Linux machine with at least 8GB of RAM.
- Docker installed.
- Minikube or a multi-node Kubernetes cluster setup.
- Basic understanding of MPI, Docker, and Kubernetes.

## Steps

### 1. Set Up a Kubernetes Cluster

1. **Install Minikube**

    ```sh
    curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    chmod +x minikube
    sudo mv minikube /usr/local/bin/
    ```

2. **Start Minikube with Multi-Node Configuration**

    ```sh
    minikube start --nodes 2 --driver=virtualbox
    ```

3. **Install `kubectl`**

    ```sh
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    chmod +x kubectl
    sudo mv kubectl /usr/local/bin/
    ```

### 2. Install Networking Plugin

Choose and install a networking plugin for Kubernetes (Flannel or Calico).

- **Install Flannel**

    ```sh
    kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
    ```

- **Install Calico**

    ```sh
    kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
    ```

### 3. Install MPI Operator

1. **Clone the MPI Operator Repository**

    ```sh
    git clone https://github.com/kubeflow/mpi-operator.git
    cd mpi-operator
    ```

2. **Deploy the MPI Operator**

    ```sh
    kubectl apply -f deploy/crd.yaml
    kubectl apply -f deploy/rbac.yaml
    kubectl apply -f deploy/mpi-operator.yaml
    ```

3. **Verify the Deployment**

    ```sh
    kubectl get crds | grep mpijobs
    kubectl get deployments -n mpi-operator
    kubectl get pods -n mpi-operator
    ```

### 4. Create Docker Container with OSU Benchmark

1. **Create `Dockerfile`**

    Create a file named `Dockerfile` with the following content:

    ```Dockerfile
    FROM ubuntu:20.04

    RUN apt-get update && apt-get install -y \
        wget \
        build-essential \
        gcc \
        gfortran \
        make \
        mpich \
        && rm -rf /var/lib/apt/lists/*

    WORKDIR /osu_benchmarks

    RUN wget http://mvapich.cse.ohio-state.edu/download/mvapich/osu-micro-benchmarks-5.7.1.tgz && \
        tar -xzf osu-micro-benchmarks-5.7.1.tgz

    WORKDIR /osu_benchmarks/osu-micro-benchmarks-5.7.1

    RUN ./configure CC=mpicc CXX=mpicxx && make

    WORKDIR /osu_benchmarks/osu-micro-benchmarks-5.7.1/mpi/pt2pt

    CMD ["mpirun", "-np", "2", "./osu_latency"]
    ```

2. **Build and Push Docker Image**

    ```sh
    docker build -t your-dockerhub-username/osu-benchmarks .
    docker push your-dockerhub-username/osu-benchmarks
    ```

### 5. Create MPI Job in Kubernetes

1. **Create `mpi-job.yaml`**

    Save the following configuration as `mpi-job.yaml`:

    ```yaml
    apiVersion: kubeflow.org/v1beta1
    kind: MPIJob
    metadata:
      name: osu-benchmarks
    spec:
      mpiReplicaSpecs:
        Launcher:
          replicas: 1
          spec:
            containers:
            - name: mpi-launcher
              image: your-dockerhub-username/osu-benchmarks
              command: ["/bin/bash", "-c"]
              args: ["mpirun -np 2 ./osu_latency"]
        Worker:
          replicas: 2
          spec:
            containers:
            - name: mpi-worker
              image: your-dockerhub-username/osu-benchmarks
    ```

2. **Deploy MPI Job**

    ```sh
    kubectl apply -f mpi-job.yaml
    ```

### 6. Measure and Compare Latency

1. **Monitor the MPI Job**

    ```sh
    kubectl get mpijobs
    ```

2. **Get Logs to Check Latency**

    ```sh
    kubectl logs <mpi-launcher-pod-name>
    ```

3. **Modify Pod Placement for Comparison**

    Use node selectors or affinities to control pod placement. For example, to place workers on specific nodes:

    ```yaml
    affinity:
      nodeAffinity:
        requiredDuringSchedulingIgnoredDuringExecution:
          nodeSelectorTerms:
          - matchExpressions:
            - key: kubernetes.io/hostname
              operator: In
              values:
              - <node1-name>
    ```

### 7. Analyze Results

1. **Install Python and matplotlib**

    ```sh
    sudo apt update
    sudo apt install python3-pip
    pip3 install matplotlib
    ```

2. **Create `plot_latency.py`**

    Save the following Python script as `plot_latency.py`:

    ```python
    import matplotlib.pyplot as plt

    # Data - Replace with actual latency data
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
    plt.savefig('broadcast_latency_plot.png')
    print("Plot saved as 'broadcast_latency_plot.png'")
    ```

3. **Run the Python Script**

    ```sh
    python3 plot_latency.py
    ```



