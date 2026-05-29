"""
Завдання 6. Жадібний алгоритм та динамічне програмування для вибору їжі.

Задано бюджет і набір страв з вартістю та калорійністю. Треба максимізувати
сумарну калорійність, не перевищуючи бюджет. Кожну страву беремо не більше
одного разу (0/1 knapsack).

Реалізовано два підходи:
  - greedy_algorithm: сортує страви за співвідношенням калорій/вартість
    і бере, поки вистачає бюджету. Швидкий, але не гарантує оптимум.
  - dynamic_programming: класичний 0/1 knapsack по бюджету. Гарантує оптимум
    за O(n · budget) часу і пам'яті.
"""

from __future__ import annotations
from typing import Dict, List, Tuple


Items = Dict[str, Dict[str, int]]


# ---------- 6.1 Жадібний алгоритм ----------

def greedy_algorithm(items: Items, budget: int) -> Tuple[List[str], int, int]:
    """
    Жадібний вибір: страви сортуються за спаданням відношення калорій/вартість,
    і беруться доти, доки залишається бюджет на наступну.

    Повертає: (список_вибраних_страв, сумарна_вартість, сумарна_калорійність).
    Складність: O(n log n) — домінує сортування.
    """
    # Сортуємо за «щільністю калорій» — скільки калорій на одну грошову одиницю
    ranked = sorted(
        items.items(),
        key=lambda kv: kv[1]["calories"] / kv[1]["cost"],
        reverse=True,
    )

    chosen: List[str] = []
    total_cost = 0
    total_calories = 0

    for name, props in ranked:
        if total_cost + props["cost"] <= budget:
            chosen.append(name)
            total_cost += props["cost"]
            total_calories += props["calories"]

    return chosen, total_cost, total_calories


# ---------- 6.2 Динамічне програмування ----------

def dynamic_programming(items: Items, budget: int) -> Tuple[List[str], int, int]:
    """
    0/1 knapsack: dp[i][b] — максимум калорій, використавши перші i страв при бюджеті b.
    Перехід: або не беремо i-у страву (dp[i-1][b]), або беремо, якщо вистачає бюджету
    (dp[i-1][b - cost_i] + calories_i).

    Повертає: (список_вибраних_страв, сумарна_вартість, сумарна_калорійність).
    Складність: O(n · budget) часу і пам'яті.
    """
    names = list(items.keys())
    n = len(names)
    if n == 0 or budget <= 0:
        return [], 0, 0

    # dp[i][b]: i — кількість розглянутих страв, b — бюджет від 0 до budget
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        name = names[i - 1]
        cost = items[name]["cost"]
        calories = items[name]["calories"]
        for b in range(budget + 1):
            # Варіант 1: не беремо поточну страву
            dp[i][b] = dp[i - 1][b]
            # Варіант 2: беремо, якщо вміщається
            if cost <= b:
                take = dp[i - 1][b - cost] + calories
                if take > dp[i][b]:
                    dp[i][b] = take

    # Відновлюємо вибір, рухаючись від dp[n][budget] назад
    chosen: List[str] = []
    b = budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            # цю страву взяли
            name = names[i - 1]
            chosen.append(name)
            b -= items[name]["cost"]
    chosen.reverse()

    total_cost = sum(items[name]["cost"] for name in chosen)
    total_calories = dp[n][budget]
    return chosen, total_cost, total_calories


# ---------- демонстрація ----------

ITEMS: Items = {
    "pizza":     {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog":   {"cost": 30, "calories": 200},
    "pepsi":     {"cost": 10, "calories": 100},
    "cola":      {"cost": 15, "calories": 220},
    "potato":    {"cost": 25, "calories": 350},
}


def print_result(label: str, chosen: List[str], cost: int, calories: int, budget: int) -> None:
    print(f"\n[{label}]  бюджет={budget}")
    print(f"  Обрано:     {chosen}")
    print(f"  Вартість:   {cost} (з {budget})")
    print(f"  Калорій:    {calories}")


if __name__ == "__main__":
    for budget in (50, 75, 100, 150):
        g_items, g_cost, g_cal = greedy_algorithm(ITEMS, budget)
        d_items, d_cost, d_cal = dynamic_programming(ITEMS, budget)

        print("=" * 60)
        print_result("Greedy", g_items, g_cost, g_cal, budget)
        print_result("DP",     d_items, d_cost, d_cal, budget)
        diff = d_cal - g_cal
        if diff > 0:
            print(f"  → DP виграє у жадібного на {diff} калорій ({diff/g_cal:.1%})")
        elif diff == 0:
            print("  → На цьому бюджеті обидва алгоритми дають однаковий результат.")
