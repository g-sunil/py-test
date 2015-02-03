import random


def bubble_sort(items):
    "Bubble Sort"
    for i in range(len(items)):
        for j in range(len(items)):
            if items[i] < items[j]:
                items[j], items[i] = items[i], items[j]


if __name__ == '__main__':
    random_items = [random.randint(-50, 100) for c in range(32)]

    print 'Before: ', random_items, len(random_items)
    bubble_sort(random_items)
    print 'After: ', random_items, len(random_items)
