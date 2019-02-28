import sys
infile = sys.argv[1]

def read_photo(infile):
    slides = []
    with open(infile) as f:
        num_slides = f.readline().strip()
        id = 0
        for line in f:
            line = line.rstrip().split()
            slideType = line[0]
            setTags = set(line[2:])
            slides.append((id, slideType, setTags, len(setTags)))
            id = id+1
    return slides

def get_slides(infile):
    fotos = read_photo(infile)

    # Filtrar les fotos verticals
    fotos_verticals = fotos.copy()
    filter(lambda x: x[1] == 'V', fotos_verticals)
    fotos_verticals = [x for x in fotos if x[1] == "V"]

    # Ordernar les fotos verticals segons el núm tags que tenen
    fotos_verticals = sorted(fotos_verticals, key=lambda x:x[3] )

    # Si hi ha un núm senar de fotos verticals, eliminar la menys valuosa
    if len(fotos_verticals) % 2 > 0:
        fotos_verticals.remove(fotos_verticals[0])

    # Combinar fotos verticals de 2 en 2 fent que la que té menys tags vagi amb la que en té més
    fotos_vert_comb = []
    while len(fotos_verticals) > 0:
        fotos_vert_comb.append((fotos_verticals[0], fotos_verticals[len(fotos_verticals)-1]))
        fotos_verticals.remove(fotos_verticals[0])
        fotos_verticals.remove(fotos_verticals[len(fotos_verticals)-1])

    # Extreure les fotos horitzontals
    fotos_horitzontals = fotos.copy()
    filter(lambda x: x[1] == 'H', fotos_horitzontals)
    fotos_horitzontals = [x for x in fotos if x[1] == "H"]

    # Juntar totes les fotos en array de slides
    slides = fotos_horitzontals + fotos_vert_comb
    return(slides)

get_slides(infile)
