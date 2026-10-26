
import math
import random
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


def nearest_neighbor(start: str) -> list[str]:
    unvisited = set(cities.keys())
    unvisited.remove(start)
    route = [start]
    current = start

    while unvisited:
        next_city = min(
            unvisited,
            key=lambda city: math.dist(cities[current], cities[city])
        )
        route.append(next_city)
        unvisited.remove(next_city)
        current = next_city

    return route


def two_opt(route: list[str]):
    route = route.copy()
    improvements = 0

    while True:
        best_route = route
        best_length = tour_length(route)
        n = len(route)

        for i in range(1, n - 1):
            for k in range(i + 1, n):
                candidate = two_opt_move(route, i, k)
                candidate_length = tour_length(candidate)

                if candidate_length < best_length - 1e-10:
                    best_route = candidate
                    best_length = candidate_length

        if best_route == route:
            break

        route = best_route
        improvements += 1

    return route, improvements, tour_length(route)


def random_route():
    route = list(cities.keys())
    random.shuffle(route)
    return route


def run_experiment(trials=100):
    random_results = []
    nearest_results = []

    for _ in range(trials):
        initial_random = random_route()
        final_random, improvements_random, cost_random = two_opt(
            initial_random
        )

        random_results.append({
            "initial": initial_random,
            "final": final_random,
            "improvements": improvements_random,
            "cost": cost_random
        })

        start = random.choice(list(cities.keys()))
        initial_nearest = nearest_neighbor(start)
        final_nearest, improvements_nearest, cost_nearest = two_opt(
            initial_nearest
        )

        nearest_results.append({
            "initial": initial_nearest,
            "final": final_nearest,
            "improvements": improvements_nearest,
            "cost": cost_nearest
        })

    return random_results, nearest_results


def show_summary(name, results):
    improvements = [r["improvements"] for r in results]
    costs = [r["cost"] for r in results]

    print(f"\n{name}")
    print("-" * 45)
    print(f"Ejecuciones: {len(results)}")
    print(f"Promedio de mejoras: {sum(improvements) / len(improvements):.2f}")
    print(f"Mejor costo final: {min(costs):.2f}")
    print(f"Peor costo final: {max(costs):.2f}")
    print(f"Costo promedio: {sum(costs) / len(costs):.2f}")

    example = results[0]
    print(f"Ruta inicial de ejemplo: {example['initial']}")
    print(f"Ruta final de ejemplo: {example['final']}")
    print(f"Mejoras en el ejemplo: {example['improvements']}")
    print(f"Costo final del ejemplo: {example['cost']:.2f}")


def plot_results(random_results, nearest_results):
    labels = ["Ruta aleatoria", "Vecino mas cercano"]

    mean_improvements = [
        sum(r["improvements"] for r in random_results) / len(random_results),
        sum(r["improvements"] for r in nearest_results) / len(nearest_results)
    ]

    mean_costs = [
        sum(r["cost"] for r in random_results) / len(random_results),
        sum(r["cost"] for r in nearest_results) / len(nearest_results)
    ]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    bars1 = axes[0].bar(
        labels, mean_improvements, color=["orange", "steelblue"]
    )
    axes[0].set_title("Promedio de mejoras para converger")
    axes[0].set_ylabel("Numero de mejoras")
    axes[0].bar_label(bars1, fmt="%.2f")
    axes[0].grid(axis="y", alpha=0.3)

    bars2 = axes[1].bar(
        labels, mean_costs, color=["orange", "steelblue"]
    )
    axes[1].set_title("Costo promedio de la ruta final")
    axes[1].set_ylabel("Distancia total")
    axes[1].bar_label(bars2, fmt="%.2f")
    axes[1].grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig("comparacion_two_opt.png", dpi=300)
    print("\nGrafica guardada como comparacion_two_opt.png")
    plt.show()


if __name__ == "__main__":
    random.seed(7)

    route = ["A", "D", "E", "B", "C"]
    new_route = two_opt_move(route, 1, 3)

    print(f"Antes: {route} | L = {tour_length(route):.2f}")
    print(f"Despues: {new_route} | L = {tour_length(new_route):.2f}")

    trials = 100
    random_results, nearest_results = run_experiment(trials)

    print(f"\nEXPERIMENTO: {trials} EJECUCIONES POR ESCENARIO")

    show_summary("SOLUCION INICIAL ALEATORIA", random_results)
    show_summary("SOLUCION INICIAL CON VECINO MAS CERCANO", nearest_results)

    plot_results(random_results, nearest_results)
