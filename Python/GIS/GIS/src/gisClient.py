from gis import *

def main():
    gsystem = Gis()
    gsystem.selectAllCities()
    gsystem.selectAllEdges()

    delimiter = '\n*************************************\n'

    #### EXPERIMENT 5 ####
    gsystem.selectAllCities()
    gsystem.selectAllEdges()

    # print TSP tour starting from Yakima, WA, with
    # exactly 4 cities on each line except possibly the
    # last line.
    gsystem.tour('Vincennes, IN')

    print delimiter    

    gsystem.selectEdges(505,1500)    

    gsystem.tour('Yakima, WA')
    """

    gsystem.selectAllCities()
    gsystem.selectAllEdges()
    gsystem.selectCities('state', 'NY')
    gsystem.selectEdges(20, 800)
    gsystem.tour('Rochester, NY')
    print delimiter

    gsystem.tour('Yakima, NY')
    """

main()