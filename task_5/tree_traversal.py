"""
Завдання 5. Візуалізація обходу бінарного дерева у глибину та в ширину.

Використано стек (DFS) і чергу (BFS) — БЕЗ рекурсії, як вимагає умова.
Кожен вузол при відвідуванні отримує унікальний колір у форматі #RRGGBB,
від темного до світлого відтінку, відповідно до порядку обходу.

Градієнт будується через HSV: тон фіксується (наприклад, синій для BFS і
оранжевий для DFS), а value (яскравість) лінійно зростає від темного до світлого.
"""

from __future__ import annotations
import colorsys
import uuid
from collections import deque
from typing import List, Optional

import matplotlib.pyplot as plt
import networkx as nx


# ---------- структура вузла (з умови завдання 4) ----------

class Node:
    def __init__(self, key, color: str = "#cccccc"):
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


# ---------- утиліти ----------

def gradient_color(index: int, total: int, hue: float) -> str:
    """
    Повертає колір у форматі #RRGGBB для відвідування з номером index із total.
    hue — тон у [0, 1] (наприклад, 0.6 — синій, 0.08 — оранжевий).
    Яскравість лінійно зростає: ранні відвідування темні, пізні — світлі.
    """
    if total <= 1:
        v = 0.5
    else:
        v = 0.25 + 0.65 * (index / (total - 1))  # від 0.25 (темний) до 0.90 (світлий)
    r, g, b = colorsys.hsv_to_rgb(hue, 0.85, v)
    return "#{:02X}{:02X}{:02X}".format(int(r * 255), int(g * 255), int(b * 255))


def count_nodes(root: Node) -> int:
    """Підраховує кількість вузлів у дереві (ітеративно, через стек)."""
    if root is None:
        return 0
    count, stack = 0, [root]
    while stack:
        node = stack.pop()
        count += 1
        if node.right: stack.append(node.right)
        if node.left:  stack.append(node.left)
    return count


# ---------- обходи (без рекурсії) ----------

def dfs_order(root: Node) -> List[Node]:
    """
    Обхід у глибину (preorder) за допомогою СТЕКУ.
    Порядок: корінь → лівий → правий. Для preorder праве піддерево кладемо в стек
    раніше за ліве, щоб ліве оброблялося першим.
    """
    order: List[Node] = []
    if root is None:
        return order
    stack = [root]
    while stack:
        node = stack.pop()
        order.append(node)
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)
    return order


def bfs_order(root: Node) -> List[Node]:
    """Обхід у ширину (level-order) за допомогою ЧЕРГИ (deque)."""
    order: List[Node] = []
    if root is None:
        return order
    queue: deque[Node] = deque([root])
    while queue:
        node = queue.popleft()
        order.append(node)
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)
    return order


# ---------- візуалізація ----------

def visualize_traversal(root: Node, traversal: str = "bfs",
                        save_path: Optional[str] = None) -> List:
    """Розфарбовує дерево відповідно до обраного обходу і малює його."""
    traversal = traversal.lower()
    if traversal == "dfs":
        order = dfs_order(root)
        hue = 0.08          # оранжевий
        title = "DFS (preorder, стек)"
    elif traversal == "bfs":
        order = bfs_order(root)
        hue = 0.58          # синій
        title = "BFS (level-order, черга)"
    else:
        raise ValueError("traversal має бути 'dfs' або 'bfs'")

    total = len(order)
    for i, node in enumerate(order):
        node.color = gradient_color(i, total, hue)

    tree = nx.DiGraph()
    pos = {root.id: (0.0, 0.0)}
    tree = add_edges(tree, root, pos)

    colors = [data["color"] for _, data in tree.nodes(data=True)]
    labels = {node_id: data["label"] for node_id, data in tree.nodes(data=True)}

    plt.figure(figsize=(11, 6))
    nx.draw(tree, pos=pos, labels=labels, arrows=False,
            node_size=2200, node_color=colors, font_weight="bold",
            font_color="white", font_size=11)
    plt.title(
        f"{title}.  Порядок відвідування: {[n.val for n in order]}",
        fontsize=11,
    )
    if save_path:
        plt.savefig(save_path, dpi=100, bbox_inches="tight")
        plt.close()
    else:
        plt.show()
    return [n.val for n in order]


# ---------- демонстрація ----------

def build_sample_tree() -> Node:
    """Те саме дерево, що в умові завдання 4."""
    root = Node(0)
    root.left = Node(4)
    root.left.left = Node(5)
    root.left.right = Node(10)
    root.right = Node(1)
    root.right.left = Node(3)
    root.right.right = Node(8)
    root.left.left.left = Node(7)
    root.left.right.right = Node(2)
    return root


if __name__ == "__main__":
    print("DFS:")
    visualize_traversal(build_sample_tree(), traversal="dfs")

    print("BFS:")
    visualize_traversal(build_sample_tree(), traversal="bfs")
