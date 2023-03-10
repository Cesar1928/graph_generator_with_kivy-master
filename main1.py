import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, MDList
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.navigationdrawer import MDNavigationLayout
from kivy.factory import Factory
from kivy.properties import StringProperty, ListProperty
import webbrowser
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas, NavigationToolbar2Kivy, FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from kivy.properties import NumericProperty
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.metrics import r2_score

       
class ui(ScreenManager):
    pass

class main(MDApp):

    def build(self):
        Builder.load_file("main.kv")
        return ui()

    def gnrt_graph(self):
        
            fr = float (self.root.ids.fr.text) 
            b = float (self.root.ids.b.text)
            s = float (self.root.ids.s.text)
            h = float (self.root.ids.h.text)
            Desv = float (self.root.ids.Desv.text)
            t = float (self.root.ids.t.text)
            d = float (self.root.ids.d.text)
            sp = float (self.root.ids.sp.text)
            de = float (self.root.ids.de.text)
            rws = float (self.root.ids.rws.text)

            lc = h+sp- t
            w = de * lc *3.1416*d**2/2
            V= b*s*h
                
            Xprom = fr*((V/w)**0.8)*(w**(1/6))*(115/rws)**(19/30)
            
            n = 2.2-14*(b/d)*(((1+s/b)/2)**0.5)*(1-Desv/b)*(lc/h)
            
            paso1 =5
            p=np.arange(5,95+paso1,paso1)/100 
            
            Xc = Xprom / (0.693**(1/n))
            
            X = Xc * ((- (np.log(1-p)))**(1/n))
                        
            X80 = Xc * ((- (np.log(0.2)))**(1/n))      
            
            plt.xlabel('Tamaño frag.(m)', fontsize=10)
            plt.ylabel('Retención (%)', fontsize = 7)
            plt.grid(True, color='lightgray')

            #plt.subplot(2,2,3)
            plt.axhline(y=80, color="r", ls ="--") 
            plt.axvline(x=X80, color = "r", ls="--")
            plt.text (0.10,50,'Gráfica', color="r", fontsize=10)
        
            plt.title ('Predicción Fragmentación', fontsize=15,color='blue')
            plt.plot(X,p*100, label = 'Valores')        

         
            # fig, ax = plt.subplots()    
            self.bx = self.root.ids.bx
                                           
            return self.bx.add_widget(FigureCanvasKivyAgg(plt.gcf()))


    def limpiar(self):
        self.root.ids.fr.text =""
        self.root.ids.b.text =""
        self.root.ids.s.text =""
        self.root.ids.h.text =""
        self.root.ids.Desv.text=""
        self.root.ids.t.text =""
        self.root.ids.d.text=""
        self.root.ids.sp.text=""
        self.root.ids.de.text=""
        self.root.ids.rws.text=""
        return self.bx.add_widget(FigureCanvasKivyAgg(plt.clf()))
    
    def atenua (self):
        v1 = float (self.root.ids.v1.text) 
        v2 = float (self.root.ids.v2.text) 
        v3 = float (self.root.ids.v3.text) 
        v4 = float (self.root.ids.v4.text) 
        v5 = float (self.root.ids.v5.text) 
        v6 = float (self.root.ids.v6.text) 
        v7 = float (self.root.ids.v7.text) 
               
        d1 = float (self.root.ids.d1.text) 
        d2 = float (self.root.ids.d2.text) 
        d3 = float (self.root.ids.d3.text) 
        d4 = float (self.root.ids.d4.text) 
        d5 = float (self.root.ids.d5.text) 
        d6 = float (self.root.ids.d6.text) 
        d7 = float (self.root.ids.d7.text) 
       
        k1 = float (self.root.ids.k1.text) 
        k2 = float (self.root.ids.k2.text) 
        k3 = float (self.root.ids.k3.text) 
        k4 = float (self.root.ids.k4.text) 
        k5 = float (self.root.ids.k5.text) 
        k6 = float (self.root.ids.k6.text) 
        k7 = float (self.root.ids.k7.text) 
      
        K1 = float (self.root.ids.K1.text) 
        D1 = float (self.root.ids.D1.text) 
        p = float (self.root.ids.C1.text) 
               
        reg = linear_model.LinearRegression()

        df1 = pd.DataFrame({"veloci":[v1,v2,v3,v4,v5,v6,v7], "dista":[d1,d2,d3,d4,d5,d6,d7],"carga":[k1,k2,k3,k4,k5,k6,k7]})
        df2 = (df1["dista"])/((df1["carga"])**(1/2))
        df3 = pd.DataFrame({"sd":df2})
        
        x1 = df3 ["sd"]
        y1 = df1 ["veloci"]

        XX = x1[:,np.newaxis]
        YY = y1[:,np.newaxis]

        #Convertir los datos a parametros logaritmicos
        x = df3["sd"].apply(lambda x1: np.log10(x1))
        y = df1["veloci"].apply(lambda y1: np.log10(y1))

        Y = y[:,np.newaxis]
        X = x[:,np.newaxis]
       
        print (regr.fit(X,y))

        # calcular la pendiente y punto de corte en el eje 
        m = regr.coef_[0]
        b = regr.intercept_

        #calcular parametros para error tipico
        Y2 = df1["veloci"].apply(lambda y1: (np.log10(y1))**2)
        xy = X * Y

        Y21 = Y2.sum()
        y1 = Y.sum()
        xy1= xy.sum()
        n = 7 # cantidad de datos scatter

        error = (((Y21-(b*y1)-(m*xy1))/(n-2))**(1/2))

        # ahora sacar el nuevo K en función a porcentaje de confianza 50%
        k = 10**b
        k1=round(k,4)
        self.root.ids.KN1.text= str (k1)
        
        alf = m 
        
        self.root.ids.alfa.text= str (alf)

        y_p1 = k * (XX**alf)  # el vpp con confianza de 50%

        #ahora sacar el nuevo K en función a porcentaje de confianza 85%
        f1 = np.log10(k)
        
        f2 = norm.ppf(p)
        ka = 10**(f1+f2*error)
        ka1= round(ka,4)
        self.root.ids.KN2.text= str (ka1)
        y_p2 = ka * (XX**alf) # el vpp con confianza de 85%

        # para sacar las vibraciones con el ka
        z = D1/(K1**(1/2))
        yc = ka*((z)**alf)
        yc1 = round(yc, 3)
        self.root.ids.V1.text= str (yc1)

        print(regr.predict(XX)[0:5])
        r2 = r2_score(YY,y_p2)
        print("el valor de r2:",r2_score(YY,y_p2))

        
        #ax1 = plt.subplot(1,2,1)
               
        plt.scatter(XX,YY,color="blue")
        plt.plot(XX,y_p1,color="red")
        plt.plot(XX,y_p2,color="green")
        plt.title("LEY DE ATENUACIÓN VPP", fontsize=11)
        plt.xlabel("SD (Distancia/Raíz(Carga))",fontsize=8)
        plt.ylabel ("VPP", fontsize=8)
        
        self.bx1 = self.root.ids.bx1            
        return self.bx1.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def limpiar1(self):
        self.root.ids.v1.text =""
        self.root.ids.v2.text =""
        self.root.ids.v3.text =""
        self.root.ids.v4.text =""
        self.root.ids.v5.text =""
        self.root.ids.v6.text =""
        self.root.ids.v7.text =""
        self.root.ids.d1.text =""
        self.root.ids.d2.text =""
        self.root.ids.d3.text =""
        self.root.ids.d4.text =""
        self.root.ids.d5.text =""
        self.root.ids.d6.text =""
        self.root.ids.d7.text =""
        self.root.ids.k1.text =""
        self.root.ids.k2.text =""
        self.root.ids.k3.text =""
        self.root.ids.k4.text =""
        self.root.ids.k5.text =""
        self.root.ids.k6.text =""
        self.root.ids.k7.text =""

        
        self.root.ids.K1.text =""
        self.root.ids.D1.text =""
        self.root.ids.V1.text =""
        self.root.ids.KN1.text =""
        self.root.ids.KN2.text =""
        self.root.ids.alfa.text =""
        self.root.ids.C1.text =""
        return self.bx1.add_widget(FigureCanvasKivyAgg(plt.clf()))

if __name__ == "__main__":
    main().run()
