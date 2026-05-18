import math
import time
import csv
import os

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

from vis import (
    save_histogram,
    save_circuit,
    create_plots
)

RESULTS_DIR = "results"

if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

def oracle(qc, target_state):

    n = len(target_state)

    target_state = target_state[::-1]

    for qubit in range(n):

        if target_state[qubit] == '0':
            qc.x(qubit)

    qc.h(n - 1)

    qc.mcx(
        list(range(n - 1)),
        n - 1
    )

    qc.h(n - 1)

    for qubit in range(n):

        if target_state[qubit] == '0':
            qc.x(qubit)



def multi_oracle(qc, target_states):

    for target in target_states:
        oracle(qc, target)



def diffusion(qc, n):
    for qubit in range(n):
        qc.h(qubit)


    for qubit in range(n):
        qc.x(qubit)

    qc.h(n - 1)

    qc.mcx(
        list(range(n - 1)),
        n - 1
    )

    qc.h(n - 1)

    for qubit in range(n):
        qc.x(qubit)

    for qubit in range(n):
        qc.h(qubit)


def grover_search(n, target_state, shots=1024):

    simulator = AerSimulator()

    qc = QuantumCircuit(n, n)

    qc.h(range(n))

    N = 2 ** n

    iterations = math.floor(
        (math.pi / 4) * math.sqrt(N)
    )

    for _ in range(iterations):

        oracle(qc, target_state)

        diffusion(qc, n)

    qc.measure(range(n), range(n))

    start_time = time.perf_counter()

    compiled_circuit = transpile(
        qc,
        simulator
    )

    result = simulator.run(
        compiled_circuit,
        shots=shots
    ).result()

    end_time = time.perf_counter()

    counts = result.get_counts()

    most_common_state = max(
        counts,
        key=counts.get
    )

    success_probability = (
        counts.get(target_state, 0) / shots
    )

    execution_time = end_time - start_time

    save_histogram(
        counts,
        "basic_histogram.png"
    )

    save_circuit(
        qc,
        "basic_circuit.png"
    )

    return {
        "counts": counts,
        "result": most_common_state,
        "probability": success_probability,
        "time": execution_time,
        "depth": qc.depth(),
        "iterations": iterations
    }

def grover_multi_search(
    n,
    target_states,
    shots=1024
):

    simulator = AerSimulator()

    qc = QuantumCircuit(n, n)

    qc.h(range(n))

    N = 2 ** n
    M = len(target_states)

    iterations = math.floor(
        (math.pi / 4) * math.sqrt(N / M)
    )

    for _ in range(iterations):

        multi_oracle(
            qc,
            target_states
        )

        diffusion(qc, n)

    qc.measure(range(n), range(n))

    start_time = time.perf_counter()

    compiled_circuit = transpile(
        qc,
        simulator
    )

    result = simulator.run(
        compiled_circuit,
        shots=shots
    ).result()

    end_time = time.perf_counter()

    counts = result.get_counts()

    most_common_state = max(
        counts,
        key=counts.get
    )

    total_success = 0

    for target in target_states:
        total_success += counts.get(target, 0)

    success_probability = total_success / shots

    execution_time = end_time - start_time

    save_histogram(
        counts,
        "multi_histogram.png"
    )

    save_circuit(
        qc,
        "multi_circuit.png"
    )

    return {
        "counts": counts,
        "result": most_common_state,
        "probability": success_probability,
        "time": execution_time,
        "depth": qc.depth(),
        "iterations": iterations
    }


def run_experiments():

    qubits_list = []
    states_list = []
    time_list = []
    probability_list = []
    depth_list = []

    print("\n=== RUNNING EXPERIMENTS ===\n")

    for n in range(2, 16):

        target = "1" * n

        result = grover_search(
            n,
            target
        )

        qubits_list.append(n)

        states_list.append(2 ** n)

        time_list.append(result["time"])

        probability_list.append(
            result["probability"]
        )

        depth_list.append(
            result["depth"]
        )

        print(
            f"Qubits: {n} | "
            f"States: {2**n} | "
            f"Time: {result['time']:.5f} sec | "
            f"Probability: {result['probability']:.4f} | "
            f"Depth: {result['depth']}"
        )

    csv_path = os.path.join(
        RESULTS_DIR,
        "results.csv"
    )

    with open(
        csv_path,
        mode='w',
        newline=''
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "qubits",
            "states",
            "execution_time",
            "probability",
            "circuit_depth"
        ])

        for i in range(len(qubits_list)):

            writer.writerow([
                qubits_list[i],
                states_list[i],
                time_list[i],
                probability_list[i],
                depth_list[i]
            ])

    print(
        f"\nCSV results saved to: {csv_path}"
    )

    return (
        qubits_list,
        states_list,
        time_list,
        probability_list,
        depth_list
    )


if __name__ == "__main__":

    print("\n================================================")
    print("BASIC GROVER SEARCH")
    print("================================================")

    basic_result = grover_search(
        n=3,
        target_state="101"
    )

    print("Target state: 101")

    print(
        f"Measured result: "
        f"{basic_result['result']}"
    )

    print(
        f"Success probability: "
        f"{basic_result['probability']:.4f}"
    )

    print(
        f"Execution time: "
        f"{basic_result['time']:.5f} sec"
    )

    print(
        f"Circuit depth: "
        f"{basic_result['depth']}"
    )

    print(
        f"Grover iterations: "
        f"{basic_result['iterations']}"
    )

    print("\nMeasurement counts:")

    print(basic_result["counts"])

    print("\n================================================")
    print("MULTI-TARGET GROVER SEARCH")
    print("================================================")

    multi_result = grover_multi_search(
        n=3,
        target_states=["101", "111"]
    )

    print(
        "Target states: "
        "['101', '111']"
    )

    print(
        f"Measured result: "
        f"{multi_result['result']}"
    )

    print(
        f"Success probability: "
        f"{multi_result['probability']:.4f}"
    )

    print(
        f"Execution time: "
        f"{multi_result['time']:.5f} sec"
    )

    print(
        f"Circuit depth: "
        f"{multi_result['depth']}"
    )

    print(
        f"Grover iterations: "
        f"{multi_result['iterations']}"
    )

    print("\nMeasurement counts:")

    print(multi_result["counts"])

    q, s, t, p, d = run_experiments()

    create_plots(
        q,
        s,
        t,
        p,
        d
    )

    print("\nAll results saved successfully.")