'''
Created on Aug 12, 2017


Static functions for fst objects

@author: Gabor Pinter
'''
import pywrapfst
import os



def initFst(fst, add_eps=True, eps_label="<eps>", is_initial_final=False):
    '''
    fst: vector Fst object
    '''
    q0 = fst.add_state()
    fst.set_start(q0)
    if is_initial_final:
        fst.set_final(q0)
    fst.set_input_symbols(pywrapfst.SymbolTable())
    fst.set_output_symbols(pywrapfst.SymbolTable())
    if add_eps:
        for sym_tbl in [ fst.mutable_input_symbols(), fst.mutable_output_symbols()]:
            sym_tbl.add_symbol(eps_label)

def addArcFlower(fst, q0, q1, ilabels, olabels=None, weight=None):
    '''
    Adding
    q0 arc(s) origin
    q1 arc(s) target
    '''
    if not isinstance(ilabels, list):
        raise ValueError("input label argument must be a list")
    if olabels is None:
        olabels = ilabels
    if not isinstance(olabels, list):
        raise ValueError("Output label argument must be a list")

    isym_tbl = fst.mutable_input_symbols()
    osym_tbl = fst.mutable_output_symbols()

    for label in ilabels + olabels:
        isym = isym_tbl.add_symbol(label)
        osym = osym_tbl.add_symbol(label)

    if weight is None:
        weight = pywrapfst.Weight.One(fst.weight_type())

    for i in range(len(ilabels)):
        isym = isym_tbl.add_symbol(ilabels[i])
        osym = osym_tbl.add_symbol(olabels[i])
        fst.add_arc(q0,
                    pywrapfst.Arc(isym, osym, weight, q1))


def addArcLinear(fst, start_state, labels, olabels=None, is_loop=False):
    if not isinstance(labels, list):
        raise ValueError("Label argument must be a list")

    isym_tbl = fst.mutable_input_symbols()
    osym_tbl = fst.mutable_output_symbols()

    if olabels is None:
        sym_len = len(labels)
        isyms = [isym_tbl.add_symbol(lab) for lab in labels]
        osyms = [osym_tbl.add_symbol(lab) for lab in labels]
    else:
        sym_len = max(len(labels), len(olabels))
        isyms = [isym_tbl.add_symbol(lab) for lab in labels]   + [0]*(sym_len-len(labels))
        osyms = [osym_tbl.add_symbol(lab) for lab in olabels]  + [0]*(sym_len-len(olabels))

    q0 = start_state
    for i in range(sym_len):
        if is_loop and i == sym_len-1:
            q1 = start_state
        else:
            q1 = fst.add_state()
        fst.add_arc(q0,
                    pywrapfst.Arc(isyms[i], osyms[i], pywrapfst.Weight.One(fst.weight_type()), q1))
        q0 = q1
    return q1

def writeFst(fst, path):
    '''
    Writes FST into path.
    Writes symbol tables as well.
    Writes
    '''
    if not path.endswith(".fst"):
        path += ".fst"
    path = os.path.abspath(path)
    print "Write", os.path.abspath(path)
    isym_tbl_path = os.path.splitext(path)[0] + ".isym"
    fst.input_symbols().write(isym_tbl_path)
    osym_tbl_path = os.path.splitext(path)[0] + ".osym"
    fst.input_symbols().write(osym_tbl_path)
    fst.write(path)
    fst.draw(path + ".dot")


def genStrFst(ilabels, olabels=None):
    if olabels is None:
        olabels = ilabels
    fst = pywrapfst.Fst()
    initFst(fst)
    addArcLinear(fst, 0, ilabels, olabels, is_loop=False)
    return fst



#     fst = genStrFst([c for c in "abc"],
#                     [c for c in "abcde"],
#               )
#     writeFst(fst, "/home/kinoko/Dropbox/workspace/FstProsody/build/str")






