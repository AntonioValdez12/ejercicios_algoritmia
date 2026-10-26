
import multiprocessing as mp
import random
import time
import matplotlib.pyplot as plt


def estimate_pi(seed: int, samples: int = 1_000_000) -> float:
    """Monte Carlo: fraction of random points that fall inside the unit quarter circle."""
    rng = random.Random(seed)
    inside = sum(
        rng.random()**2 + rng.random()**2 <= 1.0
        for _ in range(samples)
    )
    return 4 * inside / samples


def ejecutar_secuencial(seeds):
    """Ejecuta estimate_pi secuencialmente y mide el tiempo."""
    t0 = time.perf_counter()
    resultados = [estimate_pi(s) for s in seeds]
    tiempo = time.perf_counter() - t0

    return resultados, tiempo


def ejecutar_paralelo(seeds, procesos):
    """Ejecuta estimate_pi usando el número indicado de procesos."""
    t0 = time.perf_counter()

    with mp.Pool(processes=procesos) as pool:
        resultados = pool.map(estimate_pi, seeds)

    tiempo = time.perf_counter() - t0

    return resultados, tiempo


def calcular_speedup(tiempo_secuencial, tiempo_paralelo):
    """Calcula la aceleración respecto a la ejecución secuencial."""
    return tiempo_secuencial / tiempo_paralelo


def graficar_speedup(procesos, speedups):
    """Grafica el speedup real y el speedup ideal."""
    plt.figure(figsize=(8, 5))

    # Aceleración obtenida experimentalmente
    plt.plot(
        procesos,
        speedups,
        marker="o",
        linewidth=2,
        label="Speedup real"
    )

    # Aceleración ideal: S(p) = p
    plt.plot(
        procesos,
        procesos,
        linestyle="--",
        marker="x",
        label="Speedup ideal"
    )

    plt.xlabel("Número de procesos")
    plt.ylabel("Aceleración (speedup)")
    plt.title("Aceleración paralela de estimate_pi")
    plt.xticks(procesos)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig("speedup.png", dpi=300)
    print("\nGráfica guardada como speedup.png")

    plt.show()


if __name__ == "__main__":
    # 8 ejecuciones independientes, una por cada semilla.
    seeds = list(range(8))

    # 1. Ejecución secuencial: referencia para calcular el speedup.
    seq_results, t_seq = ejecutar_secuencial(seeds)

    print(f"Sequential wall-clock: {t_seq:.3f} s")
    print(
        f"pi estimate (mean of {len(seeds)} runs): "
        f"{sum(seq_results) / len(seq_results):.5f}"
    )

    # 2. Ejecuciones paralelas con 1, 2, 4 y 8 procesos.
    numero_procesos = [1, 2, 4, 8]

    tiempos = []
    speedups = []

    for p in numero_procesos:
        resultados, t_par = ejecutar_paralelo(seeds, p)
        speedup = calcular_speedup(t_seq, t_par)

        tiempos.append(t_par)
        speedups.append(speedup)

        print(
            f"Processes: {p:2d} | "
            f"Parallel wall-clock: {t_par:.3f} s | "
            f"Speedup: {speedup:.2f}x | "
            f"Pi estimate: {sum(resultados) / len(resultados):.5f}"
        )




    graficar_speedup(numero_procesos, speedups)
