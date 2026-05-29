"""
Завдання 4. Візуалізація бінарної купи.

Беремо за базу код з умови завдання (Node + add_edges + draw_tree) і будуємо
з масиву-купи структуру вузлів. Бінарна купа зберігається як масив:
для вузла з індексом i його нащадки знаходяться в 2i+1 та 2i+2.

Підтримуються min-heap і max-heap — для наочності перевіряється коректність
купи перед візуалізацією.
"""

from __future__ import annotations
import heapq
import uuid
from typing import List, Optional

import networkx as nx
import matplotlib.pyplot as plt


# ---------- структура вузла з умови завдання ----------

class Node:
    def __init__(self, key, color="skyblue"):
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(graph, node, pos, x=0.0, y=0.0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


# ---------- перетворення масиву-купи у дерево вузлів ----------

def heap_array_to_tree(heap: List, node_color: str = "skyblue") -> Optional[Node]:
    """
    Перетворює масив, що представляє бінарну купу, у дерево з вузлів Node.
    Зв'язки встановлюються за стандартною формулою: children(i) = 2i+1, 2i+2.
    """
    if not heap:
        return None

    nodes = [Node(value, color=node_color) for value in heap]
    n = len(nodes)
    for i in range(n):
        left_idx, right_idx = 2 * i + 1, 2 * i + 2
        if left_idx < n:
            nodes[i].left = nodes[left_idx]
        if right_idx < n:
            nodes[i].right = nodes[right_idx]
    return nodes[0]


def is_valid_heap(heap: List, kind: str = "min") -> bool:
    """Перевіряє, чи задовольняє масив властивості купи (min або max)."""
    if kind not in {"min", "max"}:
        raise ValueError("kind має бути 'min' або 'max'")
    n = len(heap)
    for i in range(n):
        left, right = 2 * i + 1, 2 * i + 2
        if kind == "min":
            if left < n and heap[i] > heap[left]:
                return False
            if right < n and heap[i] > heap[right]:
                return False
        else:
            if left < n and heap[i] < heap[left]:
                return False
            if right < n and heap[i] < heap[right]:
                return False
    return True


def draw_heap(heap: List, title: str = "Бінарна купа", kind: str = "min",
              save_path: Optional[str] = None) -> None:
    """Візуалізує бінарну купу у вигляді дерева. Колір залежить від типу купи."""
    if not heap:
        print("Купа порожня — нічого малювати.")
        return

    if not is_valid_heap(heap, kind):
        print(f"Увага: масив не є валідною {kind}-heap. Малюю як є.")

    color = "#90ee90" if kind == "min" else "#ffb6c1"  # світло-зелений / світло-рожевий
    root = heap_array_to_tree(heap, node_color=color)

    tree = nx.DiGraph()
    pos = {root.id: (0.0, 0.0)}
    tree = add_edges(tree, root, pos)

    colors = [data["color"] for _, data in tree.nodes(data=True)]
    labels = {node_id: data["label"] for node_id, data in tree.nodes(data=True)}

    plt.figure(figsize=(10, 6))
    nx.draw(tree, pos=pos, labels=labels, arrows=False,
            node_size=2200, node_color=colors, font_weight="bold")
    plt.title(f"{title}  ({kind}-heap, n={len(heap)})", fontsize=12)
    if save_path:
        plt.savefig(save_path, dpi=100, bbox_inches="tight")
        plt.close()
    else:
        plt.show()


# ---------- демонстрація ----------

if __name__ == "__main__":
    # 1) Min-heap, побудована через heapq з довільного списку
    values = [10, 4, 7, 1, 8, 3, 9, 2, 5, 6]
    min_heap = values.copy()
    heapq.heapify(min_heap)
    print("Початковий список:", values)
    print("Min-heap (масив):", min_heap)
    draw_heap(min_heap, title="Min-heap після heapify", kind="min")

    # 2) Max-heap — heapq не вміє напряму, інвертуємо знак
    max_heap = [-x for x in values]
    heapq.heapify(max_heap)
    max_heap = [-x for x in max_heap]
    print("Max-heap (масив):", max_heap)
    draw_heap(max_heap, title="Max-heap", kind="max")
