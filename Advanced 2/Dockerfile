# Use an official Ubuntu as a parent image
FROM ubuntu:20.04

# Set environment variable to noninteractive to avoid tzdata configuration prompt
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    gcc \
    gfortran \
    make \
    mpich \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /osu_benchmarks

# Download and extract OSU Micro-Benchmarks
RUN wget http://mvapich.cse.ohio-state.edu/download/mvapich/osu-micro-benchmarks-5.7.1.tgz && \
    tar -xzf osu-micro-benchmarks-5.7.1.tgz

# Set the working directory
WORKDIR /osu_benchmarks/osu-micro-benchmarks-5.7.1

# Configure and compile the benchmarks
RUN ./configure CC=mpicc CXX=mpicxx && make

# Set the working directory to the pt2pt benchmarks
WORKDIR /osu_benchmarks/osu-micro-benchmarks-5.7.1/mpi/pt2pt

# Define the command to run when the container starts
CMD ["mpirun", "-np", "2", "./osu_latency"]

