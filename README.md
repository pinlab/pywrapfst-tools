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

# iterating over arcs outgoing from a state:
for arc in fst.num_arcs( <state> )
    print arc.ilabel, arc.olabel, arc.nextstate
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



