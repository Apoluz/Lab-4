class Item:
    def __init__(self, weight, value, abrev):
        self.weight = weight  
        self.value = value    
        self.abrev = abrev    

def knapsack(items, capacity, required_items):
    def node_bound_count(i, weight, value):
        if weight > capacity:
            return 0
        node_value = value
        j = i
        total_weight = weight

        while j < len(items) and total_weight + items[j].weight <= capacity:
            node_value += items[j].value
            total_weight += items[j].weight
            j += 1
        if j < len(items):
            node_value += (capacity - total_weight) * (items[j].value / items[j].weight)

        return node_value

    def branch_bound(i, weight, value, selected_items):
        nonlocal max_value, best_combination
        if weight <= capacity and value > max_value:
            max_value = value
            best_combination = selected_items.copy()

        if i == len(items):
            return 0
        if node_bound_count(i, weight, value) > max_value:
            branch_bound(i+1, weight, value, selected_items)

        if value + (capacity - weight) * (items[i].value / items[i].weight) > max_value:
            selected_items.append(items[i])
            branch_bound(i+1, weight + items[i].weight, value + items[i].value, selected_items)
            selected_items.pop()

   
    items = sorted(items, key=lambda x: x.value / x.weight, reverse=True)
    max_value = 0
    best_combination = []
    branch_bound(0, 0, 0, [])

    return best_combination, max_value



items = [
    Item(3, 25, 'r'),  # Винтовка (rifle)
    Item(2, 15, 'p'),  # Пистолет (pistol)
    Item(2, 15, 'a'),  # Боекомплект (ammo)
    Item(2, 20, 'm'),  # Аптечка (medkit)
    Item(1, 5, 'i'),   # Ингалятор (inhaler)
    Item(1, 15, 'k'),  # Нож (knife)
    Item(3, 20, 'x'),  # Топор (axe)
    Item(1, 25, 't'),  # Оберег (talisman)
    Item(1, 15, 'f'),  # Фляжка (flask)
    Item(1, 10, 'd'),  # Антидот (antidot)
    Item(2, 20, 's'),  # Еда (supplies)
    Item(2, 20, 'c')   # Арбалет (crossbow)
]


capacity = 9


required_items = ['i', 'd']


required_items_set = set(required_items)

filtered_items = [item for item in items if item.abrev in required_items_set]
items = [item for item in items if item.abrev not in required_items_set] + filtered_items


best_combination, max_value = knapsack(items, capacity, required_items)

print("Лучшее сочетание выбранных предметов:")
for item in best_combination:
    print(f"- {item.abrev} - {item.value} очков выживания")

print(f"Общее количество очков выживания: {max_value}")


inventory_grid = [[' ' for _ in range(3)] for _ in range(3)]
current_size = 0


for item in best_combination:
    size = item.weight
    abrev = item.abrev
    for i in range(size):
        row = (current_size // 3)
        col = current_size % 3
        inventory_grid[row][col] = abrev
        current_size += 1


print("\nИнвентарь в 3x3 (представление с аббревиатурами):")
for row in inventory_grid:
    print(' '.join(row))