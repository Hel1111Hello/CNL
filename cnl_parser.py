################################### yacc ######################################################
import ply.lex as lex
import ply.yacc as yacc
import cnl_lexer as tokrules
from cnl_lexer import tokens


'''
s → (sl)
sl → sentence | sl sentence
sentence →  aim_condition sub_pred DOT
aim_condition → ε | aim_condition_prep sub_pred COMMA
aim_condition_prep → IF | FOR 
sub_pred → sub pred

sub → name  
name → prop_noun aggregate_material_loc_part_except
prop_noun → prop NOUN prop

op → AND | OR | DASH    # DASH - дефис '-' 
prop → ε | ADJF prop | LPAREN prop op prop RPAREN prop

aggregate_material_loc_part_except → aggregate material loc part except
prop_gent → ε | ADJF_gent prop_gent
prop_ablt → ε | ADJF_ablt prop_ablt | LCURLYBRACE prop_ablt op prop_ablt RCURLYBRACE prop_ablt

aggregate → ε | prop_gent Gent_noun_prtf__plur aggregate| LSBRACKET aggregate op aggregate RSBRACKET aggregate
material → ε | FROM prop Gent_noun_prtf__plur
loc → ε | LOC_PREP prop_name aggregate
part → ε | prep_part prop_name part
prop_name → prop_noun | prop_gent Gent_noun_prtf__plur | prop_gent Loct | prop_ablt Ablt prop_ablt   
prep_part → WITH | WITHOUT
except → ε | EXCEPT aggregate 

pred → ε | quality feature obj_instr
quality → ε | ADVB
feature → act | relation
act →  VERB | INFN | PRTS | PRCL # PRTS краткое причастие - выточена. PRCL частица - есть 
relation → COMP

obj_instr → obj instr
obj → ε | obj_loc obj_name | obj_name 
obj_loc → LOC_PREP | FROM  
obj_name → name | prop_gent Gent_noun_prtf__plur aggregate_material_loc_part
instr → ε | Ablt prop_ablt 
'''

def p_s(p):
    's : sl'
    p[0] = '(' + str1(p[1]) + ')'


def p_sl(p):
    'sl : sentence'
    p[0] = str1(p[1])


def p_empty(p):
    'empty :'
    pass


def p_sl_sent(p):
    'sl : sl sentence'
    p[0] = str1(p[1]) + ' ' + str1(p[2])


def p_sentence(p):
    'sentence : aim_condition sub_pred DOT'
    p[0] = '(:sentence  ' + str1(p[1]) + ' ' + str1(p[2]) + ')'


def p_aim_condition_empty(p):
    'aim_condition : empty'
    p[0] = '(:aim_condition :nil)'


def p_aim_condition(p):
    'aim_condition : aim_condition_prep sub_pred COMMA'
    p[0] = '(:aim_condition ' + str1(p[1]) + str1(p[2]) + ')'


def p_aim_condition_prep_if(p):
    'aim_condition_prep : IF'
    p[0] = '(:if ' + str1(p[1]) + ')'


def p_aim_condition_prep_for(p):
    'aim_condition_prep : FOR'
    p[0] = '(:aim ' + str1(p[1]) + ')'


def p_sub_pred(p):
    'sub_pred : sub pred'
    p[0] = '(:sub_pred  ' + str1(p[1]) + ' ' + str1(p[2]) + ')'


##############################################

def p_sub(p):
    'sub : name'
    p[0] = '(:sub ' + str1(p[1]) + ')'


def p_name(p):
    'name : prop_noun aggregate_material_loc_part_except'
    p[0] = str1(p[1]) + ' ' + str1(p[2])


def p_prop_noun(p):
    'prop_noun : prop NOUN prop'
    p[0] = '(:prop_noun ' + str1(p[1]) + ' ' + str1(p[2]) + ' ' + str1(p[3]) + ')'


def p_op_and(p):
    'op : AND'
    p[0] = str1(p[1])


def p_op_or(p):
    'op : OR'
    p[0] = str1(p[1])


def p_op_dash(p):
    'op : DASH'
    p[0] = str1(p[1])


def p_prop__empty(p):
    'prop : empty'
    p[0] = '(:prop :nil)'


def p_prop_1(p):
    'prop : ADJF prop'
    p[0] = '(:prop_list ' + str1(p[1]) + ' ' + str1(p[2]) + ')'


def p_prop_2(p):
    'prop : LPAREN prop op prop RPAREN prop'
    p[0] = '(' + str1(p[3]) + ' ' + str1(p[2]) + ' ' + str1(p[4]) + ' ' + str1(p[6]) + ')'


def p_aggregate_material_loc_part_except(p):
    'aggregate_material_loc_part_except : aggregate material loc part except'
    p[0] = str1(p[1]) + ' ' + str1(p[2]) + ' ' + str1(p[3]) + ' ' + str1(p[4]) + ' ' + str1(p[5])



def p_prop_gent_empty(p):
    'prop_gent : empty'
    p[0] = '(:prop_gent :nil)'


def p_prop_gent(p):
    'prop_gent : ADJF_gent prop_gent'
    p[0] = '(:prop_gent_list ' + str1(p[1]) + ' ' + str1(p[2]) + ')'


def p_prop_ablt_empty(p):
    'prop_ablt : empty'
    p[0] = '(:prop_ablt :nil)'


def p_prop_ablt_1(p):
    'prop_ablt : ADJF_ablt prop_ablt'
    p[0] = '(:prop_ablt_list ' + str1(p[1]) + ' ' + str1(p[2]) + ')'


def p_prop_ablt_2(p):
    'prop_ablt : LCURLYBRACE prop_ablt op prop_ablt RCURLYBRACE prop_ablt'
    p[0] = '(' + str1(p[3]) + ' ' + str1(p[2]) + ' ' + str1(p[4]) + ' ' + str1(p[6]) + ')'


def p_aggregate_empty(p):
    'aggregate : empty'
    p[0] = '(:aggregate :nil)'


def p_aggr_1(p):
    'aggregate : prop_gent Gent_noun_prtf__plur aggregate'
    p[0] = '(:aggregate_list ' + str1(p[1]) + ' ' + str1(p[2]) + ' ' + str1(p[3]) +')'


def p_aggr_2(p):
    'aggregate : LSBRACKET aggregate op aggregate RSBRACKET aggregate'
    p[0] = '(' + str1(p[3]) + ' ' + str1(p[2]) + ' ' + str1(p[4]) + ' ' + str1(p[6]) + ')'


def p_material_empty(p):
    'material : empty'
    p[0] = '(:material :nil)'


def p_material(p):
    'material : FROM prop_gent Gent_noun_prtf__plur'
    p[0] = '(:material ' + str1(p[1]) + ' ' + str1(p[2]) + ' ' + str1(p[3]) + ')'


def p_loc_empty(p):
    'loc : empty'
    p[0] = '(:loc :nil)'


def p_loc(p):
    'loc : LOC_PREP prop_name aggregate'
    p[0] = '(:loc ' + str1(p[1]) + ' ' + str1(p[2]) + ' ' + str1(p[3]) + ')'


def p_part_empty(p):
    'part : empty'
    p[0] = '(:part :nil)'


def p_part(p):
    'part : prep_part prop_name part'
    p[0] = '(:part_list ' + str1(p[1]) + ' ' + str1(p[2]) + ' ' + str1(p[3]) + ')'


def p_prop_name(p):
    'prop_name : prop_noun'
    p[0] = str1(p[1])


def p_prop_name_1(p):
    'prop_name : prop_gent Gent_noun_prtf__plur'
    p[0] = '(:prop_name ' + str1(p[1]) + ' ' + str1(p[2]) + ')'

def p_prop_name_2(p):
    'prop_name : prop_gent Loct'
    p[0] = '(:prop_name ' + str1(p[1]) + ' ' + str1(p[2]) + ')'


def p_prop_name_3(p):
    'prop_name : prop_ablt Ablt prop_ablt'
    p[0] = '(:prop_name ' + str1(p[1]) + ' ' + str1(p[2]) + ' ' + str1(p[3]) + ')'


def p_prep_part_with(p):
    'prep_part : WITH'
    p[0] = str1(p[1])


def p_prep_part_without(p):
    'prep_part : WITHOUT'
    p[0] = str1(p[1])


def p_except(p):
    'except : empty'
    p[0] = '(:except :nil)'


def p_except_1(p):
    'except : EXCEPT aggregate'
    p[0] = '(:except ' + str1(p[1]) + ' ' + str1(p[2]) + ')'


#########################
def p_pred_empty(p):
    'pred : empty'
    p[0] = '(:pred :nil)'


def p_pred(p):
    'pred : quality feature obj_instr'
    p[0] = '(:pred ' + str1(p[1]) + ' ' + str1(p[2]) + ' ' + str1(p[3]) + ')'


def p_quality__empty(p):
    'quality : empty'
    p[0] = '(:quality :nil)'


def p_quality(p):
    'quality : ADVB'
    p[0] = '(:quality ' + str1(p[1]) + ')'


def p_feature_act(p):
    'feature : act'
    p[0] = '(:act ' + str1(p[1]) + ')'


def p_feature_relation(p):
    'feature : relation'
    p[0] = '(:relation ' + str1(p[1]) + ')'


def p_act_verb(p):
    'act : VERB'
    p[0] = '(:act_VERB ' + str1(p[1]) + ')'


def p_act_infn(p):
    'act : INFN'
    p[0] = '(:act_INFN ' + str1(p[1]) + ')'


def p_act_prts(p):
    'act : PRTS'
    p[0] = '(:act_PRTS ' + str1(p[1]) + ')'


def p_act_prcl(p):
    'act : PRCL'
    p[0] = '(:act_PRCL ' + str1(p[1]) + ')'


def p_relation_comp(p):
    'relation : COMP'
    p[0] = '(:relation ' + str1(p[1]) + ')'


####################################################
def p_obj_instr(p):
    'obj_instr : obj instr'
    p[0] = '(:obj_instr ' + str1(p[1]) + ' ' + str1(p[2]) + ')'


def p_obj_empty(p):
    'obj : empty'
    p[0] = '(:obj :nil)'


def p_obj(p):
    'obj : obj_loc obj_name'
    p[0] = '(:obj ' + str1(p[1]) + ' ' + str1(p[2]) + ')'

def p_obj_1(p):
    'obj : obj_name'
    p[0] = '(:obj ' + str1(p[1]) + ')'


def p_obj_loc(p):
    'obj_loc : LOC_PREP'
    p[0] = '(:obj_loc ' + str1(p[1]) +')'


def p_obj_loc_1(p):
    'obj_loc : FROM'
    p[0] = '(:obj_loc ' + str1(p[1]) +')'


def p_obj_name(p):
    'obj_name : name'
    p[0] = '(:obj_name ' + str1(p[1]) + ')'


def p_obj_name_1(p):
    'obj_name : prop_gent Gent_noun_prtf__plur aggregate_material_loc_part_except'
    p[0] = '(:obj_name ' + str1(p[1]) + ' ' + str1(p[2]) + ' ' + str1(p[3]) + ')'


def p_instr_empty(p):
    'instr : empty'
    p[0] = '(:instr :nil)'


def p_instr(p):
    'instr : Ablt prop_ablt'
    p[0] = '(:instr ' + str1(p[1]) + ' ' + str1(p[2]) + ')'

#############################################################
def str1(s):
    """
    Вставка двоеточия перед терминами.
    """
    if s[0] != '(' and s[0] != ':':
        s = ':' + str(s)

    return str(s)


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")
    print(p)


# Build lexer and parser
lexer = lex.lex(module=tokrules)
parser = yacc.yacc(debug=True)


