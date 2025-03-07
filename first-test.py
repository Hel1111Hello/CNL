import ply.lex as lex
import ply.yacc as yacc
from pymorphy3 import MorphAnalyzer

# Инициализация морфологического анализатора
morph = MorphAnalyzer()

# Лексические правила (токены)
tokens = (
    'DOT',  # точка
    'COMMA', # запятая
    'NOUN', # имя существительное   хомяк
    'VERB', # глагол (личная форма) говорю, говорит, говорил
    'ADVB', # наречие   круто
    'ADJF', # имя прилагательное (полное)   хороший
    'INFN', # инфинитив
    'PRTS', # причастие (краткое)   прочитана
    'COMP', # компаратив    лучше, получше, выше
    'PRCL', # частица   это, бы, же, лишь

    'Gent_noun_prtf__plur',
    'Ablt',
    'Loct',
    'ADJF_gent',
    'ADJF_ablt',

    'WITH', # предлог 'c', 'со'
    'WITHOUT', # предлог 'без'
    'FROM',  # предлог 'из'
    'IF',   # предлог 'если'
    'FOR',   # предлог 'для', 'чтобы'
    'LOC_PREP',   # предлоги 'на', 'в', 'над', 'под', 'за', 'к', 'от'
    'AND',   # и
    'OR',   # или
    'DASH', # дефис '-'
    'EXCEPT',   # кроме

    'LPAREN',
    'RPAREN',
)

# Регулярные выражения для токенов
def t_dot(t):
    r'\.'
    t.type = 'DOT'
    return t

def t_comma(t):
    r','
    t.type = 'COMMA'
    return t

def t_lparen(t):
    r'\('
    t.type = 'LPAREN'
    return t

def t_rparen(t):
    r'\)'
    t.type = 'RPAREN'
    return t

# Лексический анализатор для слов
def t_word(t):
    r'[а-яА-Я]+'
    parses = morph.parse(t.value)
    if not parses:
        return t  # Если не удалось разобрать слово, оставляем как есть

    p = parses[0]
    tag = p.tag

    if tag.POS == 'NOUN':
        if tag.case == 'gent':
            t.type = 'Gent_noun_prtf__plur'
        elif tag.case == 'loct':
            t.type = 'Loct'
        elif tag.case == 'ablt':
            t.type = 'Ablt'
        else:
            t.type = 'NOUN'
    elif tag.POS == 'ADJF':
        if tag.case == 'gent':
            t.type = 'ADJF_gent'
        elif tag.case == 'ablt':
            t.type = 'ADJF_ablt'
        else:
            t.type = 'ADJF'
    elif tag.POS == 'VERB':
        t.type = 'VERB'
    elif tag.POS == 'ADVB':
        t.type = 'ADVB'
    elif tag.POS == 'INFN':
        t.type = 'INFN'
    elif tag.POS == 'PRTS':
        t.type = 'PRTS'
    elif tag.POS == 'COMP':
        t.type = 'COMP'
    elif tag.POS == 'PRCL':
        t.type = 'PRCL'

    return t

# Игнорирование пробелов и табуляций
t_ignore = ' \t\n'

# Обработка ошибок лексического анализатора
def t_error(t):
    print(f"Illegal character '{t.value[0]}' on line {t.lineno}")
    t.lexer.skip(1)

# Создаем лексический анализатор
lexer = lex.lex()

# Грамматические правила (синтаксический анализатор)
def p_expression(p):
    '''expression : sentence DOT'''
    p[0] = p[1]

def p_sentence(p):
    '''sentence : subject predicate'''
    p[0] = f"Subject: {p[1]}, Predicate: {p[2]}"

def p_subject(p):
    '''subject : NOUN
               | Loct
               | Ablt
               | Gent_noun_prtf__plur'''
    p[0] = p[1]

def p_predicate(p):
    '''predicate : VERB object'''
    p[0] = f"Verb: {p[1]}, Object: {p[2]}"

def p_object(p):
    '''object : NOUN
              | Loct
              | Ablt
              | Gent_noun_prtf__plur'''
    p[0] = p[1]

# Обработка ошибок синтаксического анализатора
def p_error(p):
    if p is not None:
        print(f"Syntax error at token '{p.value}' on line {p.lineno}")
        recommend_correction(p)
    else:
        print("Unexpected end of input")

def recommend_correction(p):
    # Простая рекомендация для исправления ошибок
    suggestions = []
    parses = morph.parse(p.value)

    if not parses:
        print(f"Could not find suitable suggestions for '{p.value}'.")
        return

    for parse in parses:
        tag = parse.tag
        if p.type == 'NOUN':
            if tag.POS == 'NOUN':
                suggestions.append(parse.word)
        elif p.type == 'VERB':
            if tag.POS == 'VERB':
                suggestions.append(parse.normal_form + ' (verb)')
        elif p.type == 'ADVB':
            if tag.POS == 'ADVB':
                suggestions.append(parse.normal_form + ' (adverb)')
        elif p.type == 'ADJF':
            if tag.POS == 'ADJF':
                suggestions.append(parse.normal_form + ' (adjective)')
        elif p.type == 'INFN':
            if tag.POS == 'INFN':
                suggestions.append(parse.word)
        elif p.type == 'PRTS':
            if tag.POS == 'PRTS':
                suggestions.append(parse.word)
        elif p.type == 'COMP':
            if tag.POS == 'COMP':
                suggestions.append(parse.normal_form + ' (comparative)')
        elif p.type == 'PRCL':
            if tag.POS == 'PRCL':
                suggestions.append(parse.word)

    if suggestions:
        print(f"Did you mean: {', '.join(suggestions)}?")
    else:
        print(f"No suitable suggestions for '{p.value}'.")

# Создаем синтаксический анализатор
parser = yacc.yacc()

# Пример использования
try:
    text = "хомяк ест зерно."
    lexer.input(text)
    result = parser.parse(text, lexer=lexer)
    print(result)
except Exception as e:
    print(e)