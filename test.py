from cnl_parser import parser
from pymorphy3 import MorphAnalyzer

morph = MorphAnalyzer()

# принимает слово и ожидаемую часть речи в качестве входных данных и предлагает исправления на основе морфологического анализа. 
# Она разбирает слово на все возможные интерпретации, проверяет часть речи каждой интерпретации и добавляет подходящие предложения в список. 
# Функция возвращает строку с предложениями или сообщение, если подходящих предложений нет.

def recommend_correction(word, expected_pos):
    suggestions = []
    parse_results = morph.parse(word)
    
    for parse in parse_results:
        tag = parse.tag
        
        if expected_pos == 'NOUN' and tag.POS == 'NOUN':
            suggestions.append(parse.normal_form)
        elif expected_pos == 'VERB' and tag.POS == 'VERB':
            suggestions.append(parse.normal_form)
        elif expected_pos == 'ADVB' and tag.POS == 'ADVB':
            suggestions.append(parse.normal_form)
        elif expected_pos == 'ADJF' and tag.POS == 'ADJF':
            suggestions.append(parse.normal_form)
        elif expected_pos == 'INFN' and tag.POS == 'INFN':
            suggestions.append(parse.normal_form)
        elif expected_pos == 'PRTS' and tag.POS == 'PRTS':
            suggestions.append(parse.word)
        elif expected_pos == 'COMP' and tag.POS == 'COMP':
            suggestions.append(parse.normal_form + ' (comparative)')
        elif expected_pos == 'PRCL' and tag.POS == 'PRCL':
            suggestions.append(parse.word)

    if suggestions:
        return f"Did you mean: {', '.join(suggestions)}?"
    else:
        return f"No suitable suggestions for '{word}'."

def get_previous_and_next_tokens(lexer, pos):
    previous_token = None
    next_token = None
    
    # Ищем предыдущий токен
    lexer.backup()
    while lexer.pos > 0:
        token = lexer.token()
        if token is None:
            break
        if token.lexpos < pos:
            previous_token = token
        else:
            break
    lexer.forward()
    
    # Ищем следующий токен
    while True:
        token = lexer.token()
        if token is None or token.lexpos > pos:
            break
        next_token = token
    
    return previous_token, next_token

# обрабатывает синтаксические ошибки. Она выводит сообщение об ошибке с номером строки, позицией и неожиданным токеном. 
# Затем использует функцию get_previous_and_next_tokens для поиска и вывода предыдущих и следующих токенов. 
# Пытается разобрать весь ввод и выводит дерево разбора, если успешно, или сообщение об ошибке, если нет.

def error_handler(error):
    print(f"Syntax error at line {error.lineno}, position {error.lexpos}:")
    print(f"Unexpected token: {error.value}")
    
    # Получаем предыдущий и следующий токены
    lexer = error.lexer
    previous_token, next_token = get_previous_and_next_tokens(lexer, error.lexpos)
    if previous_token:
        print(f"Previous token: {previous_token.type} ({previous_token.value})")
    if next_token:
        print(f"Next token: {next_token.type} ({next_token.value})")
    
    # Лексический анализ предложения
    try:
        parse_tree = parser.parse(error.lexer.lexdata)
        print("Parsed tree:", parse_tree)
    except Exception as e:
        print("Failed to parse the entire input due to previous errors.")
    
    # Предположим, что мы знаем ожидаемые типы токенов на этом месте
    expected_token_types = ['NOUN', 'VERB', 'ADVB']
    
    for token_type in expected_token_types:
        suggestion = recommend_correction(error.value, token_type)
        print(suggestion)

# Устанавливаем обработчик ошибок в PLY
parser.error = error_handler

# Пример использования
try:
    text = "диспетчер формируета рейсы."
    result = parser.parse(text)
    print(result)
except Exception as e:
    print(e)
