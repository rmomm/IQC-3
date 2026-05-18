import os
import matplotlib.pyplot as plt

from qiskit.visualization import plot_histogram


RESULTS_DIR = "results"

if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)


def save_histogram(counts, filename):

    fig = plot_histogram(counts, figsize=(10, 6))

    path = os.path.join(RESULTS_DIR, filename)

    fig.savefig(path)

    plt.close(fig)


def save_circuit(qc, filename):

    fig = qc.draw(output='mpl', fold=50)

    path = os.path.join(RESULTS_DIR, filename)

    fig.savefig(path)

    plt.close(fig)



def create_plots(qubits, states, times, probabilities, depths):
    plt.figure(figsize=(8, 5))

    plt.plot(states, times, marker='o')

    plt.xlabel("Number of states")
    plt.ylabel("Execution time (sec)")
    plt.title("Grover Algorithm Execution Time")

    plt.grid(True)

    plt.savefig(os.path.join(
        RESULTS_DIR,
        "execution_time.png"
    ))

    plt.close()


    plt.figure(figsize=(8, 5))

    plt.plot(states, probabilities, marker='o')

    plt.xlabel("Number of states")
    plt.ylabel("Success probability")
    plt.title("Grover Algorithm Success Probability")

    plt.grid(True)

    plt.savefig(os.path.join(
        RESULTS_DIR,
        "probability.png"
    ))

    plt.close()


    plt.figure(figsize=(8, 5))

    plt.plot(qubits, depths, marker='o')

    plt.xlabel("Number of qubits")
    plt.ylabel("Circuit depth")
    plt.title("Quantum Circuit Depth")

    plt.grid(True)

    plt.savefig(os.path.join(
        RESULTS_DIR,
        "circuit_depth.png"
    ))

    plt.close()

    print("\nPlots saved to results/")
