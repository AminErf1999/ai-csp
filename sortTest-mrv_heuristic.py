from copy import deepcopy
variables = '1 2 3 4 5 6 7 8 9 10'.split()
domains = {}
for variable in variables:
    domains[variable] = ['+']

domains['10'].append('-')
domains['9'].append('-')
domains['8'].append('-')
domains['7'] = domains['7'] + ['-', '0']
domains['6'] = domains['6'] + ['-', '0']
domains['5'] = domains['5'] + ['-', '0']
domains['4'] = domains['4'] + ['-', '0', '1']


variables.sort(key=lambda variable: len(domains[variable]))

new_domains = deepcopy(domains)

for v in variables:
    new_domains[v].remove('+')

for variable in variables:
    print(domains[variable])
    print(new_domains[variable])
    print('__________')
