def read_photo(infile):
    slides = []
    with open(infile) as f:
        num_slides = f.readline().strip()
        for line in f:
            line = line.rstrip().split()
            slideType = line[0]
            setTags = set(line[2:])
            slides.append((slideType, setTags))
    return slides