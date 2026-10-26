
import itertools
import math
import random
import time
import matplotlib.pyplot as plt


def mst_prim(points: list[tuple[float, float]]) -> dict[int, list[int]]:
    best = {
        v: (math.dist(points[0], points[v]), 0)
        for v in range(1, len(points))
    }
    children = {v: [] for v in range(len(points))}

    while best:
        v = min(best, key=lambda u: best[u][0])
        children[best.pop(v)[1]].append(v)

        for u in best:
            d = math.dist(points[v], points[u])
            if d < best[u][0]:
                best[u] = (d, v)

    return children


def preorder(children: dict[int, list[int]], root: int = 0) -> list[int]:
    return [
        root
    ] + [
        c
        for child in children[root]
        for c in preorder(children, child)
    ]


def tour_length(points, tour) -> float:
    return sum(
        math.dist(
            points[tour[i]],
            points[tour[(i + 1) % len(tour)]]
        )
        for i in range(len(tour))
    )


def two_opt_move(route: list[int], i: int, k: int) -> list[int]:
    return route[:i] + route[i:k + 1][::-1] + route[k + 1:]


def two_opt(points, route):
    route = route.copy()
    improvements = 0
    n = len(route)

    while True:
        best_route = route
        best_cost = tour_length(points, route)

        for i in range(1, n - 1):
            for k in range(i + 1, n):
                candidate = two_opt_move(route, i, k)
                candidate_cost = tour_length(points, candidate)

                if candidate_cost < best_cost - 1e-10:
                    best_route = candidate
                    best_cost = candidate_cost

        if best_route == route:
            break

        route = best_route
        improvements += 1

    return route, tour_length(points, route), improvements


def optimal_tour(points):
    n = len(points)
    distances = [
        [
            math.dist(points[i], points[j])
            for j in range(n)
        ]
        for i in range(n)
    ]

    best_cost = float("inf")

    for permutation in itertools.permutations(range(1, n)):
        route = (0,) + permutation
        cost = sum(
            distances[route[i]][route[(i + 1) % n]]
            for i in range(n)
        )

        if cost < best_cost:
            best_cost = cost

    return best_cost


def simulated_annealing(points, initial_route, iterations=1000,
                        initial_temperature=10.0, alpha=0.995, seed=0):
    rng = random.Random(seed)
    current = initial_route.copy()
    current_cost = tour_length(points, current)

    best = current.copy()
    best_cost = current_cost
    n = len(current)

    for iteration in range(iterations):
        temperature = initial_temperature * (alpha ** iteration)

        i, k = sorted(rng.sample(range(n), 2))

        if i == 0 and k == n - 1:
            continue

        candidate = two_opt_move(current, i, k)
        candidate_cost = tour_length(points, candidate)
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

    return best, best_cost


def run_experiment(instances=100, n_cities=9):
    results = {
        "MST puro": [],
        "MST + 2-opt": [],
        "Busqueda Local": [],
        "Recocido Simulado": []
    }

    ratios = []
    execution_times = {
        "MST puro": [],
        "MST + 2-opt": [],
        "Busqueda Local": [],
        "Recocido Simulado": []
    }

    for trial in range(instances):
        rng = random.Random(7 + trial)

        points = [
            (rng.uniform(0, 10), rng.uniform(0, 10))
            for _ in range(n_cities)
        ]

        optimal_cost = optimal_tour(points)

        start = time.perf_counter()
        tree = mst_prim(points)
        mst_route = preorder(tree)
        mst_cost = tour_length(points, mst_route)
        execution_times["MST puro"].append(
            time.perf_counter() - start
        )

        start = time.perf_counter()
        _, mst_2opt_cost, _ = two_opt(points, mst_route)
        execution_times["MST + 2-opt"].append(
            time.perf_counter() - start
        )

        rng_route = random.Random(1000 + trial)
        initial_route = rng_route.sample(
            list(range(n_cities)), n_cities
        )

        start = time.perf_counter()
        _, local_cost, _ = two_opt(points, initial_route)
        execution_times["Busqueda Local"].append(
            time.perf_counter() - start
        )

        start = time.perf_counter()
        _, sa_cost = simulated_annealing(
            points,
            initial_route,
            iterations=1000,
            initial_temperature=10.0,
            alpha=0.995,
            seed=2000 + trial
        )
        execution_times["Recocido Simulado"].append(
            time.perf_counter() - start
        )

        results["MST puro"].append(mst_cost)
        results["MST + 2-opt"].append(mst_2opt_cost)
        results["Busqueda Local"].append(local_cost)
        results["Recocido Simulado"].append(sa_cost)

        ratios.append(mst_cost / optimal_cost)

    return results, ratios, execution_times


def show_results(results, ratios, execution_times):
    print("RESULTADOS DEL EXPERIMENTO")
    print("=" * 55)
    print("Instancias: 100")
    print("Ciudades por instancia: 9")

    print(f"\nRazon promedio MST / optimo: {sum(ratios) / len(ratios):.4f}")
    print(f"Razon minima: {min(ratios):.4f}")
    print(f"Razon maxima: {max(ratios):.4f}")
    print(f"Instancias con razon superior a 2: "
          f"{sum(r > 2 + 1e-9 for r in ratios)}")

    print("\nCOMPARACION DE COSTOS Y TIEMPOS")
    print("-" * 55)

    for method, costs in results.items():
        average_cost = sum(costs) / len(costs)
        average_time = (
            sum(execution_times[method]) / len(execution_times[method])
        )

        print(f"\n{method}")
        print(f"Costo promedio: {average_cost:.4f}")
        print(f"Mejor costo: {min(costs):.4f}")
        print(f"Tiempo promedio: {average_time:.6f} segundos")


def plot_results(results, ratios):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].hist(
        ratios,
        bins=12,
        color="steelblue",
        edgecolor="black",
        alpha=0.8
    )
    axes[0].axvline(
        2,
        color="red",
        linestyle="--",
        linewidth=2,
        label="Limite teorico = 2"
    )
    axes[0].axvline(
        sum(ratios) / len(ratios),
        color="green",
        linestyle="-.",
        linewidth=2,
        label="Razon promedio"
    )
    axes[0].set_title("Razon de aproximacion MST")
    axes[0].set_xlabel("Costo MST / costo optimo")
    axes[0].set_ylabel("Numero de instancias")
    axes[0].legend()
    axes[0].grid(axis="y", alpha=0.3)

    methods = list(results.keys())
    costs = [results[method] for method in methods]

    axes[1].boxplot(costs, tick_labels=methods)
    axes[1].set_title("Comparacion de costos finales")
    axes[1].set_ylabel("Costo de la ruta")
    axes[1].tick_params(axis="x", rotation=15)
    axes[1].grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig("comparacion_mst_tsp.png", dpi=300)
    print("\nGrafica guardada como comparacion_mst_tsp.png")
    plt.show()


if __name__ == "__main__":
    results, ratios, execution_times = run_experiment(
        instances=100,
        n_cities=9
    )

    show_results(results, ratios, execution_times)
    plot_results(results, ratios)
