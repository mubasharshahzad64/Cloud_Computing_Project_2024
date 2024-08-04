#include <mpi.h>
#include <stdio.h>

#define SIZE 1000  // Size of the data to broadcast

int main(int argc, char** argv) {
    int rank, size;
    int data[SIZE];
    MPI_Status status;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (rank == 0) {
        // Initialize the data
        for (int i = 0; i < SIZE; i++) {
            data[i] = i;
        }
    }

    // Broadcast the data
    MPI_Bcast(data, SIZE, MPI_INT, 0, MPI_COMM_WORLD);

    

    MPI_Finalize();
    return 0;
}
