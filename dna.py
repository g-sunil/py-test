expt = 'ATCG'


def main():
    vsp1, vsp2 = enter_species()
    print vsp1, vsp2


def validate_specie(spc):
    return all([(ch in spc) for ch in expt])


def enter_species():
    sp1 = specie1()
    sp2 = specie2()
    return (sp1, sp2)


def specie1():
    sp1 = raw_input('Enter the Specie1 \nConsisting of A T C G : ')
    while not validate_specie(sp1):
        specie1()
    return sp1


def specie2():
    sp2 = raw_input('Enter the Specie2 \nConsisting of A T C G : ')
    while not validate_specie(sp2):
        specie2()
    return sp2

if __name__ == '__main__':
    main()
