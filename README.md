# Pywrapfst Tools

The goal of this project is to collect tools to work easily with [OpenFst](www.openfst.org)'s Python extension/wrapper: [PyWrapFst](http://www.openfst.org/twiki/bin/view/FST/PythonExtension).

## Install ##
Add flag ```--enable-python``` when configuring OpenFst, before ```make```ing it.
```bash
./configure  --enable-python
```

## Import ##
```Python
import pywrapfst
```
## Usagage ##

### Create/Read FST ###
```Python
fst = pywrapfst.Fst()
fst = pywrapfst.Fst.read( <path> )
```

### States ###
```Python
q0 = fst.add_state()
cnt = fst.num_states()

```

### Arcs ###
```Python
q1 = arc.nextstate
i  = arc.ilabel
o  = arc.olabel
w  = arc.weight

# creating an arc to state q1
arc = pywrapfst.Arc(isym, osym, pywrapfst.Weight.One(fst.weight_type()), q1))

# adding an arc to state q0 in fst (which is Fst vector object)
fst.add_arc(q0, arc)

# iterating over arcs outgoing from state q0:
for arc in fst.num_arcs( q0 )
    print arc.ilabel, arc.olabel, arc.nextstate
    
# sort arcs
fst.arcsort(sort_type="ilabel")
fst.arcsort(sort_type="olabel") 
```

### Symbols ###
```Python
sym_tbl = pywrapfst.SymbolTable()
sym_tbl = fst.input_symbols()
sym_tbl = fst.mutable_input_symbols()

# add label
# returns integer (sym)
# if label is present: does not create new symbol for label
sym_tbl.add_symbol(label)

# find sym for label or vice-versa
# raises error if missing
sym   = sym_tbl.find(label)
label = sym_tbl.find(sym)

fst.set_input_symbols(sym_tbl)
fst.set_output_symbols(sym_tbl)
```

### Operations ###

```Python
# composition
pywrapfst.compose(fst1, fst2)

# merge symbl tables
left_sym_tbl = str_fst.mutable_output_symbols()
right_sym_tbl = self.fst.mutable_input_symbols()
left_sym_tbl.add_table(right_sym_tbl)
right_sym_tbl.add_table(left_sym_tbl)
str_fst.relabel_tables(new_osymbols=self.fst.input_symbols())    

# remove epsilons
```

