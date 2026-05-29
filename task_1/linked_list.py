"""
Завдання 1. Однозв'язний список.

Реалізовано:
  - reverse: реверсування списку зміною посилань між вузлами (in-place);
  - merge_sort: сортування злиттям (O(n log n), стабільне);
  - merge_two_sorted: об'єднання двох відсортованих списків в один відсортований.
"""

from __future__ import annotations
from typing import Optional, Iterable


class Node:
    """Вузол однозв'язного списку."""

    def __init__(self, data, next_node: Optional["Node"] = None):
        self.data = data
        self.next = next_node

    def __repr__(self) -> str:
        return f"Node({self.data!r})"


class LinkedList:
    """Однозв'язний список з мінімально необхідним API."""

    def __init__(self, iterable: Optional[Iterable] = None):
        self.head: Optional[Node] = None
        if iterable is not None:
            for value in iterable:
                self.append(value)

    # ---------- базові операції ----------

    def append(self, data) -> None:
        """Додає елемент у кінець. O(n) — для простоти без tail-вказівника."""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node

    def to_list(self) -> list:
        """Повертає вміст у вигляді звичайного Python-списку (для друку та тестів)."""
        result, current = [], self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def __repr__(self) -> str:
        return " -> ".join(map(str, self.to_list())) or "<empty>"

    # ---------- 1.1 Реверсування ----------

    def reverse(self) -> None:
        """
        Реверсує список in-place, змінюючи посилання між вузлами.
        Класичний three-pointer-підхід: prev / current / next_node.
        Складність: час O(n), пам'ять O(1).
        """
        prev: Optional[Node] = None
        current = self.head
        while current is not None:
            next_node = current.next   # запам'ятати наступний
            current.next = prev        # розвернути посилання
            prev = current             # зсунути prev
            current = next_node        # зсунути current
        self.head = prev

    # ---------- 1.2 Сортування злиттям ----------

    def sort(self) -> None:
        """Сортує список за зростанням (merge sort). O(n log n) часу, O(log n) стеку."""
        self.head = self._merge_sort(self.head)

    @classmethod
    def _merge_sort(cls, head: Optional[Node]) -> Optional[Node]:
        # База: 0 або 1 елемент — вже відсортовано
        if head is None or head.next is None:
            return head

        # Розбиваємо список на дві половини через "повільний/швидкий" вказівники
        left_head, right_head = cls._split(head)

        # Рекурсивно сортуємо кожну половину
        left_sorted = cls._merge_sort(left_head)
        right_sorted = cls._merge_sort(right_head)

        # Зливаємо дві відсортовані половини
        return cls._merge_nodes(left_sorted, right_sorted)

    @staticmethod
    def _split(head: Node) -> tuple[Node, Optional[Node]]:
        """
        Ділить список навпіл. Повертає голови лівої і правої частин.
        Використовує техніку slow/fast pointer: fast рухається удвічі швидше за slow.
        """
        slow, fast = head, head.next
        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next
        right_head = slow.next
        slow.next = None  # розрив зв'язку між половинами
        return head, right_head

    @staticmethod
    def _merge_nodes(a: Optional[Node], b: Optional[Node]) -> Optional[Node]:
        """Об'єднує два відсортованих ланцюжки вузлів. Спільна логіка для sort і merge."""
        dummy = Node(None)   # технічний фіктивний вузол спрощує код
        tail = dummy
        while a is not None and b is not None:
            if a.data <= b.data:
                tail.next = a
                a = a.next
            else:
                tail.next = b
                b = b.next
            tail = tail.next
        tail.next = a if a is not None else b  # дописуємо залишок
        return dummy.next


# ---------- 1.3 Об'єднання двох відсортованих списків ----------

def merge_two_sorted(list_a: LinkedList, list_b: LinkedList) -> LinkedList:
    """
    Об'єднує два ВЖЕ ВІДСОРТОВАНИХ списки в один відсортований.
    Не створює нових вузлів — переплітає існуючі (O(n + m) часу, O(1) пам'яті).

    Увага: після виклику list_a та list_b слід вважати "спожитими"
    — їхні вузли тепер належать результуючому списку.
    """
    merged = LinkedList()
    merged.head = LinkedList._merge_nodes(list_a.head, list_b.head)
    list_a.head = None
    list_b.head = None
    return merged


# ---------- демонстрація ----------

if __name__ == "__main__":
    # 1.1 Реверс
    ll = LinkedList([1, 2, 3, 4, 5])
    print("Початковий список:    ", ll)
    ll.reverse()
    print("Після реверсування:   ", ll)

    # 1.2 Сортування
    ll2 = LinkedList([4, 2, 8, 1, 9, 3, 7, 5, 6])
    print("\nНевідсортований:      ", ll2)
    ll2.sort()
    print("Після merge sort:     ", ll2)

    # Граничні випадки сортування
    empty = LinkedList()
    empty.sort()
    print("Порожній після sort:  ", empty)

    single = LinkedList([42])
    single.sort()
    print("З одного елемента:    ", single)

    # 1.3 Об'єднання двох відсортованих
    a = LinkedList([1, 3, 5, 7, 9])
    b = LinkedList([2, 4, 6, 8, 10])
    print("\nСписок A:             ", a)
    print("Список B:             ", b)
    merged = merge_two_sorted(a, b)
    print("Об'єднаний (A ⊕ B):   ", merged)

    # Перевірка з нерівними довжинами
    c = LinkedList([0, 100])
    d = LinkedList([1, 2, 3, 4, 5])
    print("\nСписок C:             ", c)
    print("Список D:             ", d)
    print("Об'єднаний (C ⊕ D):   ", merge_two_sorted(c, d))
