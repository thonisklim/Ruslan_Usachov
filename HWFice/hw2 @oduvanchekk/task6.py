def island_perimeter(island):
    perimeter = 0
    for y in range(len(island)):
        for x in range(len(island[y])):
            # max perimeter per tile is 4, so i add 4 and decrease
            # value depending on if it is a land tile next to tile (x, y)
            if island[y][x] == 'X':
                perimeter += 4 - (island[y][x - 1] == 'X') * (x != 0) - (island[y - 1][x] == 'X') * (y != 0)
                if x != len(island[y]) - 1:
                    perimeter -= island[y][x + 1] == 'X'
                if y != len(island) - 1:
                    perimeter -= island[y + 1][x] == 'X'
    return f"Total land perimeter: {perimeter}"


print(island_perimeter(['OXXOOOXX',
                        'OOOXOOOX',
                        'OOOXOOOX',
                        'OXXXXOXX',
                        'OOOOXXXO']))
