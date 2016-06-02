"""
Description : Simulate 1000 visits to the provided 15 restaurants,
              and provide visualizations showing frequency that each restaurant is visited, their distance,
              and the rating that the algorithm calculated for each of the restaurant.

Author : Nandan Nayak

Date : 01/June/2016
"""

#import all modules
import string
import math
import random
import matplotlib.pyplot as plt
import sys


#define global variables
ratingsDoc="ratings.txt"
restDoc="restaurants.txt"
user="you"
neighborhood=int(sys.argv[1])
maxVisits=1000
maxRest=15
idx2={"A":1,"B":2,"C":3,"D":4,"E":5,"F":6,"G":7,"H":8,"I":9,
          "J":10,"K":11,"L":12,"M":13,"N":14,"O":15}
restDict={1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{},
           11:{},12:{},13:{},14:{},15:{}}
restInfo={"A":{},"B":{},"C":{},"D":{},"E":{},"F":{},"G":{},"H":{},"I":{},
          "J":{},"K":{},"L":{},"M":{},"N":{},"O":{}}
ratingInfo={}



#define functions
def getUnratedRest():
    """Finds the list of restaurants that are unrated by the user=you """
    global restDict
    tempList=[]
    for restaurant in restDict:        
        if restDict[restaurant][user]=="":            
            tempList.append(restaurant)    
    return tempList
    
def getCommonUsers(rest1,rest2):
    """Returns a list of users who have rated the given pair of restaurants
rest1 - Restaurant 1
rest2 - Restaurant 2"""
    global restDict
    tempList=[]    
    for usr in restDict[rest1]:
        if restDict[rest1][usr]!="" and restDict[rest2][usr]!="":
            tempList.append(usr)
    return tempList

def getAvg(inList,rest):
    """Returns the average rating of a restaurant based on co-rated users
    inList - List of co-rated users
    rest - Restaurant"""
    global restDict
    total=0
    for users in inList:
        total+=restDict[rest][users]
    avg=float(total)/float(len(inList))
    return avg

def getLine(inString):
    """Converts a string into a list and returns it by removing the \n character and using split()
    inString - input string"""
    inString=inString.replace("\n","")
    inString=inString.split(";")
    return inString

def getDist(inLine):
    """"Returns the distance of a restaurant using Euclidian distance equation
    inLine - Line in restaurants.txt"""
    x_Coord=2
    y_Coord=3
    x=float(inLine[x_Coord])
    y=float(inLine[y_Coord])
    dist=math.sqrt(x**2 + y**2)
    return dist

def barPlot(inDict,inList,step,col,y_label,title,isRating, isLegend):
    """Plots a barchart - 
    inDict : input Dictionary,
    inList : List which contains a restaurants which are sorted based on the no. of visits
    step : step size to have enough padding in the legend
    col : Color of bar graph
    y_label : string for y_label
    title : Title for the graph
    isRating : boolean for rating bar graph
    isLegend : boolean to print the legend"""
    x=inList
    y=[]
    for item in inList:
        y.append(inDict[item])    
    length=len(inDict)
    i=0
    j=length
    k=float(max(y))+30.0
    size=8   
    
    for key in inList:
        if isRating:            
            if restInfo[key]["type"]=="predicted":
                text="P"
            else:
                text="R"
            plt.text(i,inDict[key],"%d(%s)"%(inDict[key],text),ha="center",va="bottom")
            i+=1
        else:
            plt.text(i,inDict[key],inDict[key],ha="center",va="bottom")
            i+=1

        if isRating:
           plt.text(j,2.25,"(P)-Predicted Rating",bbox=dict(boxstyle="round",color="red"),fontsize=size)
           plt.text(j,2.75,"(R)-User Rating",bbox=dict(boxstyle="round",color="red"),fontsize=size)
        
        if isLegend:            
           k=k-step
           plt.text(j,k,"%s : %s"%(key,restInfo[key]["name"]),bbox=dict(boxstyle="round",color="pink"),fontsize=size) 
        
    plt.bar(range(length),y,align="center",color=col)
    plt.xticks(range(length),x)    
    plt.ylabel(y_label)
    plt.title(title)
    


#define main
if __name__ == "__main__":
    """If the neighborhood value is out of range, throw an error"""
    if neighborhood>(maxRest-1) or neighborhood<1:
        print "\nThe entered neighborhood value %d is out of range<1,14>\n"%(neighborhood)
        sys.exit()
    myFile=open(ratingsDoc)
    count=0
    for line in myFile:
        if count==0:
            count+=1
            continue
        line=getLine(line)
        reviewer=line[0]
        for i in range(1,len(line)):
            if line[i]=='':
                rating=line[i]
            else:
                rating=int(line[i])
            restDict[i][reviewer]=rating
            
    """unratedRestList: Contains a list of unrated restaurants, ratings of which have to be predicted"""      
    unratedRestList=getUnratedRest()


    """W:Contains a dictionary of values representing the Pearson Co-relation between restaurants"""
    W={}
    for unratedRest in unratedRestList:
        W[unratedRest]={}


    """Calculate the Pearson correlation between the restaurants"""    
    for restaurant in restDict:
        for unratedRest in W:
            if restaurant!=unratedRest:
                commonUsersList=getCommonUsers(restaurant,unratedRest)
                avgRating = getAvg(commonUsersList,restaurant)
                avgUnRatedRest = getAvg(commonUsersList,unratedRest)
                Nr=Dr=term1=term2=0

                for users in commonUsersList:
                    Nr+=(restDict[restaurant][users]-avgRating)*(restDict[unratedRest][users]-avgUnRatedRest)
                    term1+=(restDict[restaurant][users]-avgRating)**2                    
                    term2+=(restDict[unratedRest][users]-avgUnRatedRest)**2
                term1=math.sqrt(term1)
                term2=math.sqrt(term2)
                Dr=term1*term2 
                if Dr!=0:
                    val=Nr/Dr
                else:
                    val=0
                W[unratedRest][restaurant]=val


    """sortedWDict : sorted in decreasing order of Pearson correlation value"""
    sortedWDict={}
    for unratedRest in W:
        tempList=[]
        tempDict=W[unratedRest]
        tempList=[v[0] for v in sorted(tempDict.iteritems(), key=lambda(k, v): (-v, k))]
        sortedWDict[unratedRest]=tempList



    """Calculate the ratings of unrated restaurants by taking weighted average"""
    predictionDict={}
    for unratedRest in sortedWDict:
        Nr=Dr=0.0
        m=neighborhood
        if len(sortedWDict[unratedRest]) < neighborhood:
            m=len(sortedWDict[unratedRest])
        i=0
        
        while i<len(sortedWDict[unratedRest]) and i<m:            
            ratedRest=sortedWDict[unratedRest][i]
            if restDict[ratedRest][user]!="":
                Nr+=(W[unratedRest][ratedRest])*(restDict[ratedRest][user])
                Dr+=(W[unratedRest][ratedRest])
            else:
                m+=1
            i+=1
        val=float(Nr)/float(Dr)
        if Dr!=0:   
            predictionDict[unratedRest]=val        
        else:
            predictionDict[unratedRest]=0.0
        
    """tempList: tuple of restaurant and its predicted value"""    
    tempList=sorted(predictionDict.items(),key=lambda(k,v):(-v,k))
    


    """predictedRatings : contains the tuple of unrated restaurant and its predicted ratings"""
    predictedRatings={}
    for tup in tempList:
        key=tup[0]
        val=tup[1]
        if val>5:
            predictedRatings[key]=5
        elif val<1:
            predictedRatings[key]=1
        else:
            predictedRatings[key]=int(round(val))



    """restInfo: contains all info regarding a restaurant with no visits recorded"""    
    myFile2=open(restDoc)
    count=0    
    for line in myFile2:
        if count==0:
            count+=1
            continue
        line=getLine(line)        
        distance=getDist(line)
        rest=line[0]
        restInfo[rest]["visits"]=0
        restInfo[rest]["dist"]="{0:0.2f}".format(distance)
        restInfo[rest]["name"]=line[1]
        restNum=idx2[rest]        
        if restNum in predictedRatings:
            restInfo[rest]["rating"]=predictedRatings[restNum]
            restInfo[rest]["type"]="predicted"
        else:
            restInfo[rest]["rating"]=restDict[restNum][user]
            restInfo[rest]["type"]="rated"



    """ratingInfo : with distances for each restaurant for each rating (1-5)"""
    for rest in restInfo:
        val=restInfo[rest]["rating"]
        distance=restInfo[rest]["dist"]
        if val not in ratingInfo:
            ratingInfo[val]=[]
            ratingInfo[val].append([rest,distance])
        else:
            ratingInfo[val].append([rest,distance])



    """ratingInfo : sorted according to distances and distances replaced with intervals"""
    for rating in ratingInfo:
        ratingInfo[rating]=sorted(ratingInfo[rating],key=lambda x: x[1])
        initLength=len(ratingInfo[rating])+2
        interval=0
        for item in ratingInfo[rating]:
            initLength-=1
            interval+=initLength
            item[1]=interval



    """restInfo: with updated visits"""
    i=0
    while i<maxVisits:
        #ratingChoice=random.choice(range(1,6))
        ratingChoice=random.choice(range(21))
        if ratingChoice<=6:
            ratingChoice=5
        elif ratingChoice<=11:
            ratingChoice=4
        elif ratingChoice<=15:
            ratingChoice=3
        elif ratingChoice<=18:
            ratingChoice=2
        elif ratingChoice<=20:
            ratingChoice=1
        length=len(ratingInfo[ratingChoice])
        maxVal=ratingInfo[ratingChoice][length-1][1]
        restChoice=random.choice(range(maxVal))
        for item in ratingInfo[ratingChoice]:
            if restChoice<=item[1]:
                restChoice=item[0]
                if ratingChoice==1 or ratingChoice==2:
                    if restInfo[restChoice]["type"]=="rated" and restInfo[restChoice]["visits"]==0:
                        restInfo[restChoice]["visits"]+=1
                        i+=1
                else:
                    restInfo[restChoice]["visits"]+=1
                    i+=1

    
    """freqDict : key=Restaurant, value=Freq. of visits"""
    freqDict={}
    """distDict : key=Restaurant, value=distance"""
    distDict={}
    """ratingsDict : key=Restaurant, value=its rating"""
    ratingsDict={}
    for rest in restInfo:        
        freqDict[rest]=restInfo[rest]["visits"]
        distDict[rest]=restInfo[rest]["dist"]
        ratingsDict[rest]=restInfo[rest]["rating"]
        

    """freqKeyList : Contains restaurants sorted in decreasing order of visits"""
    freqKeyList=[v[0] for v in sorted(freqDict.iteritems(), key=lambda(k, v): (-v, k))]


    """Plot the Bar Graph"""
    """First subplot is graph of Distance against Restaurants"""
    plt.subplot(3,1,1)
    barPlot(distDict,freqKeyList,0.2,"yellow","Distance","Distance of restaurants",0,0)
    
    """Second subplot is graph of Ratings against Restaurants"""
    plt.subplot(3,1,2)
    barPlot(ratingsDict,freqKeyList,0.4,"orange","Restaurant Ratings","Ratings of Restaurants",1,0)
    
    """Third subplot is graph of Frequency of visits against Restaurants"""
    plt.subplot(3,1,3)
    valList=freqDict.values()
    step=(max(valList)/10)-10
    barPlot(freqDict,freqKeyList,step,"green","Frequency","Frequency of each restaurant visited",0,1)
    plt.xlabel("Restaurant Names")
    plt.show()

    



                    
