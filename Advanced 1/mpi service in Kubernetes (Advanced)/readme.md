# Running OSU Benchmarks in Kubernetes

This directory contains solutions and configurations for running OSU benchmarks inside two containers distributed across different nodes in a Kubernetes cluster.

## Introduction

This aims to demonstrate proficiency in Kubernetes, Docker, and HPC workflows by porting simple HPC workflows into Kubernetes and testing their performance.

## Steps

- A Kubernetes cluster with at least two nodes.
- Calico installed for network communication between nodes.
- MPI operator installed in the cluster.

### 1. Set Up the Kubernetes Cluster

I have made Kubernetes cluster with at least two nodes. Install Calico for network communication between nodes.

### 2. Install MPI Operator

Install the MPI operator in Kubernetes cluster by applying the YAML manifest provided in the [mpi-operator documentation](https://github.com/kubeflow/mpi-operator).
### 3. kubectl apply -f https://raw.githubusercontent.com/kubeflow/mpi-operator/v0.3.0/deploy/v1alpha2/mpi-operator.yaml
Build the container image using the provided Dockerfile.
Push the image to a container registry accessible by your Kubernetes cluster.
### 4. Deploy MPI Job in Kubernetes
# MPIJob YAML
```
apiVersion: kubeflow.org/v1alpha2
kind: MPIJob
metadata:
  name: osu-benchmark
spec:
  slotsPerWorker: 1
  cleanPodPolicy: Running
  mpiReplicaSpecs:
    Launcher:
      replicas: 1
      template:
        spec:
          containers:
            - name: mpi-launcher
              image: <your-dockerhub-username>/osu-benchmark:latest
              command: ["mpirun"]
              args: ["-n", "2", "-hostfile", "/etc/mpi/hostfile", "./pt2pt/osu_latency"]
              resources:
                limits:
                  cpu: 1
                  memory: 1Gi
    Worker:
      replicas: 2
      template:
        spec:
          containers:
            - name: mpi-worker
              image: <your-dockerhub-username>/osu-benchmark:latest
              resources:
                limits:
                  cpu: 1
                  memory: 1Gi
```
### 5. Verify and Measure Latency

### 6. Compare Latency with Pods on the Same Node
### 7. Summary
By following these steps, I have done:

-Set up a Kubernetes cluster with minikube networking.
-Install the MPI operator.
-Create and deploy a container for the OSU benchmark.
-Measure and compare the latency between nodes and within the same node.
