def read_slides(infile):
    slides = []
    with open(infile) as f:
        num_slides = f.readline().strip()
        for line in f:
            line = line.rstrip().split()
            slideType = line[0]
            numTags = line[1]
            setTags = set(line[2:])
            slides.append((slideType, numTags, setTags))
    return num_slides, slides
