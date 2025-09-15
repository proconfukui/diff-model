#include <iostream>
#include <vector>
using namespace std;

int rand_int(int a, int b)
{
    return a + rand() % (b - a + 1);
}

int main()
{
    int size = 0;
    do
    {
        cout << "棋譜のサイズ(4~24の偶数)? ";
        cin >> size;
    } while (!(size >= 4 && size <= 24 && size % 2 == 0));

    // 完成形の盤面をランダムに生成
    vector<vector<int>> field;
    vector<int> unused_numbers;
retry:
    field = vector<vector<int>>(size, vector<int>(size, -1));
    unused_numbers = vector<int>(size * size / 2);
    for (int index = 0; index < size * size / 2; index++)
    {
        unused_numbers[index] = index;
    }
    for (int y = 0; y < size; y++)
    {
        for (int x = 0; x < size; x++)
        {
            // 既に数値があるならスキップ
            if (field[y][x] != -1)
            {
                continue;
            }
            int picked_index = rand_int(0, unused_numbers.size() - 1);
            int picked_number = unused_numbers[picked_index];
            field[y][x] = picked_number;
            bool can_place_horizontally = x + 1 < size && field[y][x + 1] == -1;
            bool can_place_vertically = y + 1 < size && field[y + 1][x] == -1;
            if (can_place_horizontally && can_place_vertically)
            {
                if (rand_int(0, 1) == 0)
                {
                    field[y][x + 1] = picked_number;
                }
                else
                {
                    field[y + 1][x] = picked_number;
                }
            }
            else if (can_place_horizontally && !can_place_vertically)
            {
                field[y][x + 1] = picked_number;
            }
            else if (!can_place_horizontally && can_place_vertically)
            {
                field[y + 1][x] = picked_number;
            }
            else
            {
                goto retry;
            }
            unused_numbers.erase(unused_numbers.begin() + picked_index);
        }
    }

    for (int y = 0; y < size; y++)
    {
        for (int x = 0; x < size; x++)
        {
            cout << field[y][x] << " ";
        }
        cout << endl;
    }
    return 0;

    // ペアがなくなるまで左回転を続ける
    while (true)
    {
        // ランダムな位置で左回転
        int n = rand_int(2, size);
        int x = rand_int(0, size - n), y = rand_int(0, size - n);

        // ペアがなくなったら終了
    }
}
