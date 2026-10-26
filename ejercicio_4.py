
import math
import random
import time
import matplotlib.pyplot as plt

cities = {
    "A": (0, 0),
    "B": (0, 3),
    "E": (2, 5),
    "D": (4, 3),
    "C": (4, 0)
}


def tour_length(route: list[str]) -> float:
    return sum(
        math.dist(cities[route[i]], cities[route[(i + 1) % len(route)]])
        for i in range(len(route))
    )


def two_opt_move(route: list[str], i: int, k: int) -> list[str]:
    return route[:i] + route[i:k + 1][::-1] + route[k + 1:]


def simulated_annealing(initial_route, schedule, iterations=1000,
                        initial_temperature=10.0, alpha=0.995, seed=0):
    rng = random.Random(seed)

    current = initial_route.copy()
    current_cost = tour_length(current)

    best = current.copy()
    best_cost = current_cost
    convergence = []

    start_time = time.perf_counter()

    n = len(current)

    for iteration in range(iterations):
        if schedule == "linear":
            temperature = initial_temperature * (
                1 - iteration / iterations
            )
        elif schedule == "exponential":
            temperature = initial_temperature * (alpha ** iteration)
        else:
            raise ValueError("Esquema de enfriamiento no valido")

        i, k = sorted(rng.sample(range(n), 2))

        if i == 0 and k == n - 1:
            k -= 1

        candidate = two_opt_move(current, i, k)
        candidate_cost = tour_length(candidate)
        delta = candidate_cost - current_cost

        if delta < 0 or (
            temperature > 0
            and rng.random() < math.exp(-delta / temperature)
        ):
            current = candidate
            current_cost = candidate_cost

        if current_cost < best_cost:
            best = current.copy()
            best_cost = current_cost

        convergence.append(best_cost)

    elapsed = time.perf_counter() - start_time

    return best, best_cost, convergence, elapsed


def run_experiment(trials=30, iterations=1000):
    results = {
        "linear": {"costs": [], "times": [], "curves": [], "routes": []},
        "exponential": {"costs": [], "times": [], "curves": [], "routes": []}
    }

    for trial in range(trials):
        initial_route = random.Random(trial).sample(
            list(cities.keys()), len(cities)
        )

        for schedule in ["linear", "exponential"]:
            best, cost, curve, elapsed = simulated_annealing(
                initial_route=initial_route,
                schedule=schedule,
                iterations=iterations,
                initial_temperature=10.0,
                alpha=0.995,
                seed=trial + 100
            )

            results[schedule]["costs"].append(cost)
            results[schedule]["times"].append(elapsed)
            results[schedule]["curves"].append(curve)
            results[schedule]["routes"].append(best)

    return results


def show_results(results):
    names = {
        "linear": "Enfriamiento lineal",
        "exponential": "Enfriamiento exponencial"
    }

    print("RESULTADOS DE RECOCIDO SIMULADO")
    print("=" * 55)

    for schedule, result in results.items():
        average_cost = sum(result["costs"]) / len(result["costs"])
        average_time = sum(result["times"]) / len(result["times"])

        print(f"\n{names[schedule]}")
        print(f"Costo promedio final: {average_cost:.4f}")
        print(f"Mejor costo encontrado: {min(result['costs']):.4f}")
        print(f"Tiempo promedio: {average_time:.6f} segundos")
        print(f"Ruta de ejemplo: {result['routes'][0]}")


def plot_results(results, iterations):
    names = {
        "linear": "Enfriamiento lineal",
        "exponential": "Enfriamiento exponencial"
    }

    colors = {
        "linear": "steelblue",
        "exponential": "darkorange"
    }

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    for schedule, result in results.items():
        average_curve = [
            sum(curve[i] for curve in result["curves"])
            / len(result["curves"])
            for i in range(iterations)
        ]

        axes[0].plot(
            range(iterations),
            average_curve,
            label=names[schedule],
            color=colors[schedule]
        )

    axes[0].set_title("Convergencia del costo")
    axes[0].set_xlabel("Iteraciones")
    axes[0].set_ylabel("Mejor costo encontrado")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    for schedule, result in results.items():
        average_time = sum(result["times"]) / len(result["times"])
        average_cost = sum(result["costs"]) / len(result["costs"])

        axes[1].scatter(
            average_time,
            average_cost,
            s=100,
            color=colors[schedule],
            label=names[schedule]
        )

        axes[1].annotate(
            names[schedule],
            (average_time, average_cost),
            xytext=(5, 5),
            textcoords="offset points"
        )

    axes[1].set_title("Tiempo de ejecución vs. calidad")
    axes[1].set_xlabel("Tiempo promedio (segundos)")
    axes[1].set_ylabel("Costo promedio final")
    axes[1].grid(alpha=0.3)
    axes[1].legend()

    plt.tight_layout()
    plt.savefig("comparacion_simulated_annealing.png", dpi=300)
    print("\nGrafica guardada como comparacion_simulated_annealing.png")
    plt.show()


if __name__ == "__main__":
    trials = 30
    iterations = 1000

    results = run_experiment(trials, iterations)

    print(f"Ejecuciones por esquema: {trials}")
    print(f"Iteraciones por ejecucion: {iterations}")

    show_results(results)
    plot_results(results, iterations)
