from PIL import Image
import os
import operator

def start():
    directory = "C:/Users/astro/Pictures/world_flags/discrepancy/"
    paths = get_image_paths(directory)
    
    breakdowns = {path:breakdown_image(path) for path in paths}
    predominants = get_predominant_colors(breakdowns)
    #print(predominants)

    most_predominant = [[path,t[0],t[1]] for path, t in predominants.items()]
    most_predominant = sorted(most_predominant,key=lambda x: x[2], reverse=True)
    print('most_predominant',most_predominant)


def get_image_paths(directory):
    '''
    gets all image files
    '''
    return [os.path.join(directory,f) for f in os.listdir(directory) if is_image(f)]

def is_image(filename):
    '''
    logic to determine if image
    TODO: add more
    '''
    return filename.lower().endswith(".jpg") or filename.lower().endswith(".png")


def breakdown_image(path):
    '''
    get color breakdown for image
    '''
    im = Image.open(path) # Can be many different formats.
    pix = im.load()
    w,h = im.size
    total_pixels = w*h
    colors = {}
    for x in range(w):
        for y in range(h):
            value = pix[x,y]
            colors[value] = colors[value] + 1 if value in colors else 0

    normal = {k: v/total_pixels for k,v in colors.items()}
    return normal

def max_by_value(dictionary):
    '''
    gets max tuple in dictionary by value
    '''
    return max(dictionary.items(), key=operator.itemgetter(1))


def get_predominant_colors(breakdowns):
    '''
    gets theh predmoninant color for each item in breakdowns
    '''
    return {path:max_by_value(breakdown) for path,breakdown in breakdowns.items()}


if __name__ == "__main__": start()