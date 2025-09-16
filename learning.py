import random
import copy

# int rand_int(int a, int b)
# {
#     return a + rand() % (b - a + 1);
# }

size = 0
while size < 4 or size > 24 or size % 2 == 1:
    input_string = input("棋譜のサイズ(4~24の偶数)? ")
    if input_string.isdigit():
        size = int(input_string)

# 完成形の盤面をランダムに生成
def try_creating_field(size):
    field = [[None] * size for _ in range(size)]
    unused_numbers = [number for number in range(size * size // 2)]
    for y in range(size):
        for x in range(size):
            # 既に数値があるならスキップ
            if field[y][x] != None:
                continue
            picked_number = random.choice(unused_numbers)
            field[y][x] = picked_number
            can_place_horizontally = x + 1 < size and field[y][x + 1] == None
            can_place_vertically = y + 1 < size and field[y + 1][x] == None
            if can_place_horizontally:
                if can_place_vertically and random.random() < 0.5:
                    field[y + 1][x] = picked_number
                else:
                    field[y][x + 1] = picked_number
            elif can_place_vertically:
                field[y + 1][x] = picked_number
            else:
                # ペアを置く場所がなくなった
                return (False, field)
            unused_numbers.remove(picked_number)
    return (True, field)

field = None
while True:
    is_successful, temporary_field = try_creating_field(size)
    if is_successful:
        field = temporary_field
        break

for y in range(size):
    for x in range(size):
        print(field[y][x], end=" ")
    print()
print()

field_history = []
operation_history = []
while True:
    # ランダムな位置で左回転
    n = random.randint(2, size)
    x = random.randint(0, size - n)
    y = random.randint(0, size - n)
    memo = [[None] * n for _ in range(n)]
    for dy in range(n):
        for dx in range(n):
            memo[dy][dx] = field[y + dx][x + n - 1 - dy]
    for dy in range(n):
        for dx in range(n):
            field[y + dy][x + dx] = memo[dy][dx]

    # 操作履歴に追加
    field_history.append(copy.deepcopy(field))
    operation_history.append((x, y, n))    

    print(f"x: {x}, y: {y}, n: {n}")
    for y in range(size):
        for x in range(size):
            print(field[y][x], end=" ")
        print()
    print()

    pair_exists = False
    first_pair_coordinates = {}
    for y in range(size):
        for x in range(size):
            if field[y][x] in first_pair_coordinates:
                # 同じ値のエンティティが既に見つかっているので、隣接しているか判定
                first_pair_x, first_pair_y = first_pair_coordinates[field[y][x]]
                if abs(x - first_pair_x) + abs(y - first_pair_y) == 1:
                    pair_exists = True
                    break
            else:
                # 初めて出る値のエンティティなので、座標を覚える
                first_pair_coordinates[field[y][x]] = (x, y)
        if pair_exists:
            break
    # ペアがなくなったら終了
    if not pair_exists:
        break
