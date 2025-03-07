# -*- coding: utf-8 -*-
from rdf.rdf import Rdf
rdf = Rdf()
from dichotomy.dichotomy import Dichotomy
dchtm = Dichotomy()
from common.common import opposites, Common_data_manager
dm = Common_data_manager()
from cnl.cnl_parser import parser
import os
dir = os.path.abspath(os.curdir)
from rdflib import Graph
from triad.triad import Triad
from dtopology.dtopologyrwn import DTopologyRWN
trwn = DTopologyRWN()
from ok.sample import Sample


def main_ok():
    """
    Извлечение ДД из таксономии ОК с дихотомией.
    """
    sample = Sample(dir + "\\testdriver\\ok\\script74_den.txt")

    sample.linespreprocess()
    sample.brackets()
    print(sample.lines)
    pass


def main_prototype_0():
    """
    Сквозная процедура:
        компиляция CNL ->
        дихотомия ->
        д-определение сформированных дихотомие противоположностей триадным сопряжением.
    """
    # Stub - исходный текст на CNL.
    # Компиляция CNL -> rdf_строки - предложения (признаки).
    list=parser.parse('''без отверстий.  
    с отверстиями круглыми. 
    с отверстиями некруглыми.
    с отверстиями круглыми и некруглыми.''')

    # rdf_строки (признаки) -> python_list формат признаков.
    feature_list = []
    for i in range(0,len(list)) :
        feature_list.append(rdf.rdfstr2list(list[i]))
        #print(list[i])

    # Загрузка ДД и таблиц opposites, sl (sl не используется дихотомией, применяется в dtopology)
    gdd = Graph()
    gdd.parse(dir + "\\main\\с_без.txt")

    # Stub opposites
    opposites['с'] = 'без'

    # Дихотомия.
    new_opposites = dchtm.dichotomy(feature_list)
    print(new_opposites)

    # Д-определения противоположностей триаднымми сопряжениями.
    g = Graph()
    for i in range(0, len(new_opposites)):
        trd = Triad('', '', '', '', '')
        sub_pos = new_opposites[i][0]
        sub_neg = new_opposites[i][1]
        conj_pos = new_opposites[i][2]
        conj_neg = new_opposites[i][3]
        path = new_opposites[i][4]
        triad = trd.opposites2triad(sub_pos, sub_neg, gdd)

        triad_conj = triad.conj_triad(path, conj_pos+'_'+conj_neg, conj_pos, conj_neg, g)

    # Вывод ДД.
    dm.write(g.serialize(format="turtle"), dir + "\\main\\дихотомия_0.txt")
    ####################################################


def main_manual_triad_creation():
    """
    Ручное конструирование триады.
    """
    # Ввод тестового ДД.
    trd = Triad('', '', '', '', '')

    gdd = Graph()
    gdd.parse(dir + "\\testdriver\\triad\\Hegel.txt")

    triad = trd.opposites2triad('бытие', 'ничто',gdd)

    #g = Graph()
    #triad_conj = triad.conj_triad('части', 'с_без', 'с', 'без', g)
    triad_conj = triad.conj_triad('части', 'с_без', 'с', 'без', gdd)

    #write(g.serialize(format="turtle"), dir + "\\main\\с_без.txt")
    dm.write(gdd.serialize(format="turtle"), dir + "\\main\\с_без.txt")

#################################################

    gdd = Graph()
    gdd.parse(dir + "\\main\\conj_с_без.txt")
    triad_sub = trd.opposites2triad('с', 'без', gdd)

    g = Graph()
    triad_conj = triad_sub.conj_triad('отверстие', 'с_отверстиями_без_отверстий',
                                      'с_отверстиями', 'без_отверстий', g)

    dm.write(g.serialize(format="turtle"), dir + "\\main\\conj_с_без_отверстий.txt")


def test_0():
    """

    """
    # Stub - исходный текст на CNL.
    # Компиляция CNL -> rdf_строки - предложения (признаки).

    list = parser.parse('''
    пирог с_отверстиями.
    печенье без_отверстий. 
    сыр с_отверстиями.
    ''')

    # rdf_строки (признаки) -> python_list формат признаков.
    feature_list = []
    for i in range(0, len(list)):
        feature_list.append(rdf.rdfstr2list(list[i]))
        print(list[i])


    id_reper_0 = trwn.nch(trwn.title2id('пирог'), trwn.title2id('печенье'))
    #print(trwn.id2title(id_reper_0))
    id_reper_1 = trwn.nch(trwn.title2id('пирог'), trwn.title2id('сыр'))
    #print(trwn.id2title(id_reper_1))

    if trwn.nch(id_reper_0, id_reper_1) == id_reper_0:
        rez = 1
    if trwn.nch(id_reper_0, id_reper_1) == id_reper_1:
        rez = 0
    pass
