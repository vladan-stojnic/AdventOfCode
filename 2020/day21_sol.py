import collections

def read_input(path):
    with open(path, 'r') as f:
        data = f.read()
    data = data.splitlines()

    table = collections.defaultdict(lambda : list())
    ingredients_list = []

    for line in data:
        ingredients = line.split('(')[0]
        ingredients = ingredients.strip()
        ingredients = ingredients.split(' ')

        ingredients_list += ingredients

        alergenes = line.split('(')[1]
        alergenes = alergenes[9:-1]
        alergenes = alergenes.split(', ')

        for alergene in alergenes:
            table[alergene].append(set(ingredients))

    return table, ingredients_list

table, ingredients = read_input('day21')

# Part 1

ingredients_list = [v for vl in table.values() for v in vl ]

all_ingredients = set()

for i in ingredients_list:
    all_ingredients |= i

alergene_ingredient = {key: set.intersection(*value) for key, value in table.items()}

ingredients_in_alergene = set.union(*alergene_ingredient.values())

safe = all_ingredients.difference(ingredients_in_alergene)

counter = collections.Counter(ingredients)

res = 0
for s in safe:
    res += counter[s]

print(res)

# Part 2

claned = set()

for i in range(len(alergene_ingredient.keys())):
    to_clean = min([key for key in alergene_ingredient.keys() if key not in claned], key=lambda x: len(alergene_ingredient[x]))
    claned.add(to_clean)

    vals = alergene_ingredient[to_clean]

    for key in alergene_ingredient:
        if key != to_clean:
            alergene_ingredient[key] = alergene_ingredient[key].difference(set(vals))

sorted_alergenes = sorted([key for key in alergene_ingredient.keys()])

output = []

for key in sorted_alergenes:
    output+=list(alergene_ingredient[key])

print(','.join(output))