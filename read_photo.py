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
            id = id + 1
    return slides


def combine_vertical_photos(photo1, photo2):
    return (photo1[0], photo2[0]), photo1[2].union(photo2[2])


def get_slides(infile):
    fotos = read_photo(infile)

    # Filtrar les fotos verticals
    fotos_verticals = fotos.copy()
    fotos_verticals = [x for x in fotos if x[1] == "V"]

    # Ordernar les fotos verticals segons el núm tags que tenen
    fotos_verticals = sorted(fotos_verticals, key=lambda x: x[3])

    # Si hi ha un núm senar de fotos verticals, eliminar la menys valuosa
    if len(fotos_verticals) % 2 > 0:
        fotos_verticals.remove(fotos_verticals[0])

    # Combinar fotos verticals de 2 en 2 fent que la que té menys tags vagi amb la que en té més
    fotos_vert_comb = {}
    while len(fotos_verticals) > 0:
        key, value = combine_vertical_photos(fotos_verticals[0], fotos_verticals[len(fotos_verticals) - 1])
        fotos_vert_comb[key] = value
        fotos_verticals.remove(fotos_verticals[0])
        fotos_verticals.remove(fotos_verticals[len(fotos_verticals) - 1])

    # Extreure les fotos horitzontals
    fotos_horitzontals = fotos.copy()
    fotos_horitzontals = [x for x in fotos if x[1] == "H"]

    fotos_horiz = {}
    for x in fotos_horitzontals:
        fotos_horiz[x[0]] = x[2]

    # Juntar totes les fotos en array de slides
    slides = {**fotos_horiz, **fotos_vert_comb}
    return (slides)


def compare(set1, set2):
    uniquePhoto1 = len(set1.difference(set2))
    uniquePhoto2 = len(set2.difference(set1))
    intersect = len(set1.intersection(set2))
    return min([uniquePhoto1, uniquePhoto2, intersect])

def build_matrix(images):
    matrix = {}
    keysImages = images.keys()
    for image1 in keysImages:
        row_list = []
        for image2 in keysImages:
            if image1 != image2:
                row_list.append((image2, compare(images[image1], images[image2])))
        matrix[image1] = sorted(row_list, key= lambda x: x[1], reverse=True)
    return matrix

def get_wierd_photo(m):
    max_z = 0
    max_z_id = ""
    for idPhoto, value in m.items():
        numZeros = len([x[1] for x in value if x[1] == 0])
        if numZeros > max_z:
            max_z = numZeros
            max_z_id = idPhoto
    return max_z_id



photos =  get_slides(infile)

m = build_matrix(photos)
Finished = False
first_id = get_wierd_photo(m)
slideshow = [first_id]


while not Finished:
    last_id = slideshow[-1]
    IDlst = m[last_id]
    for id in IDlst:
        id = id[0]
        if id in m and len(m)>1:
            slideshow.append(id)
            del m[last_id]
            break
        else:
            Finished = True

with open("output.txt", "w") as f:
    numberSlides = len(slideshow)
    f.write("%s\n" % numberSlides)
    for photoid in slideshow:
        if type(photoid) == tuple:
            f.write("%s %s\n"% photoid)
        else:
            f.write("%s\n" % photoid)
