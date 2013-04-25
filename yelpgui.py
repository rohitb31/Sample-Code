import urllib.request
from re import findall
import csv
from tkinter import *


class yelp:

    def __init__(self, rootwin):

        label1 = Label(rootwin, text= "Enter URL") # creating the label in the zero row that says Max Finder
        self.readEntry= Entry(rootwin, width=60, state = "normal")
        button1 = Button(rootwin, text = "Write to CSV", command=self.clicked) # creating the button on the 1 row to the bottom left


        label1.grid(row = 0, column = 1) 
        button1.grid(row = 2, column = 1) 
        self.readEntry.grid(row = 1 , column = 1)


    def clicked(self):
        self.origurl=self.readEntry.get()
        self.csvwriter(self.origurl)



    def readurl(self):
      
        response = urllib.request.urlopen(self.origurl)
        html = response.read()
        self.text = str(html)#Convert the bytes to a string



    def dollarsign(self):

        pricehelp=self.text.find("</span>\\n\\t</span>") ##finds dollar sign amount
        help1=self.text.find("$61")
        help2=help1+5
        pricehelp1=pricehelp
        pricelevel="Price Range=" + self.text[help2:pricehelp1]

        self.pricelevel=pricelevel



    def extrareviews(self):
        text=self.text
        emptystr=""
        namecrop=findall("[0-9]+ Reviews of", text)
        zero=namecrop[0]
        total=zero.find("R")
        totalreviews=zero[:total]
        urllist=[]
        totals=int(totalreviews)

       # print(totals)

        if totals>=40:

            div=totals//40

            add=div*40

            rangelist=list(range(40,totals,40))

          
           
            
            rangelist=list(range(40,totals,40))
            for thing in rangelist:
                newurl=self.origurl+"?start="+ str(thing)
                urllist.append(newurl)
            
        else:
            pass
        self.urllist=urllist

    def searchurl(self):
        self.readurl()
        text=self.text
        url=self.origurl
     

        #Finds name
        name=url.find("biz")+4
        name1=url[name:]

        namecrop=findall("[0-9]+ Reviews of [a-zA-Z]* *[a-zA-Z]* *[a-zA-Z]*", text)
        zero=namecrop[0]
        total=zero.find("R")
        totalreviews=zero[:total]

        totals=int(totalreviews)
        
       
        
        
        #Adds Rating Column
        newlist=[]
        self.dollarsign()
        level=self.pricelevel
        newlist.append(level)
        newlist.append("Rating")
        
        

        #finds rating
        cutoff=text.find("Published")-1000
        newtext=text[cutoff:]
        dataCrop1=findall('itemprop="ratingValue" content="[0-9].0', newtext)
        for thing in dataCrop1:
            num=thing.find("content")+9
            thing1=thing[num:]+" stars"
            newlist.append(thing1)

        #Adds Date Column
        datelist=[]
        newdatelist=[]
        newdatelist.append(zero)
        newdatelist.append("Date")

        
            
        #finds date
        date=findall('itemprop="datePublished" content="[0-9]+-[0-9]+-[0-9]+', text)
        for dat in date:
            num1=dat.find("content")+11
            thing1=dat[num1:]
            datelist.append(thing1)
        
        length=(len(newlist))-1
      

        # formats date
        for stuff in datelist:
            year=stuff[:2]
            month=stuff[3:5]
            day=stuff[6:8]
            newstring=month+"/"+day+"/"+year
            newdatelist.append(newstring)
       # print (len(newdatelist))
       # print(len(newlist))
        self.finallist=[]
        x=0
        while x <= length:
            tuple1=(newdatelist[x],newlist[x])
            self.finallist.append(tuple1)
            x+=1           



    def extrasort(self):
        self.extrareviews()
        aList=self.urllist
        aList1=[]
        for thing in aList:
            self.origurl=thing
            self.readurl()
            self.searchurl()
            aList1.append(self.finallist)
        infoList=[]
        for info in aList1:
            for info1 in info:
                infoList.append(info1)

        cleaned=[]

        for thing in infoList:
            if "stars" in thing[1]:
                cleaned.append(thing)
        self.cleaned=cleaned






    def csvwriter(self,url):

        self.searchurl()
        finallist=self.finallist
        finalList=[]
        self.extrasort()
        adding=self.cleaned
        title=url.find("biz")+4
        name=url[title:]+".csv"

        if len(adding)>1:
            finalList=finallist+adding
        else:
            finalList=finallist
       

        file = open(name, "w", newline="")
        csvWriter = csv.writer( file )  #Defaults to the excel 
        csvWriter.writerows(finalList)
        file.close()   


root = Tk()
app=yelp(root)
root.mainloop()






