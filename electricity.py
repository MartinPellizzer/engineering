'''

electron orbits
---
number of electrons per shell: 2N^2
N: number of the orbit (shell)

valence electrons
---
electrons in outer shell
cannot be more than 8
when electron escape an atom -> become free electron
this is called ionization, and positive atoms called positive ion
if atom aquire electron, negative charge and called negative ion

'''

def atom_shell_electron_number_max_get(N):
    res = 2 * (N ** 2)
    return res

print('SHELL 1 ELECRON NUMBER:', atom_shell_electron_number_max_get(1))
print('SHELL 2 ELECRON NUMBER:', atom_shell_electron_number_max_get(2))
print('SHELL 3 ELECRON NUMBER:', atom_shell_electron_number_max_get(3))
print('SHELL 4 ELECRON NUMBER:', atom_shell_electron_number_max_get(4))
print('SHELL 5 ELECRON NUMBER:', atom_shell_electron_number_max_get(5))
