
import matplotlib.pyplot as plt

items = [
    {"name": "A", "value": 2,  "weight": 2},
    {"name": "B", "value": 3,  "weight": 3},
    {"name": "C", "value": 16, "weight": 4},
    {"name": "D", "value": 5,  "weight": 5},
    {"name": "E", "value": 30, "weight": 6}
]

CAPACITY = 10


def mostrar_instancia(items, capacity):
    """Muestra los datos de la instancia experimental."""

    print("=" * 65)
    print("EJERCICIO 2: GREEDY KNAPSACK")
    print("=" * 65)

    print("\nDISENO DE LA INSTANCIA EXPERIMENTAL")
    print(
        f"Se propone una mochila con capacidad maxima de "
        f"{capacity} unidades y {len(items)} objetos."
    )
    print(
        "El objetivo es demostrar que elegir primero los objetos "
        "de menor peso puede producir un valor total inferior "
        "al criterio de valor/peso.\n"
    )

    print(f"{'Objeto':<12}{'Peso':<12}{'Valor':<12}{'Valor/Peso':<12}")

    for item in items:
        ratio = item["value"] / item["weight"]
        print(
            f"{item['name']:<12}"
            f"{item['weight']:<12}"
            f"{item['value']:<12}"
            f"{ratio:<12.2f}"
        )

    print(f"\nCapacidad de la mochila: {capacity}")


def greedy_knapsack(items, capacity, criterion):
    """Resuelve la mochila mediante una estrategia voraz."""

    if criterion == "weight":
        # Priorizar los objetos de menor peso
        ordered = sorted(
            items,
            key=lambda item: item["weight"]
        )

    elif criterion == "ratio":
        # Priorizar el mayor valor por unidad de peso
        ordered = sorted(
            items,
            key=lambda item: item["value"] / item["weight"],
            reverse=True
        )

    else:
        raise ValueError("Criterio no valido")

    selected = []
    used_capacity = 0
    total_value = 0

    for item in ordered:
        if used_capacity + item["weight"] <= capacity:
            selected.append(item)
            used_capacity += item["weight"]
            total_value += item["value"]

    return selected, used_capacity, total_value


def show_results(name, result):
    """Muestra los resultados de una estrategia."""

    selected, used, value = result

    print(f"\n{name}")
    print("-" * 45)

    objects = [item["name"] for item in selected]

    print(f"Objetos seleccionados: {objects}")
    print(f"Capacidad utilizada: {used}/{CAPACITY}")
    print(f"Valor total: {value}")


def compare_results(weight_result, ratio_result):
    """Compara los resultados mediante una tabla y graficas."""

    methods = ["Menor peso", "Valor/peso"]

    results = [weight_result, ratio_result]

    print("\nTABLA COMPARATIVA DE RESULTADOS")
    print("=" * 75)
    print(
        f"{'Metodo':<16}"
        f"{'Objetos':<22}"
        f"{'Peso usado':<16}"
        f"{'Valor total':<12}"
    )

    for name, result in zip(methods, results):
        selected, used, value = result
        objects = ", ".join(item["name"] for item in selected)

        print(
            f"{name:<16}"
            f"{objects:<22}"
            f"{used}/{CAPACITY:<14}"
            f"{value:<12}"
        )


    used_capacities = [result[1] for result in results]
    total_values = [result[2] for result in results]

    fig, axes = plt.subplots(1, 2, figsize=(11, 5))

    bars1 = axes[0].bar(
        methods,
        total_values,
        color=["orange", "steelblue"]
    )
    axes[0].set_title("Valor total obtenido")
    axes[0].set_ylabel("Valor")
    axes[0].bar_label(bars1)
    axes[0].grid(axis="y", alpha=0.3)

    bars2 = axes[1].bar(
        methods,
        used_capacities,
        color=["orange", "steelblue"]
    )
    axes[1].set_title("Capacidad utilizada")
    axes[1].set_ylabel("Peso")
    axes[1].set_ylim(0, CAPACITY + 2)
    axes[1].bar_label(bars2)
    axes[1].grid(axis="y", alpha=0.3)

    fig.suptitle("Comparacion de estrategias voraces")
    plt.tight_layout()

    plt.savefig("comparacion_knapsack.png", dpi=300)
    print("\nGrafica guardada como comparacion_knapsack.png")

    plt.show()


if __name__ == "__main__":

    
    mostrar_instancia(items, CAPACITY)

  
    result_weight = greedy_knapsack(
        items, CAPACITY, "weight"
    )

    result_ratio = greedy_knapsack(
        items, CAPACITY, "ratio"
    )

   
    show_results("Metodo: menor peso primero", result_weight)
    show_results("Metodo: mayor valor/peso primero", result_ratio)


    compare_results(result_weight, result_ratio)


    print("\nANALISIS DE LA INSTANCIA")
    print("-" * 45)

    difference = ratio_result_value = (
        result_ratio[2] - result_weight[2]
    )

    print(
        f"El metodo de valor/peso obtuvo "
        f"{difference} unidades mas de valor."
    )

    print(
        "Esto demuestra que elegir primero los objetos de menor "
        "peso no garantiza maximizar el valor total de la mochila."
    )