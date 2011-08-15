import networkx as nx
#from sets import Set
class City:
    def __init__(self,id,name,state,lat,lon,population):
        """create a new city"""
        self.id = id
        self.name  = name
        self.state = state
        self.population = population
        self.lat =  lat
        self.lon =  lon
        self.dist = []
        self.latitude = int(lat)/100.0
        self.longitude = int(lon)/100.0
class Gis:
    def __init__(self): #this is called when a new GIS object is created. It reads from gis.dat and sets everything ready to use.
        self.cities = [] #list of city objects
        self.cityGraph = nx.Graph()  #Graph
        self.selection = [] #current selection
        self.selected_edges = []
        self.mincutPhases = []

        #print "GIS object created! :) ";
        #print "Trying to read the file gis.dat"
        i = 0
        myfile = file("gis.dat");
        for line in myfile: # reading each line
            if line[0] is not '*':
                #if(i==1 or i%2 == 0):
                if not (line[0]>='0' and line[0]<='9'):
                    i = i+1
                    name = line.split(',')[0] #spliting the line at the 1st comma ,
                    state = line.split(',')[1].split("[")[0].split(' ')[1];
                    name = name+", "+state
                    latlong = line.split('[')[1].split(']')[0]
                    lat = latlong.split(',')[0]
                    lat = int(lat)
                    lon = latlong.split(',')[1]
                    lon = int(lon)
                    pop = int(line.split(']')[1].rstrip())
                    #create city object with currently gathered data.
                    c = City(i/2+1,name,state,lat,lon,pop)
                    self.cities.append(c)
                    self.cityGraph.add_node(c.name)
                    #if(i!=1):
                else:                #reading the distances
                    num = line.split(' ') # reading the next line containing distances
                    num[len(num)-1]= num[len(num)-1].rstrip() #removing \n from the last number read as string
                    for number in num: #converting string to int
                        if i is not 1:
                            self.cities[i-1].dist.append(int(number))
            else:
                pass
            #end of file reading process.
        for city in self.cities:
            city.dist.reverse()

        for l in range(0,len(self.cities)):
           for k in range(l+1,len(self.cities)):
              self.cityGraph.add_edge(self.cities[l].name,self.cities[k].name,distance=self.cities[k].dist[l])
       # for city in self.cities:
       #      city.dist = []
       #end of function init..


    #-------------------city functions-----------------------:
    def printPopulationDistr(self,step=None):

        if step is None:
            step = 20000
        self.selection.sort(key = lambda x:x.population, reverse = False)
        slots = {}
        if len(self.selection) > 0:
            i = 0
            slots[i] = 0
            upper = step
            for city in self.selection:
                if city.population <= upper :
                    slots[i]= slots[i]+1
                else :
                    i = i+1
                    upper = i*step
                    slots[i]= 1

            for i in range(0,len(slots)):
                print "["+str(i*step)+" , "+str((i+1)*step)+"] : "+str(slots[i])
        else:
            print "No cities found"

    def selectAllCities(self):
        #"selecting all cities!"
        self.selection = self.cities

    def unselectAllCities(self):
        # No city is selected
        self.selection = []

    def printFullSelection(self):
        for city in self.selection:
                print  city.name +' [' + str(city.lat) + ', ' + str(city.lon)+ '], ' +str(city.population)

    def printShortSelection(self):
        self.printCities()

    def printCities(self,attribute=None,choice=None,num=None):
        if attribute is None and choice is None: #this means it's a call to printCities() i.e. without any parameters
            self.selection.sort(key = lambda x:x.name, reverse = False)
            for city in self.selection:
                print city.name #+ ', ' + city.state
        else :
                if attribute is 'population':
                    self.selection.sort(key = lambda x:x.population, reverse = False)
                elif attribute is 'name':
                    self.selection.sort(key = lambda x:x.name, reverse = False)
                elif attribute is 'latitude':
                    self.selection.sort(key = lambda x:x.lat, reverse = False)
                elif attribute is 'longitude':
                    self.selection.sort(key = lambda x:x.lon, reverse = False)

                if choice is 'F': #printing full form
                    self.printFullSelection()
                elif choice is 'S': #printing short form
                    self.printShortSelection()



    def selectCities(self,attribute, lowerBound, upperBound = None):
        # attribute can be "name", "state","latitude", "longitude", and "population"
        current = []
        if attribute is "name":
           if upperBound is None:
               upperBound = 'z'
           #print "processing name"
           for city in self.selection:
               if city.name[0]>=lowerBound and city.name[0]<=upperBound:
                   current.append(city)
               self.selection = current

        elif attribute is "population":
            #print "processing population"
            if upperBound is None:
                upperBound = infinity
            for city in self.selection:
                if lowerBound<= city.population <=upperBound :
                        current.append(city)
            self.selection = current

        elif attribute is "latitude":
            #print "processing latitude"
            for city in self.selection:
                if city.latitude >= lowerBound and city.latitude <= upperBound :
                        current.append(city)
            self.selection = current

        elif attribute is "longitude":
            #print "processing longitude"
            for city in self.selection:
                if city.longitude >= lowerBound and city.longitude <= upperBound :
                        current.append(city)
            self.selection = current
        elif attribute is "state":
             for city in self.selection:
               if city.state == lowerBound:
                   current.append(city)
             self.selection = current

    #------------------end of city functions ------------------#

    #state functions:

    def printPopulatedStates(self, num):

        print str(num)+" most populated states"
        statepopulation = {}
        for city in self.selection:
            statepopulation[city.state] = 0

        for city in self.selection:
            statepopulation[city.state] = statepopulation[city.state] + city.population

        
        #statepopulation.sort(key = lambda x:x,reverse = False)
        
        from operator import itemgetter
        sortedpopulation = sorted(statepopulation.items(), key=itemgetter(1), reverse = True)
        
        lim = len(sortedpopulation)

        for i in range(0,num):
            if i< lim:
                print sortedpopulation[i][0] + " " + str(sortedpopulation[i][1])

        # Here implement one more method which will use heaps to get this in O(num.log(n))

    #----------------------end of state functions------------------#

    #--------------------------edge functions-------------------:

    def selectAllEdges(self):
        #selecting all edges
        self.selected_edges = self.cityGraph.edges(None,True)

    def unselectAllEdges(self):
        self.selected_edges = []

    def printEdges(self):
        #print "printing all the selected edges"
        #print self.selected_edges
        for myedge in self.selected_edges:
            print myedge[0]+ " "+myedge[1] + " "+ str(self.cityGraph.edge[myedge[0]][myedge[1]]['distance'])

    def selectEdges(self,lowerBound, upperBound):
        print "Assuming NO EDGES are selected previously, selecting edges with distances between ",lowerBound," to ",upperBound
        self.unselectAllEdges()
        for myedge in self.cityGraph.edges(None,True):
            wt = myedge[2]['distance']
            if lowerBound<= wt <= upperBound :
                #if myedge not in self.selected_edges:
                    self.selected_edges.append(myedge)

        if(len(self.selected_edges) <= 0):
            #self.printEdges()            
        #else :
            print "No such edges"









    #--------------------------end of edge functions---------------#


    #-----------------------Graph Functions ------------------------#

    def testMinMaxConsDistance(self):
        #for city in self.selection:
        #    print city.name
        print "Goal: minimize the maximum distance between any pair of consecutive cities on path from source to destination."

        while True:
            source = raw_input("Source (City, State): ")
            target = raw_input("Target (City, State): ")
            if source in ('','\n'):
                break
            elif target in ('','\n'):
                break
            else:                
                network = self.makeGraph()
                sflag = False
                tflag = False
                for node in network.nodes():
                    if node == source:
                        sflag = True
                    if node == target:
                        tflag = True

                if sflag == True and tflag == True:

                    allpaths = []
                    allpaths = self.find_all_paths(network,source,target,allpaths)
                    maxofpaths= []
                    for k in range(0,len(allpaths)):
                        maxofpaths.append(0)

                    if len(allpaths)>0:
                        for i in range(0,len(allpaths)):
                            for j in range(0,len(allpaths[i])-1):
                                length = network.edge[allpaths[i][j]][allpaths[i][j+1]]['distance']
                                #print length
                                if length > maxofpaths[i]:
                                    maxofpaths[i]=length

                        z = maxofpaths.index(min(maxofpaths))
                        print "Cost of optimal solution: ",int(maxofpaths[z])
                        print "Path from",source,"to",target,": "
                        for city in allpaths[z]:
                            print city

                    else:
                        print "No path exists"
                else:
                    print "Input Error. Please enter correct name of the city and state."
                

                










    def find_all_paths(self,graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        #if not graph.has_key(start):
        #    return []
        paths = []
        for node in graph[start]:
            if node not in path:
                newpaths = self.find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths


                


    def makeGraph(self):

        currentlySelectedCities = []
        for city in self.selection:
            currentlySelectedCities.append(city.name)
        citySubGraph = self.cityGraph.subgraph(currentlySelectedCities).copy()
        subEdges  =  citySubGraph.edges(None,True)
        common = []
        for edge in subEdges:
            for selectededge in self.selected_edges:
                if (edge[0] == selectededge[0] and edge[1]== selectededge[1]):
                    common.append(selectededge)
                elif (edge[1]==selectededge[0] and edge[0]== selectededge[1]):
                       common.append(selectededge)

        citySubGraph = nx.Graph(common)
        return citySubGraph

    def minCut(self):
        G = self.makeGraph()
        H = G.copy()
        lim = len(G.nodes())
        part = G.nodes()[0]
        theMinCut = 1000000000000
        for i in range(1,lim):
            randomNode = G.nodes()[0]
            cut = self.findcut(G,randomNode)
            if cut <= theMinCut:
                theMinCut = cut
                part = randomNode
            z = self.tightlyConnected(G,randomNode)
            G = self.combineNodes(G,randomNode,z)        
        mincutedges = []
        scut = part.split('|')        
        scut = set(scut)        
        all = set(H.nodes())
        tcut = all.difference(scut)        
        scut = list(scut)                
        for snode in scut:
            nbr = set(H.neighbors(snode))
            #print "neighbors of",snode,"are:",nbr
            nbr = tcut.intersection(nbr)
            #print "T-cut neighbors of",snode,"are:",nbr
            nbr = list(nbr)
            #print nbr
            for n in nbr:                                        
                    mincutedges.append((snode,n))#,H.edge[snode][n]))

        print "The edges in the mincut are "
        for ed in mincutedges:
            print ed,
        print
        print "Weight of the min-cut:",str(theMinCut)
        


    def findcut(self,H,s):
        nbr = H.neighbors(s)
        sum = 0
        if len(nbr) > 0:
            for node in nbr:
                sum = sum + H.edge[node][s]['distance']
                
        return sum



    def tightlyConnected(self,G,a):
        wtmax = 0
        nbr = G.neighbors(a)
        if len(nbr)>0:
            tight = nbr[0]
            for node in nbr:
                if G.edge[node][a]['distance'] >= wtmax:
                    tight = node
                    wtmax = G.edge[node][a]['distance']
            return tight


    def combineNodes(self,G,s,t):
        H = G.copy()        
        st = str(s)+"|" + str(t)       
        H.add_node(st)
        """
        steps to be followed:
        1) remove the edge, if exists, between s,t
        2) create a new node, which is the combined node of s,t
        3) find common neighbors of s,t
        4) for each common node, add an edge to the new node, with distace= sum of distances.
        5) find all nodes connected to s and not in common
        6) add an edge between new node and all nodes in 5
        7) remove previous nodes from s to nodes in 5
        8) repeat 5,6,7 for t
        """
        if H.has_edge(s,t):
            H.remove_edge(s,t)       

        snbr = set(H.neighbors(s))       
        tnbr = set(H.neighbors(t))
        common = snbr.intersection(tnbr)      
        commonNodes = list(common)

        for node in commonNodes:
            sum = G.edge[s][node]['distance'] + G.edge[t][node]['distance']
            H.add_edge(st,node,distance=sum)
            H.remove_edge(s,node)
            H.remove_edge(t,node)                    

        sdiff = snbr.difference(common)        
        sdiff = list(sdiff)

        for node in sdiff:
            H.add_edge(st,node,distance= H.edge[s][node]['distance'])
            H.remove_edge(s,node)
        tdiff = tnbr.difference(common)        
        tdiff = list(tdiff)        
        
        for node in tdiff:
            H.add_edge(st,node,distance= H.edge[t][node]['distance'])
            H.remove_edge(t,node)        

        H.remove_node(s)
        H.remove_node(t)
        
        return H
    

    def tour(self,start):
        length = 0
        H = self.makeGraph()
        statusFlag = False
        for node in H.nodes():
            if start == node:
                statusFlag = True

        if statusFlag == True:
            
            noofcities = len(H.nodes())
            if noofcities is not 0:

                    for node in H.nodes():
                        H.add_node(node,marker = False)
                    curr = start
                    #.split(",")[0]
                    first = curr
                    #H.node['Youngstown']['marker']= True  way to access it..
                    #print H.node['Youngstown']['marker']
                    #for n in H.nodes(True):
                    #   print n[1]['marker']
                    flag = False
                    nbr = []
                    order = []
                    while True:
                            order.append(curr)
                            H.node[curr]['marker']= True
                            nbr =  H.neighbors(curr)
                            counter = 0
                            for j in range(0,len(nbr)):
                                if H.node[nbr[counter]]['marker'] == True:
                                    nbr.remove(nbr[counter])
                                else:
                                    counter = counter + 1
                            if(len(nbr) == 0):
                                if noofcities != len(order):
                                    print "Traveling Salesman Tour starting from",start,"is not possible."
                                    flag = False
                                else:
                                    if H.has_edge(order[len(order)-1],first):
                                        flag = True
                                        length = length + H.edge[order[len(order)-1]][first]['distance']
                                    else:
                                        flag = False
                                break
                            else:
                                min = 10000000000
                                next = nbr[0]
                                for node in nbr:
                                    wt = H.edge[curr][node]['distance']
                                    if wt < min:
                                        min = wt
                                        next = node
                                curr = next
                                length = length + min
                    if flag == True:
                        #print "final order"
                        order.append(start.split(",")[0])
                        lim = len(order)
                        if lim >= 4:
                            for i in range(0,lim/4):
                                if i == lim/4-1:
                                    print order[4*i],"-->",order[4*i+1],"-->",order[4*i+2],"-->",order[4*i+3]
                                else:
                                    print order[4*i],"-->",order[4*i+1],"-->",order[4*i+2],"-->",order[4*i+3],"-->"

                            for j in range(0,lim%4):
                                if j== lim%4-1:
                                    print order[(lim/4)*4+j],
                                else:
                                    print order[(lim/4)*4+j],"-->",
                        else :
                            for j in range(0,lim):
                                print order[j],"-->",

                        print "Tour length:",str(length)
            else:
                print "Traveling Salesman Tour starting from",start,"is not possible."
        else:
                print "Traveling Salesman Tour starting from",start,"is not possible."



    #---------------------End of Graph Functions --------------------#







