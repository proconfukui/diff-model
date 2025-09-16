import os
import random
import copy
import pickle

# 全てのペアが揃った盤面のランダム生成を試みる
# 失敗した場合はNoneを返す
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
                return None
            unused_numbers.remove(picked_number)
    return field

# 1回分の棋譜を作成する
def create_record(size):
    # 盤面の初期化
    field = None
    while field is None:
        field = try_creating_field(size)

    field_history = []
    operation_history = []
    while True:
        # ランダムな位置と園の大きさで左回転
        # 導きは右回転のみなので、その逆の操作をすることで学習データを作る
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
            return (field_history, operation_history)


size = 0
while size < 4 or size > 24 or size % 2 == 1:
    input_string = input("棋譜のサイズ(4~24の偶数)? ")
    if input_string.isdigit():
        size = int(input_string)

# 同じサイズの棋譜データがファイルとして存在する場合、読み込む
records = []
record_path = f"records_{size}.pickle"
if os.path.isfile(record_path):
    with open(record_path, mode="rb") as file:
        records = pickle.load(file)
    print(f"{record_path} から読み込み完了")

generation_count = 0
while generation_count == 0:
    input_string = input("棋譜の生成回数? ")
    if input_string.isdigit():
        generation_count = int(input_string)


while generation_count > 0:
    print(f"残り{generation_count}回")
    records.append(create_record(size))
    generation_count -= 1

# 生成した棋譜データをファイルに記録
with open(record_path, mode="wb") as file:
    pickle.dump(records, file)
print(f"{record_path} に記録完了")
