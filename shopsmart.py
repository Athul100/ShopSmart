import sys
import os
import urllib
from PyQt4 import QtGui,QtCore,Qt
from lxml import html
import requests
class Window(QtGui.QWidget):
    def __init__(self,parent=None):
        #-----------------------------------------------
        
        #-----------MAIN WINDOW START------------------

        
        super(Window,self).__init__()
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background,QtGui.QColor.fromHsv(30, 193, 247))
        self.setPalette(palette)
        self.setFixedSize(1200, 600);
        self.setWindowTitle("Shop Smart")
        self.setWindowIcon(QtGui.QIcon('shop.gif'))
        extractAction = QtGui.QAction("&Quit",self)
        extractAction.setShortcut("ctrl+Q")
        extractAction.triggered.connect(self.close_application)
        QtGui.QStatusBar()
        self.mainMenu = QtGui.QMenuBar(self)
        fileMenu = self.mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)
        pic = QtGui.QLabel(self)
        pic.setGeometry(10, 10, 30, 30)
        pic.move(10,40)
        pic.setStyleSheet("QLabel { background-color : white;  }")
        pic.setPixmap(QtGui.QPixmap(os.getcwd() + "/search1.png"))
        self.pic1 = QtGui.QLabel(self)
        self.pic1.setGeometry(100, 400, 1500, 500)
        self.pic1.move(0,70)
        self.pic1.setPixmap(QtGui.QPixmap(os.getcwd() + "/market1.png"))
        self.button = QtGui.QPushButton('Search', self)
        self.button.move(350,40)
        self.button.resize(50,30)
        self.button.clicked.connect(self.on_click)
        self.button.setStyleSheet('QPushButton { border: none;background-color: white; color: black;}')
        self.setFocus()
        self.grid = QtGui.QGridLayout()
        self.opt=0
        self.home()
        #----------------MAIN WINDOW END--------------------

        #--------------------------------------------------

    def home(self):
        #-------------------------------------------------

        #----------------SEARCH BOX START----------------
        self.textbox=QtGui.QLineEdit(self)
        self.textbox.setPlaceholderText("So, what are you wishing for today?")
        self.textbox.move(40, 40)
        self.textbox.resize(280,30)
        self.textbox.setStyleSheet("QLineEdit { border: none }")
        #-------------------------------------------------

        #----------------SEARCH BOX END----------------
        self.show()
    
    def keyPressEvent(self, evt):
            self.textbox.setFocus()
            self.textbox.keyPressEvent(evt)

    def close_application(self):
        choice = QtGui.QMessageBox.question(self,'QUIT','Are you sure you want to quit?',QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
                                            sys.exit()
        else:
                                            pass
    def on_click(self):
        self.item=self.textbox.text()
        print self.item
        self.item=self.item.replace(' ','+')
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        link = 'http://www.flipkart.com/search/a/all?query={0}&vertical=all&dd=0&autosuggest[as]=off&autosuggest[as-submittype]=entered&autosuggest[as-grouprank]=0&autosuggest[as-overallrank]=0&autosuggest[orig-query]=&autosuggest[as-shown]=off&Search=%C2%A0&otracker=start&_r=YSWdYULYzr4VBYklfpZRbw--&_l=pMHn9vNCOBi05LKC_PwHFQ--&ref=a2c6fadc-2e24-4412-be6a-ce02c9707310&selmitem=All+Categories'.format(self.item)
        try:
            page = requests.get(link)
            self.tree = html.fromstring(page.content)
            self.get_flip_suggestions() #gets suggestion from flipkart
            status=1
        except:
            print "No internet connection "
            QtGui.QApplication.restoreOverrideCursor()
            status=0
        if status==1:
            self.pic1.hide()
            QtGui.QApplication.restoreOverrideCursor()
            #----------------------------SHOW FLIPKART SUGGESTIONS ONSCREEN--------------------

            index=0
            for i, name in enumerate(self.title1):
                QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
                new_name=name+"\n\n\t"+self.price1[i]
                button = QtGui.QPushButton(new_name, self)
                
                button.clicked.connect(self.flip_search(name))
                button.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
                button.setStyleSheet('QPushButton {background-color: silver; color: black;}')
                url = self.img1[index]
                index+=1
                


                data= requests.get(url).content

                
                QtGui.QApplication.restoreOverrideCursor()
                
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(data)
                
                button.setIcon(QtGui.QIcon(pixmap))
                button.setIconSize(QtCore.QSize(100,100))
                row, col = divmod(i, 2)
                self.grid.addWidget(button, row, col)
            self.setLayout(self.grid)
            #------------------------------------------------------------------------
        
            self.back_button = QtGui.QPushButton('Back',self)
            self.back_button.clicked.connect(self.onclick2)
            self.back_button.move(650,440)
            self.back_button.show()
            self.suggest_button = QtGui.QPushButton('More Suggestions..',self)
            self.suggest_button.clicked.connect(self.onclick3)
            self.suggest_button.move(650,470)
            self.suggest_button.resize(150,40)
            self.suggest_button.show()

    def get_flip_suggestions(self):
        
        i=0
        self.new_link1=[]
        self.img1=[]
        self.title1=[]
        for elt in self.tree.xpath('//div[contains(@class,"pu-visual-section")]//a[contains(@class,"pu-image fk-product-thumb")]'):
            try:
                self.new_link1.append(elt.attrib['href'])
                i+=1
                if i==7:
                    break
            except:
                pass
        i=0
        for elt in self.tree.xpath('//div[contains(@class,"pu-visual-section")]//a[contains(@class,"pu-image fk-product-thumb")]//img'):
            try:
                self.img1.append(elt.attrib['data-src'])
                i+=1
                if i==7:
                    break
            except:
                pass
        i=0
        for elt in self.tree.xpath('//div[contains(@class,"pu-details lastUnit")]//a[contains(@class,"fk-display-block")]'):
            try:
                self.title1.append(elt.attrib['title'])
                i+=1
                if i==7:
                    break
            except:
                pass
        i=0
        self.price1=self.tree.xpath('//div[contains(@class,"pu-details lastUnit")]//div[contains(@class,"pu-price")]//span/text()')
        
    def flip_search(self, name):
        def flip_search():
            print(name)
            self.onclick2()
            ####-----------------show details of flipkart ------
            self.pic1.hide()
            self.show_flipkart_details(name)
            self.cmpre_button = QtGui.QPushButton('Compare with AMAZON',self)
            self.cmpre_button.clicked.connect(self.compare_amazon)
            self.cmpre_button.move(700,240)
            self.cmpre_button.resize(180,40)
            self.cmpre_button.show()
            
            
        return flip_search
    def ama_search(self, name):
        def ama_search():
            print(name)
            self.onclick2()
            ####-----------------show details of amazon ------
            self.pic1.hide()
            self.title=name
            self.fliptoamazonSearch()
            self.display_amazon_specs()
            self.button4.hide()
            self.cmpre_button = QtGui.QPushButton('Compare with Flipkart',self)
            self.cmpre_button.clicked.connect(self.compare_flipkart)
            self.cmpre_button.move(200,240)
            self.cmpre_button.resize(180,40)
            self.cmpre_button.show()
            
            
        return ama_search
    def compare_flipkart(self):
        self.button4.show()
        self.amatoflipsearch()
    def amatoflipsearch(self):
        self.item=self.item.replace(' ','+')
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        link = 'http://www.flipkart.com/search/a/all?query={0}&vertical=all&dd=0&autosuggest[as]=off&autosuggest[as-submittype]=entered&autosuggest[as-grouprank]=0&autosuggest[as-overallrank]=0&autosuggest[orig-query]=&autosuggest[as-shown]=off&Search=%C2%A0&otracker=start&_r=YSWdYULYzr4VBYklfpZRbw--&_l=pMHn9vNCOBi05LKC_PwHFQ--&ref=a2c6fadc-2e24-4412-be6a-ce02c9707310&selmitem=All+Categories'.format(self.item)
        page = requests.get(link)
        self.tree = html.fromstring(page.content)
        self.get_flip_suggestions()

        for elt in self.tree.xpath('//div[contains(@class,"pu-visual-section")]//a'):
            new=elt.attrib['href'], elt.text_content()
            break
        ##########################################################
        for elt in self.tree.xpath('//div[contains(@class,"pu-visual-section")]//a[contains(@class,"pu-image fk-product-thumb")]'):
            try:
                self.new_link1=elt.attrib['href']
            except:
                pass
        i=0
        for elt in self.tree.xpath('//div[contains(@class,"pu-visual-section")]//a[contains(@class,"pu-image fk-product-thumb")]//img'):
            try:
                self.img1=elt.attrib['data-src']
              
            except:
                pass
        i=0
        for elt in self.tree.xpath('//div[contains(@class,"pu-details lastUnit")]//a[contains(@class,"fk-display-block")]'):
            try:
                self.title1=elt.attrib['title']
            except:
                pass
        i=0
        self.price1=self.tree.xpath('//div[contains(@class,"pu-details lastUnit")]//div[contains(@class,"pu-price")]//span/text()')

        ##########################################################
        self.opt=1
        self.show_flipkart_details2()
        
        
    def show_flipkart_details2(self):
            href='http://www.flipkart.com'+self.new_link1

            url=self.img1
            data= requests.get(url).content
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(data)
            image = QtGui.QImage()
            image.loadFromData(data)
            val=0
            self.lbl = QtGui.QLabel(self)
            mypixmap=QtGui.QPixmap(image)
            self.lbl.resize(100,100)
            myScaledPixmap=mypixmap.scaled(self.lbl.size(),QtCore.Qt.KeepAspectRatio)
            self.lbl.setPixmap(myScaledPixmap)
            self.cmpre_button.hide()
            
            self.lbl.setStyleSheet('QLabel {font: bold ;   font-size: 16pt; color: black;}')
            self.lbl.move(5,150)
            self.lbl.show()
            self.lbl1 =  QtGui.QLabel(self)
            

            self.lbl1.setText(self.title)
            self.lbl1.setStyleSheet('QLabel {font: bold ;   font-size: 16pt; color: black;}')
            self.lbl1.resize(500,160)
            self.lbl1.setWordWrap(True)
            self.lbl1.move(110,110)
            
            self.lbl1.show()
            
            self.lbl2 =  QtGui.QLabel(self)
            
            self.flip_price=self.price1[val]
            self.lbl2.setText(self.flip_price)
            self.lbl2.setStyleSheet('QLabel {font-size: 16pt; color: black;}')
            self.lbl2.resize(150,40)
            self.lbl2.move(220,260)
            
            self.lbl2.show()

            page = requests.get(href)
            self.tree3 = html.fromstring(page.content)
            QtGui.QApplication.restoreOverrideCursor()
            self.flip_rating=self.tree3.xpath('//div[contains(@class,"ratingHistogram")]//div[contains(@class,"bigStar")]/text()')

            if not self.flip_rating:
                self.flip_rating="not rated"
            else:
                self.flip_no_rating=self.tree3.xpath('//div[contains(@class,"ratingHistogram")]//p/text()')
                strin=self.flip_no_rating[1]
                self.flip_no_rating[1]=strin.strip()
            
            
            self.lbl3 =  QtGui.QLabel(self)    
            self.lbl3.setText("RATING:"+self.flip_rating[0]+'/5')
            self.lbl3.setStyleSheet('QLabel {font-size: 16pt; color: black;}')
            self.lbl3.resize(150,120)
            self.lbl3.move(220,260)
            
            self.lbl3.show()
            self.lbl4 =  QtGui.QLabel(self)    
            self.lbl4.setText("Ratings "+self.flip_no_rating[1])
            self.lbl4.setStyleSheet('QLabel {font-size: 16pt; color: black;}')
            self.lbl4.resize(450,120)
            self.lbl4.move(220,320)
            self.lbl4.show()
        
        
    def onclick2(self):
        while self.grid.count():
                    item = self.grid.takeAt(0)
                    widget = item.widget()
                    widget.deleteLater()
        self.back_button.hide()
        self.suggest_button.hide()
        self.pic1.show()

    def onclick3(self):
        self.onclick2()
        self.pic1.hide()
        self.suggest_button.hide()
        link = 'http://www.amazon.in/s/ref=nb_ss_gw/102-1882688-6100927?initialSearch=1&url=search-alias%3Daps&field-keywords='+self.item+"&Go.x=0&Go.y=0&Go=Go"
        try:
            page = requests.get(link)
            self.tree1 = html.fromstring(page.content)
            
            self.get_amazon_sugestions()#gets suggestion from Amazon
            status=1
        except:
            print "No internet connection"
            status=0

    #--------------------------------SHOW AMAZON SUGGESTIONS ON SCREEN-------------------------
        if status==1:
            index=0
            for i, name in enumerate(self.title2):
                QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
                new_name=name+"\n\n\t"+self.price2[i]
                button = QtGui.QPushButton(new_name, self)
                button.clicked.connect(self.ama_search(name))
                button.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
                button.setStyleSheet('QPushButton {background-color: white; color: black;}')
                url = self.img2[index]
                index+=1
                data= requests.get(url).content
                QtGui.QApplication.restoreOverrideCursor()
                
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(data)
                
                button.setIcon(QtGui.QIcon(pixmap))
                button.setIconSize(QtCore.QSize(100,100))
                row, col = divmod(i, 2)
                self.grid.addWidget(button, row, col)
                
            self.setLayout(self.grid)
            
        #----------------------------------------------------------
        
            self.back_button = QtGui.QPushButton('Back',self)
            self.back_button.clicked.connect(self.onclick2)
            self.back_button.move(650,440)
            self.back_button.show()

    def get_amazon_sugestions(self):
        i=0
        self.new_link2=[]
        self.img2=[]
        self.title2=[]
        for elt in self.tree1.xpath('//div[contains(@id,"atfResults")]//div[contains(@class,"a-column a-span12 a-text-center")]//a[contains(@class,"a-link-normal a-text-normal")]'):
            self.new_link2.append(elt.attrib['href'])
            i+=1
            if i==7:
                break

        i=0
        for elt in self.tree1.xpath('//div[contains(@id,"atfResults")]//div[contains(@class,"a-column a-span12 a-text-center")]//a[contains(@class,"a-link-normal a-text-normal")]//img'):
            self.img2.append(elt.attrib['src'])
            i+=1
            if i==7:
                break
        i=0
        for elt in self.tree1.xpath('//div[contains(@id,"atfResults")]//div[contains(@class,"a-fixed-left-grid-col a-col-right")]//a[contains(@class,"a-link-normal s-access-detail-page  a-text-normal")]'):
            try:
                    self.title2.append(elt.attrib['title'])   
                    i+=1
                    if i==7:
                        break
            except:
                pass
        self.price2=self.tree1.xpath('//div[contains(@id,"atfResults")]//div[contains(@class,"a-row")]//a[contains(@class,"a-link-normal a-text-normal")]//span[contains(@class,"a-size-base a-color-price s-price a-text-bold")]/text()')        
        print self.price2
    def show_flipkart_details(self,name):
            if self.opt==0:
                i=0
                while i<len(self.title1):
                    if self.title1[i]==name:
                        val=i
                    else:
                        pass
                    i+=1
         
            self.title=self.title1[val]
            img=self.img1[val]
            href='http://www.flipkart.com'+self.new_link1[val]

            url=img
            data= requests.get(url).content
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(data)
            image = QtGui.QImage()
            image.loadFromData(data)

            self.lbl = QtGui.QLabel(self)
            mypixmap=QtGui.QPixmap(image)
            self.lbl.resize(100,100)
            myScaledPixmap=mypixmap.scaled(self.lbl.size(),QtCore.Qt.KeepAspectRatio)
            self.lbl.setPixmap(myScaledPixmap)
          
            
            self.lbl.setStyleSheet('QLabel {font: bold ;   font-size: 16pt; color: black;}')
            self.lbl.move(5,150)
            self.lbl.show()
            self.lbl1 =  QtGui.QLabel(self)
            

            self.lbl1.setText(self.title)
            self.lbl1.setStyleSheet('QLabel {font: bold ;   font-size: 16pt; color: black;}')
            self.lbl1.resize(500,160)
            self.lbl1.setWordWrap(True)
            self.lbl1.move(110,110)
            
            self.lbl1.show()

            self.lbl2 =  QtGui.QLabel(self)
            
            self.flip_price=self.price1[val]
            self.lbl2.setText(self.flip_price)
            self.lbl2.setStyleSheet('QLabel {font-size: 16pt; color: black;}')
            self.lbl2.resize(150,40)
            self.lbl2.move(220,260)
            
            self.lbl2.show()

            page = requests.get(href)
            self.tree3 = html.fromstring(page.content)
            
            self.flip_rating=self.tree3.xpath('//div[contains(@class,"ratingHistogram")]//div[contains(@class,"bigStar")]/text()')

            if not self.flip_rating:
                self.flip_rating="not rated"
            else:
                self.flip_no_rating=self.tree3.xpath('//div[contains(@class,"ratingHistogram")]//p/text()')
                strin=self.flip_no_rating[1]
                self.flip_no_rating[1]=strin.strip()
            
            
            self.lbl3 =  QtGui.QLabel(self)    
            self.lbl3.setText("RATING:"+self.flip_rating[0]+'/5')
            self.lbl3.setStyleSheet('QLabel {font-size: 16pt; color: black;}')
            self.lbl3.resize(150,120)
            self.lbl3.move(220,260)
            
            self.lbl3.show()
            self.lbl4 =  QtGui.QLabel(self)    
            self.lbl4.setText("Ratings "+self.flip_no_rating[1])
            self.lbl4.setStyleSheet('QLabel {font-size: 16pt; color: black;}')
            self.lbl4.resize(450,120)
            self.lbl4.move(220,320)
            self.lbl4.show()
    def compare_amazon(self):
            self.get_flipkart_specs()
            self.fliptoamazonSearch()
            self.display_amazon_specs()
            #self.get_amazon_searchid()
    def get_flipkart_specs(self):
            #self.tree3
            heads=self.tree3.xpath('//table//th[contains(@class,"groupHead")]/text()')
#print heads

            new= self.tree3.xpath('//table//th[contains(@class,"groupHead")]/text()|.//td[contains(@class,"specsKey")]/text() | .//td[contains(@class,"specsValue")]/text()|//table//td[@class="specsValue"]//div[contains(@class,"fk-hidden")]/text()[1]')


            i=0
            self.arr={} 


            while i<len(new):
                strin=new[i]
                new[i]=strin.strip()
                #print new[i]
                i+=1
            val=''
            self.spec_count={}
            while val in new:
                new.remove(val)
            i=0
            n=0
            self.header_count=0
            count=2
    #-------------
            t=len(heads)-1
            while i<len(new):
               # print i
        
                if new[i]==heads[n]:
                   # print heads[n]
                    #print "success"
                    j=i+1
                    #print n
                    #print len(heads)
                    if new[i]==heads[t]:
                       key=1
                       self.arr[self.header_count,0,0]=heads[t]
                       specCount=0
                       while i+1<len(new):
                            if count%2==0:
                               self.arr[self.header_count,key,0]=new[i+1]
                               self.arr[self.header_count,key+1,0]=0
                               specCount+=1
                               self.spec_count[self.header_count]=specCount
                               count+=1
                            else:
                                self.arr[self.header_count,key,1]=new[i+1]
                                self.arr[self.header_count,key+1,0]=0
                                key+=1
                                count+=1
                            i+=1
                    if n+1<len(heads):
                       # print n
                        #print heads[n]
                        self.arr[self.header_count,0,0]=heads[n]
                        #print c

                        specCount=0
                        self.spec_count[self.header_count]=specCount
                
                        while j<len(new):
                            key=1
                            if new[j]==heads[n+1]:
                                n=n+1
                                k=j-i
                                r=i+1
                    
                                if k>2:
                                    while r<j:
                                        self.arr[self.header_count,key,0]=new[r]
                                        self.arr[self.header_count,key,1]=new[r+1]
                                        self.arr[self.header_count,key+1,0]=0
                                        key+=1
                                        specCount+=1
                                        self.spec_count[self.header_count]=specCount
                                
                                        #print new[r]+":::"+new[r+1]
                                        r+=2
                                    break        
                                else:
                                    self.arr[self.header_count,key,0]=' '
                                    self.arr[self.header_count,key,1]=new[r]
                                    self.arr[self.header_count,key+1,0]=0
                                    specCount+=1
                                    self.spec_count[self.header_count]=specCount
                                    #print new[r]
                                    break
                    
                            else:
                                pass
                   
                            j+=1
         
                    self.header_count+=1            
                else:
                    pass
                i+=1
    def get_amazon_searchid(self):
            j=0
            while j<self.header_count:
                if self.arr[j,0,0]== 'GENERAL FEATURES' or self.arr[j,0,0]== 'GENERAL ':
                    i=0
                    self.model_id=''
                    self.model_name=''
                    self.model_part_number=''
                    
                    while self.arr[j,i,0]:
                    
                        if self.arr[j,i,0]=='Model ID':
                            self.model_id=self.arr[j,i,1]
                            print self.model_id
                        elif self.arr[j,i,0]=='Model Name':
                            self.model_name=self.arr[j,i,1]
                            print self.model_name
                        
                        elif self.arr[j,i,0]=='Part Number':
                            self.model_part_number=self.arr[j,i,1]
                            print self.model_part_number
                        i+=1
                        
                    break
                j+=1
    def fliptoamazonSearch(self):
        print self.title
        link = 'http://www.amazon.in/s/ref=nb_ss_gw/102-1882688-6100927?initialSearch=1&url=search-alias%3Daps&field-keywords='+self.title+"&Go.x=0&Go.y=0&Go=Go"
        page = requests.get(link)
        tree = html.fromstring(page.content)
    
        for elt in tree.xpath('//div[contains(@id,"atfResults")]//div[contains(@class,"a-column a-span12 a-text-center")]//a[contains(@class,"a-link-normal a-text-normal")]//img'):
                self.ama_img=elt.attrib['src']
                break
       
        for elt in tree.xpath('//div[contains(@id,"atfResults")]//div[contains(@class,"a-fixed-left-grid-col a-col-right")]//a[contains(@class,"a-link-normal s-access-detail-page  a-text-normal")]'):
                    self.ama_title=elt.attrib['title']
                    break
        
        
        amaz_price=tree.xpath('//div[contains(@id,"atfResults")]//div[contains(@class,"a-row")]//a[contains(@class,"a-link-normal a-text-normal")]//span[contains(@class,"a-size-base a-color-price s-price a-text-bold")]/text()')        
        self.ama_price=amaz_price[0]
       
        
        amaz_rating=tree.xpath('//div[contains(@id,"atfResults")]//div[contains(@class,"a-row")]//div[contains(@class,"a-column a-span5 a-span-last")]//span[contains(@class,"a-icon-alt")]/text()')
        self.ama_rating=amaz_rating[0]

        amaz_no_rating=tree.xpath('//div[contains(@id,"atfResults")]//div[contains(@class,"a-row")]//div[contains(@class,"a-column a-span5 a-span-last")]//a/text()')
        self.ama_no_rating=amaz_no_rating[0]
    def display_amazon_specs(self):
            url=self.ama_img
            data= requests.get(url).content
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(data)
            image = QtGui.QImage()
            image.loadFromData(data)
            self.lbl5 = QtGui.QLabel(self)
            mypixmap=QtGui.QPixmap(image)
            self.lbl5.resize(100,100)
            myScaledPixmap=mypixmap.scaled(self.lbl5.size(),QtCore.Qt.KeepAspectRatio)
            self.lbl5.setPixmap(myScaledPixmap)
            
            self.lbl5.move(550,150)
            self.lbl5.show()
 
            
            self.lbl6 =  QtGui.QLabel(self)
            

            self.lbl6.setText(self.ama_title)
            self.lbl6.setStyleSheet('QLabel {font: bold;font-size: 16pt; color: black;;}')
            self.lbl6.resize(500,160)
            self.lbl6.setWordWrap(True)
            self.lbl6.move(700,110)
            
            self.lbl6.show()

            self.lbl7 =  QtGui.QLabel(self)
            

            self.lbl7.setText(self.ama_price)
            self.lbl7.setStyleSheet('QLabel {font-size: 16pt; color: black;}')
            self.lbl7.resize(150,40)
            self.lbl7.move(750,260)
            
            self.lbl7.show()
            self.lbl8 =  QtGui.QLabel(self)    
            self.lbl8.setText("RATING:"+self.ama_rating)
            self.lbl8.setStyleSheet('QLabel {font-size: 16pt; color: black;}')
            self.lbl8.resize(450,120)
            self.lbl8.move(750,260)
            self.lbl8.show()
            self.lbl9 =  QtGui.QLabel(self)    
            self.lbl9.setText("Ratings Based on "+self.ama_no_rating)
            self.lbl9.setStyleSheet('QLabel {font-size: 16pt; color: black;}')
            self.lbl9.resize(450,120)
            self.lbl9.move(750,310)
            
            self.lbl9.show()
            try:
                self.cmpre_button.hide()
            except:
                pass
            
            self.button3 = QtGui.QPushButton('More Specifications..',self)
            self.button3.move(500,470)
            self.button3.resize(150,40)
            self.button3.clicked.connect(self.more_specs)
            self.button3.show()
            self.button4 = QtGui.QPushButton('Compare Products',self)
            self.button4.move(500,270)
            self.button4.resize(150,40)
            self.button4.clicked.connect(self.cmpre_products)
            self.button4.show()
            
    def more_specs(self):
        j=0
        p=0
        self.layout1 = QtGui.QGridLayout()
        
                
        self.table = QtGui.QTableWidget()
        self.table.setRowCount(120)
        self.table.setColumnCount(2)
        header = self.table.horizontalHeader()
        
        header.setStretchLastSection(True)
        while j<self.header_count:
            self.led = QtGui.QLineEdit(self.arr[j,0,0])
            
            self.layout1.addWidget(self.table, 1, 0)
            p+=1
            
            self.table.setItem(p,0, QtGui.QTableWidgetItem(self.led.text()))
            
            
            
                
            p+=1
           
            
            i=1
            while self.arr[j,i,0]!=0:
                self.led = QtGui.QLineEdit(self.arr[j,i,0])
                self.layout1.addWidget(self.table, 1, 0)
                self.table.setItem(p,0, QtGui.QTableWidgetItem(self.led.text()))
                self.led = QtGui.QLineEdit(self.arr[j,i,1])
                self.layout1.addWidget(self.table, 1, 0,1,1)
                self.table.setItem(p,1, QtGui.QTableWidgetItem(self.led.text()))
                
                p+=1
                
                
                i+=1
            j+=1
        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.show()
        self.setLayout(self.layout1)
    def cmpre_products(self):
        flipkart=0
        amazon=0
        amazon_price=self.ama_price.replace(',',"")
        flipK_price=self.ama_price.strip('Rs. ')
        flipK_price=self.ama_price.replace(',',"")
        a_price=float(amazon_price)
        f_price=float(flipK_price)
        print a_price
        print f_price
        if f_price<a_price:
            self.lbl2.setStyleSheet('QLabel {font-size: 18pt; color: white;}')
            flipkart+=1
        else:
            self.lbl7.setStyleSheet('QLabel {font-size: 18pt; color: white;}')
            amazon+=1
        print self.ama_rating
        ama_rating=self.ama_rating.strip(' out of 5 stars')
        a_rating=float(ama_rating)
        f_rating=float(self.flip_rating[0])
        if f_rating>a_rating:
            self.lbl3.setStyleSheet('QLabel {font-size: 18pt; color: white;}')
            flipkart+=1
        else:
            self.lbl8.setStyleSheet('QLabel {font-size: 18pt; color: white;}')
            amazon+=1
        print self.flip_no_rating[1]
        flipkart_rating=self.flip_no_rating[1].replace(' ',"")
        flipkart_rating=flipkart_rating.replace(',',"")
        flipkart_rating=flipkart_rating.strip("Basedon")
        flipkart_rating=flipkart_rating.strip("rating")
        f_no_rating=float(flipkart_rating)
        print f_no_rating
        self.ama_no_rating=self.ama_no_rating.replace(',','')
        a_no_rating=float(self.ama_no_rating)
        print a_no_rating
        if f_no_rating>a_no_rating:
            self.lbl4.setStyleSheet('QLabel {font-size: 18pt; color: white;}')
            flipkart+=1
        else:
            self.lbl9.setStyleSheet('QLabel {font-size: 18pt; color: white;}')
            amazon+=1
        print amazon
        print flipkart
        if amazon>flipkart:
            self.lbl10 =  QtGui.QLabel(self)    
            self.lbl10.setText("OUR SUGGESTION :AMAZON")
            self.lbl10.setStyleSheet('QLabel {font:bold;font-size: 24pt; color: white;}')
            self.lbl10.resize(680,120)
            self.lbl10.move(680,470)
            self.lbl10.show()
        else:
            self.lbl10 =  QtGui.QLabel(self)    
            self.lbl10.setText("OUR SUGGESTION :FLIPKART")
            self.lbl10.setStyleSheet('QLabel {font:bold;font-size: 24pt; color: white;}')
            self.lbl10.resize(680,120)
            self.lbl10.move(680,470)
            self.lbl10.show()
        
def run():    
    app=QtGui.QApplication([])
    GUI = Window()
    sys.exit(app.exec_())

run()

        
