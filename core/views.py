'''
Github: https://github.com/Sohail342

 LinkedIn: https://www.linkedin.com/in/sohailahmad3428041928/
'''

from django.shortcuts import render
import string
from itertools import product
from django.http import HttpResponse

def generate_truth_table(num_vars):
    letters = list(string.ascii_uppercase[15:])  # Starting from 'P'
    headers = [letter for letter in letters[:num_vars]]  # Header from P to variables ( if user enter 3: P, Q, and R)
    truth_table = list(product([True, False], repeat=num_vars))
    truth_table_str = [['True' if val else 'False' for val in row] for row in truth_table]
    return headers, truth_table_str

def generate_prepositions(num_vars, headers, rows, preposition=None):
    if preposition and num_vars > 1:
        # Generate new header for the preposition
        preposition_header = f'P {preposition} Q'
        headers.append(preposition_header)
        
        # logical operation based on the preposition
        for i, row in enumerate(rows):
            if preposition == "AND":
                result = 'True' if row[0] == 'True' and row[1] == 'True' else 'False'
            elif preposition == "OR":
                result = 'True' if row[0] == 'True' or row[1] == 'True' else 'False'
            elif preposition == "NAND":
                result = 'False' if row[0] == 'True' and row[1] == 'True' else 'True'
            elif preposition == "NOR":
                result = 'False' if row[0] == 'True' or row[1] == 'True' else 'True'
            elif preposition == "XOR":
                result = 'True' if row[0] != row[1] else 'False'
            elif preposition == "XNOR":
                result = 'True' if row[0] == row[1] else 'False'
            elif preposition == "IMPLIES":
                result = 'False' if row[0] == 'True' and row[1] == 'False' else 'True'
            elif preposition == "BICOND":
                result = 'True' if row[0] == row[1] else 'False'
            rows[i].append(result)
    elif num_vars == 1:
        # Handle negation if num_vars is 1
        headers.append('~P')
        for i, row in enumerate(rows):
            negated_value = 'False' if row[0] == 'True' else 'True'
            rows[i].append(negated_value)

def table(request):
    context = {}
    if request.method == "GET":
        try:
            var = request.GET.get('variable', '2')  # Default to 2 variables
            num_vars = int(var)
            preposition = request.GET.get('preposition', None)
            
            if num_vars >= 1 and num_vars <= 9:    # Validate Variables must be within 1-9 Range
            # Generate headers and truth table rows
                headers, rows = generate_truth_table(num_vars)
            
            # Generate prepositions and update headers and rows
            generate_prepositions(num_vars, headers, rows, preposition)
            
            context = {
                "headerName": headers,
                'rows': rows,
                'variable': num_vars,
            }
        except:
           return HttpResponse("<h1>Please check your inputs and ensure they are correct.<h1>")
            
    return render(request, 'core/index.html', context)
