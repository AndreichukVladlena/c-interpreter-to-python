import re


def read_c_file(file_path):
    try:
        with open(file_path, 'r') as file:
            c_code = file.read()
        return c_code
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None

def tokenize_c_code(c_code):
    patterns = [
        (r'(#include.*?)(?:;|\n)', 'LIBRARY_INCLUDE'),
        (r'\/\/.*', 'COMMENT'),
        (r'\/\*.*?\*\/', 'MULTILINE_COMMENT'),
        (r'["\']([^"\']*)["\']', 'STRING_LITERAL'),
        (r'\b(const\s+)?\b((struct)\s+([a-zA-Z_][a-zA-Z0-9_]*)|void|bool|int|float|double|char|char\[\]|char\*)\b', 'DATA_TYPE'),
        (r'\b(for|while|do)\b', 'LOOP_OPERATOR'),
        (r'\b(return|break|continue)\b', 'CONTROL_OPERATOR'),
        (r'\b(if|else|switch|case)\b', 'CONDITION_OPERATOR'),
        (r'\b(true|false)\b', 'BOOLEAN_VARIABLES'),
        (r'\b\d+(\.\d+)?\b', 'NUMERIC_VARIABLES'),
        (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', 'IDENTIFIER'),
        (r'(&&|\|\|)', 'LOGICAL'),
        (r'(>=|<=|!=|==|>|<)', 'COMPARISON'),
        (r'((?<![<>])=|\+=|\-=|\*=|\/=|%=)', 'EQUALITY'),
        (r'(\+|\-)', 'ARITHMETIC_TERM'),
        (r'(\*|\/)', 'ARITHMETIC_FACTOR'),
        (r'\+\+|--|\*|&|!|~', 'UNARY'),
        (r'(\(|\)|\[|\]|\{|\})', 'GROUPING'),
        (r'(\,|\;)', 'SEPARATOR'),
        (r'(\.)', 'DOT'),
        (r'\?|:', 'TERNARY_OPERATOR'),
        (r'\s+', 'WHITESPACE')
    ]

    combined_pattern = '|'.join('(?P<%s>%s)' % (name, pattern) for pattern, name in patterns)

    tokens = []
    for match in re.finditer(combined_pattern, c_code):
        for i, (_, name) in enumerate(patterns):
            if match.group(name):
                token_value = match.group(name)
                if token_value.strip():
                    if token_value.strip() == "(":
                        if tokens[-1][0] == 'VARIABLE_IDENTIFIER':
                            tokens[-1] = 'FUNCTION_IDENTIFIER', tokens[-1][1]
                    if name == "IDENTIFIER":
                        name = 'VARIABLE_IDENTIFIER'

                    if token_value.strip() == '+' and tokens[-1][1] == '+':
                        tokens.pop()
                        tokens.append(("UNARY", '++'))
                        continue
                    if token_value.strip() == '-' and tokens[-1][1] == '-':
                        tokens.pop()
                        tokens.append(("UNARY", '--'))
                        continue

                    tokens.append((name, token_value.strip()))

                break

    tokens.append(('END_OF_FILE', 'EOF'))
    return tokens


def is_function(identifier, c_code):
    return f"{identifier}(" in c_code

def count_single_quotes(text):
    return text.count("'")

def count_double_quotes(text):
    return text.count('"')

def find_unclosed_quotes(text):
    single_quotes_count = count_single_quotes(text)
    double_quotes_count = count_double_quotes(text)
    if single_quotes_count % 2 != 0:
        raise ValueError("Unclosed single quotes detected.")
    if double_quotes_count % 2 != 0:
        raise ValueError("Unclosed double quotes detected.")


def count_multiline_comments(text):
    return text.count('/*')

def find_unclosed_comments(text):
    comment_start_count = count_multiline_comments(text)
    comment_end_count = text.count('*/')
    if comment_start_count != comment_end_count:
        raise ValueError("Unclosed multiline comments detected.")



