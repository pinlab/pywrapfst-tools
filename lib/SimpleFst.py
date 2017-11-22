'''
Created on Nov 22, 2017

@author: Gabor Pinter
'''
import pywrapfst
import os
import logging

SYM_EPS=0
LAB_EPS="<eps>"

LOG = logging.getLogger()

class SimpleFst(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.fst = pywrapfst.Fst()
        self.STATE_START = self.fst.add_state()
        self.fst.set_start(self.STATE_START)
       
        self.fst.set_input_symbols(pywrapfst.SymbolTable())
        self.fst.set_output_symbols(pywrapfst.SymbolTable())
        self.fst.mutable_input_symbols().add_symbol(LAB_EPS, key=SYM_EPS)
        self.fst.mutable_output_symbols().add_symbol(LAB_EPS, key=SYM_EPS)
        
    
    def _label_to_sym(self, label, sym_tbl):
        if isinstance(label, basestring):
            syms = [sym_tbl.add_symbol(x) for x in label]
        elif isinstance(label, list):
            if all([isinstance(i, int)  for i in label]):
                syms = label[:]
            elif all([isinstance(i, basestring)  for i in label]):
                syms = [sym_tbl.add_symbol(x) for x in label]
                print syms
        else:
            raise ValueError("Unkown argumen type '%s'" % type(label))
        return syms
    
    
    def addFlower(self, ilabels, olabels=None, state=None):
        self.addArc(ilabels, olabels, start_state=state, is_loop=True)
   
    def addArc(self, ilabels, olabels=None, start_state=None, is_loop=False):
        '''
        
        '''
        isyms = self._label_to_sym(ilabels, self.fst.mutable_input_symbols())
        if olabels is None:
#             osyms = isyms[:] # create copy
            osyms = self._label_to_sym(ilabels, self.fst.mutable_output_symbols())
        else:
            osyms = self._label_to_sym(olabels, self.fst.mutable_output_symbols())
       
        maxix = max(len(isyms), len(osyms))
        if len(isyms) != len(osyms):
            isyms += [0] * (maxix - len(isyms))
            osyms += [0] * (maxix - len(osyms))
        
        if start_state is None:
            start_state = self.STATE_START
        
        q0 = start_state
        for i in range(maxix):
            if is_loop and i == maxix-1:
                q1 = start_state
            else:
                q1 = self.fst.add_state()
            self.fst.add_arc(q0,
                        pywrapfst.Arc(isyms[i], osyms[i], pywrapfst.Weight.One(self.fst.weight_type()), q1))
            q0 = q1
        return q1
       
    def write(self, fpath, draw=True):
        ''' Write FST 
        '''
        basename = os.path.splitext(fpath)[0]
        dot_fpath = "%s.dot" % basename  
        LOG.info("Writing '%s'" % dot_fpath)
        self.fst.write(fpath)
        self.fst.draw(dot_fpath)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%m-%d %H:%M'
                    )    
    
    fst = SimpleFst()
#     fst.addFlower(fst.STATE_START, ["a", "b", "c"], ["x", "y", "z", "k"])
    fst.addFlower(["Onset", "Nucleus"])
    fst.write("simple.fst")

