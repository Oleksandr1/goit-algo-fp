"""
Завдання 2. Фрактал «дерево Піфагора» через рекурсію.

Класична побудова: на верхній стороні квадрата будується прямокутний
трикутник, а на двох його катетах — два менших квадрати. Так рекурсивно,
поки не досягнемо вказаного рівня глибини.

Кут при лівому катеті за замовчуванням 45° — у цьому випадку дерево симетричне
і обидва нащадки мають сторону side · √2/2.
"""

from __future__ import annotations
import argparse
import math
from typing import List, Tuple

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

Point = Tuple[float, float]


def square_corners(x: float, y: float, side: float, angle: float) -> List[Point]:
    """
    Чотири кути квадрата зі стороною side та нижнім лівим кутом (x, y).
    Нижня сторона повернута на кут angle (радіани) відносно осі X.
    Повертає список [BL, BR, TR, TL].
    """
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    bl = (x, y)
    br = (x + side * cos_a, y + side * sin_a)
    # Верхні кути отримуємо, додаючи перпендикулярну сторону «вгору»:
    # нормаль до нижньої сторони, повернута на +90°, це (-sin, cos)
    tr = (br[0] - side * sin_a, br[1] + side * cos_a)
    tl = (x - side * sin_a, y + side * cos_a)
    return [bl, br, tr, tl]


def draw_pythagoras_tree(
    depth: int,
    left_angle_deg: float = 45.0,
    initial_side: float = 1.0,
) -> None:
    """Будує і відображає дерево Піфагора заданого рівня рекурсії."""
    if depth < 0:
        raise ValueError("Рівень рекурсії має бути невід'ємним.")

    left_angle = math.radians(left_angle_deg)
    squares: List[List[Point]] = []  # сюди збираємо квадрати для одного PatchCollection

    def recurse(x: float, y: float, side: float, angle: float, level: int) -> None:
        if level > depth:
            return

        corners = square_corners(x, y, side, angle)
        squares.append(corners)

        if level == depth:
            return  # листя — далі не йдемо

        tl = corners[3]  # верхній лівий кут поточного квадрата

        # Нащадки:
        # Лівий стоїть на стороні TL→T, де T — верхня точка трикутника.
        #   side_left  = side * cos(left_angle)
        #   angle_left = angle + left_angle
        # Правий стоїть на стороні T→TR.
        #   side_right  = side * sin(left_angle)
        #   angle_right = angle + left_angle - 90°
        side_left = side * math.cos(left_angle)
        angle_left = angle + left_angle

        # Точка T — нижній лівий кут правого нащадка
        t_x = tl[0] + side_left * math.cos(angle_left)
        t_y = tl[1] + side_left * math.sin(angle_left)

        side_right = side * math.sin(left_angle)
        angle_right = angle + left_angle - math.pi / 2

        recurse(tl[0], tl[1], side_left, angle_left, level + 1)
        recurse(t_x, t_y, side_right, angle_right, level + 1)

    recurse(0.0, 0.0, initial_side, 0.0, 0)

    # ---- візуалізація ----
    fig, ax = plt.subplots(figsize=(9, 9))

    # Колір залежить від «віку» квадрата у списку — кореневий темний, листя світліші.
    # Це дає природний градієнт від стовбура до крони.
    n = len(squares)
    polygons = [Polygon(sq, closed=True) for sq in squares]
    collection = PatchCollection(polygons, alpha=0.85, edgecolor="black", linewidth=0.4)
    # Зелений градієнт: від темно-коричневого (стовбур) до яскраво-зеленого (крона)
    colors = [
        (
            0.3 + 0.2 * (i / max(n - 1, 1)),
            0.2 + 0.6 * (i / max(n - 1, 1)),
            0.1 + 0.1 * (i / max(n - 1, 1)),
        )
        for i in range(n)
    ]
    collection.set_facecolor(colors)
    ax.add_collection(collection)

    ax.set_aspect("equal")
    ax.autoscale_view()
    ax.set_title(f"Дерево Піфагора (рівень рекурсії = {depth})", fontsize=13)
    ax.axis("off")
    plt.tight_layout()
    plt.show()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Фрактал «дерево Піфагора».")
    p.add_argument(
        "-d", "--depth",
        type=int,
        default=None,
        help="Рівень рекурсії (за замовчуванням питається у користувача).",
    )
    p.add_argument(
        "-a", "--angle",
        type=float,
        default=45.0,
        help="Кут при лівому катеті трикутника, градуси (default: 45).",
    )
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.depth is None:
        try:
            depth = int(input("Введіть рівень рекурсії (рекомендовано 6–12): "))
        except ValueError:
            print("Очікувалося ціле число. Використовую 8 за замовчуванням.")
            depth = 8
    else:
        depth = args.depth

    if depth > 15:
        print(f"Увага: глибина {depth} створить ~2^{depth} квадратів — може бути повільно.")

    draw_pythagoras_tree(depth=depth, left_angle_deg=args.angle)
