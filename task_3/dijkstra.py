"""
Завдання 3. Алгоритм Дейкстри на бінарній купі.

Знаходить найкоротші відстані від початкової вершини до всіх інших
у зваженому графі з невід'ємними вагами. Складність: O((V + E) log V)
за рахунок використання купи (heapq).

Підхід «lazy deletion»: ми не видаляємо застарілі записи з купи, а просто
ігноруємо їх, коли витягуємо. Це стандартний прийом, що дозволяє обійтись
без структури «decrease-key».
"""

from __future__ import annotations
import heapq
from typing import Dict, Hashable, List, Tuple


Vertex = Hashable
Graph = Dict[Vertex, List[Tuple[Vertex, float]]]   # vertex -> [(neighbour, weight), ...]


def dijkstra(graph: Graph, start: Vertex) -> Tuple[Dict[Vertex, float], Dict[Vertex, Vertex]]:
    """
    Повертає (distances, previous):
      distances[v] — найкоротша відстань від start до v (math.inf, якщо недосяжна);
      previous[v]  — попередник v у дереві найкоротших шляхів (для відновлення шляху).
    """
    # Перевірка ваг — алгоритм Дейкстри не працює з від'ємними вагами
    for u, edges in graph.items():
        for v, w in edges:
            if w < 0:
                raise ValueError(
                    f"Від'ємна вага ребра {u}→{v}: {w}. "
                    "Дейкстра не підтримує від'ємні ваги, потрібен Беллман-Форд."
                )

    distances: Dict[Vertex, float] = {v: float("inf") for v in graph}
    distances[start] = 0.0
    previous: Dict[Vertex, Vertex] = {}

    # Купа з парами (відстань, вершина). heapq — це min-heap за першим елементом.
    heap: List[Tuple[float, Vertex]] = [(0.0, start)]

    while heap:
        current_dist, u = heapq.heappop(heap)

        # Lazy deletion: запис застарів — ми вже знайшли кращий шлях до u
        if current_dist > distances[u]:
            continue

        for neighbour, weight in graph.get(u, []):
            new_dist = current_dist + weight
            if new_dist < distances[neighbour]:
                distances[neighbour] = new_dist
                previous[neighbour] = u
                heapq.heappush(heap, (new_dist, neighbour))

    return distances, previous


def reconstruct_path(previous: Dict[Vertex, Vertex], start: Vertex, target: Vertex) -> List[Vertex]:
    """Відновлює послідовність вершин шляху start → target. Порожній список, якщо шляху немає."""
    if target != start and target not in previous:
        return []
    path: List[Vertex] = [target]
    while path[-1] != start:
        path.append(previous[path[-1]])
    path.reverse()
    return path


# ---------- демонстрація ----------

def build_example_graph() -> Graph:
    """Невеликий неорієнтований зважений граф для демонстрації."""
    edges = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("B", "C", 1),
        ("B", "D", 5),
        ("C", "D", 8),
        ("C", "E", 10),
        ("D", "E", 2),
        ("D", "F", 6),
        ("E", "F", 3),
    ]
    graph: Graph = {v: [] for v in "ABCDEF"}
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))  # неорієнтований — додаємо у обидва боки
    return graph


def visualize(graph: Graph, distances: Dict[Vertex, float], previous: Dict[Vertex, Vertex],
              start: Vertex, save_path: str | None = None) -> None:
    """Малює граф з підписаними вагами та виділеним деревом найкоротших шляхів від start."""
    import networkx as nx
    import matplotlib.pyplot as plt

    nx_graph = nx.Graph()
    for u, edges in graph.items():
        for v, w in edges:
            if not nx_graph.has_edge(u, v):
                nx_graph.add_edge(u, v, weight=w)

    # Ребра дерева найкоротших шляхів
    sp_edges = {tuple(sorted((v, p))) for v, p in previous.items()}

    pos = nx.spring_layout(nx_graph, seed=42)
    edge_colors = [
        "#d62728" if tuple(sorted(e)) in sp_edges else "#aaaaaa"
        for e in nx_graph.edges()
    ]
    edge_widths = [
        2.5 if tuple(sorted(e)) in sp_edges else 1.0
        for e in nx_graph.edges()
    ]
    node_colors = ["#ffcc00" if v == start else "#87ceeb" for v in nx_graph.nodes()]

    plt.figure(figsize=(10, 7))
    nx.draw(
        nx_graph, pos,
        with_labels=True,
        node_color=node_colors,
        node_size=1100,
        font_weight="bold",
        edge_color=edge_colors,
        width=edge_widths,
    )
    edge_labels = nx.get_edge_attributes(nx_graph, "weight")
    nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels=edge_labels, font_size=9)

    # Підпис відстаней біля вузлів
    dist_labels = {v: f"{v}\nd={distances[v]:.0f}" for v in nx_graph.nodes()}
    label_pos = {v: (x, y + 0.08) for v, (x, y) in pos.items()}
    nx.draw_networkx_labels(nx_graph, label_pos, labels=dist_labels, font_size=8,
                            font_color="#444444")

    plt.title(f"Найкоротші шляхи від «{start}» (червоним — дерево SPT)")
    plt.axis("off")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=100, bbox_inches="tight")
        plt.close()
    else:
        plt.show()


if __name__ == "__main__":
    g = build_example_graph()
    start = "A"
    distances, previous = dijkstra(g, start)

    print(f"Найкоротші відстані від «{start}»:")
    for v in sorted(distances):
        print(f"  {start} → {v}: {distances[v]:>3.0f}   шлях: {' → '.join(reconstruct_path(previous, start, v))}")

    visualize(g, distances, previous, start)
