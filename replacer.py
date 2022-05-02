import csv


def make_final_dataset():
    flatslist = [] # making list of flats from a csv file
    with open('flats.csv', newline='\n') as flats:
        flatsreader = csv.reader(flats, delimiter='\n', quotechar='|')

        for row in flatsreader:
            flatslist.append(row[0].split(','))
    print(flatslist)


    ratingdict = {}
    with open('rating.csv', newline='\n') as rating:
        ratingreader = csv.reader(rating, delimiter='\n', quotechar='|')
        for row in ratingreader:
            ratingdict.update({row[0].split(',')[0]: row[0].split(',')[1]})

    print(ratingdict)


    with open('final_dataset.csv', 'a') as dataset:
        for elem in flatslist:
            if elem[3] in ratingdict.keys():
                elem[3] = ratingdict[elem[3]]
            else: # to skip broken values
                continue
            dataset.write(f"{','.join(elem)}\n")


    print(flatslist)