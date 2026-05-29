"""
Завдання 7. Метод Монте-Карло для двох гральних кубиків.

Симулюємо N кидків двох кубиків, рахуємо частоту кожної суми (2..12)
і порівнюємо з аналітичним розподілом.

Аналітика: при двох справедливих 6-гранних кубиках усього 36 рівноймовірних
комбінацій. Для суми s кількість сприятливих результатів дорівнює числу пар
(i, j), де i + j = s. Звідси добре відомий «трикутник» 1/36, 2/36, ..., 6/36, ..., 1/36.
"""

from __future__ import annotations
import argparse
import random
from collections import Counter
from typing import Dict, Tuple

import matplotlib.pyplot as plt


# Аналітичні ймовірності (frac 36)
ANALYTICAL: Dict[int, float] = {
    2: 1 / 36, 3: 2 / 36, 4: 3 / 36, 5: 4 / 36, 6: 5 / 36, 7: 6 / 36,
    8: 5 / 36, 9: 4 / 36, 10: 3 / 36, 11: 2 / 36, 12: 1 / 36,
}


def simulate(n_throws: int, seed: int | None = None) -> Dict[int, float]:
    """Виконує n_throws кидків і повертає словник sum -> emp_probability."""
    if seed is not None:
        random.seed(seed)
    counts = Counter()
    for _ in range(n_throws):
        s = random.randint(1, 6) + random.randint(1, 6)
        counts[s] += 1
    return {s: counts.get(s, 0) / n_throws for s in range(2, 13)}


def format_table(empirical: Dict[int, float], n_throws: int) -> str:
    """Форматує таблицю порівняння emp vs analytical для виводу в консоль."""
    lines = [
        f"Симуляція: {n_throws:,} кидків".replace(",", " "),
        "",
        f"{'Сума':<6}{'Емпірична':>14}{'Аналітична':>14}{'Δ (в.п.)':>12}",
        "-" * 46,
    ]
    total_abs_err = 0.0
    for s in range(2, 13):
        emp = empirical[s]
        ana = ANALYTICAL[s]
        delta = (emp - ana) * 100  # у відсоткових пунктах
        total_abs_err += abs(delta)
        lines.append(f"{s:<6}{emp*100:>12.3f}%{ana*100:>12.3f}%{delta:>+11.3f}")
    lines.append("-" * 46)
    lines.append(f"Сумарна абсолютна похибка: {total_abs_err:.3f} в.п.")
    return "\n".join(lines)


def plot_comparison(empirical: Dict[int, float], n_throws: int,
                    save_path: str | None = None) -> None:
    """Будує стовпчасту діаграму: emp vs analytical поруч."""
    sums = list(range(2, 13))
    emp_vals = [empirical[s] * 100 for s in sums]
    ana_vals = [ANALYTICAL[s] * 100 for s in sums]

    fig, ax = plt.subplots(figsize=(11, 6))
    width = 0.38
    x = range(len(sums))
    bars_emp = ax.bar([i - width / 2 for i in x], emp_vals, width,
                      label=f"Монте-Карло (N = {n_throws:,})".replace(",", " "),
                      color="#3b82f6")
    bars_ana = ax.bar([i + width / 2 for i in x], ana_vals, width,
                      label="Аналітично", color="#f59e0b")

    # Підписи над стовпцями
    for bar in list(bars_emp) + list(bars_ana):
        height = bar.get_height()
        ax.annotate(f"{height:.2f}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", fontsize=8)

    ax.set_xticks(list(x))
    ax.set_xticklabels(sums)
    ax.set_xlabel("Сума на двох кубиках")
    ax.set_ylabel("Ймовірність, %")
    ax.set_title("Ймовірності сум: метод Монте-Карло vs аналітика")
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=100, bbox_inches="tight")
        plt.close()
    else:
        plt.show()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Симуляція кидання двох кубиків методом Монте-Карло.")
    p.add_argument("-n", "--throws", type=int, default=100_000,
                   help="Кількість кидків (default: 100 000).")
    p.add_argument("--seed", type=int, default=42,
                   help="Зерно ГПВЧ для відтворюваності (default: 42).")
    p.add_argument("--no-plot", action="store_true",
                   help="Не показувати графік (тільки таблиця).")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    empirical = simulate(args.throws, seed=args.seed)
    print(format_table(empirical, args.throws))
    if not args.no_plot:
        plot_comparison(empirical, args.throws)
