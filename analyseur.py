import re
# Définition des expressions régulières pour les lexèmes
token_patterns = [
(r'\d+', 'n'), # Nombre entier
(r'\+', '+'), # Opérateur plus
(r'\*', '*'), # Opérateur multiplication
(r'\(', '('), # Parenthèse ouvrante
(r'\)', ')') # Parenthèse fermante
]
# La grammaire de l'analyseur syntaxique
grammaire = {
"A": { "n": "CB", "+": None, "*": None, "(": "CB", ")": None, "$": None },
"B": { "n": None, "+": "+CB", "*": None, "(": None, ")": "", "$": "" },
"C": { "n": "ED", "+": None, "*": None, "(": "ED", ")": None, "$": None },
"D": { "n": None, "+": "", "*": "*ED", "(": None, ")": "", "$": "" },
"E": { "n": "n", "+": None, "*": None, "(": "(A)", ")": None, "$": None }
}
# Fonction pour générer la table d'analyse de la grammaire
def generate_table(grammaire):
table = {}
for non_terminal in grammaire:
productions = grammaire[non_terminal]
table[non_terminal] = {}
for terminal, action in productions.items():
if action is None:
action = "" # Assigner une valeur vide si l'action est None
table[non_terminal][terminal] = action
return table
def print_table(table):
for non_terminal, productions in table.items():
print(non_terminal + ":")
for terminal, action in productions.items():
print("\t" + terminal + " -> " + str(action))
table = generate_table(grammaire)
# Fonction d'analyse lexicale
def lexer(input_string):
tokens = []
input_string = input_string.replace(" ", "") # Supprimer les espaces
while input_string:
match = None
for pattern, token_type in token_patterns:
regex = re.compile(pattern)
match = regex.match(input_string)
if match:
value = match.group(0)
tokens.append((value, token_type))
input_string = input_string[len(value):]
break
if not match:
raise ValueError("Invalid input: " + input_string)
return tokens
#Fonction pour vérifier si un symbole x est un terminal
def isTerminal(x):
return x in "()+*n"
# Fonction d'analyse syntaxique
def Uparser(symbols):
stack = ["$", "A"]
a = symbols.pop(0)
step = 1
while True:
x = stack[-1]
if x == "$" and a == "$":
print("Étape", step, ": Analyse terminée avec succès.")
return True
if x == a and x != "$":
stack.pop()
if len(symbols) > 0:
a = symbols.pop(0)
else:
a = "$"
step += 1
print("Étape", step, ": Symbole terminal correctement analysé.")
continue
if not isTerminal(x):
p = grammaire[x][a]
if p is None:
print("Étape", step, ": Incompatibilité entre le symbole de la pile et le symbole d'entrée.")
return False
else:
stack.pop()
stack.extend(list(p[::-1]))
step += 1
print("Étape", step, ": Application de la règle de production :", x, "->", p)
continue
print("Étape", step, ": Incompatibilité entre le symbole de la pile et le symbole d'entrée.")
return False
# Demander à l'utilisateur d'entrer l'expression pour la verifier :
input_expression = input("Entrez une expression : ")
# Analyse lexicale
try:
tokens = lexer(input_expression)
print("\nAnalyse lexicale réussie.")
print("Lexèmes :", tokens)
except ValueError as e:
print("\nErreur lors de l'analyse lexicale :", e)
# Analyse syntaxique
print("\nTrace de l'Analyse Syntaxique :")
syntax_correct = Uparser([token_type for _, token_type in tokens])
# Vérification finale
if syntax_correct:
print("L'expression est correcte lexicalement et syntaxiquement.")
else:
print("L'expression est incorrecte syntaxiquement.")
# Utilisation de la fonction print_table pour afficher la table d'analyse
print("\nGeneration de la table d'analyse")
print_table(table)