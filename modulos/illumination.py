import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
get_ipython().magic('matplotlib inline')
from ipywidgets import widgets,interact_manual,interact
import math


class daylight:
    """
    Class to read ILL files from a Radiance Simulation, calculate and render UDIs, illuminance maps and others.

    Use:
    ill(arg1)

    Parameters
    ----------
    arg1 : path of the ILL file to load into a DataFrame.
        arg1 = 'data/CEEA.ill'
    Returns
    nx: number of elements in the x direction of the grid
    ny: number of elements in the y direction of the grid
    Lx: Lenght in the x direction of the grid
    Ly: Lenght in the y direction of the grid
    dx: Size of the grid in the x direction
    dy: Size of the grid in the y direction
    -------
    The class contains the following methods:
    udi()
        Calculate the UDI [https://patternguide.advancedbuildings.net/using-this-guide/analysis-methods/useful-daylight-illuminance]
        when defining the following parameters:
        E_LL:  Lower limit illumination level [lx]
        E_UL:  Upper limit illumination level [lx]
        t_min: Start hour of day to evaluate the UDI [h]
        t_max: End hout of day to evaluate the UDI [h]
        dC:    Number of color leves for the UDI [-]
        
    map()
        Plot the illuminance map for the space for a specific day, time and renders using a maximum value of the illuminance:
        day:  day to plot the illuminance map [-]
        hour: Time of day (0,24) to plot the illuminance map [h]
        Lmax: Maximum value to render illuminance map [lx]
    
    x()
        Plot the illuminance along the x direction at a specific value of y:
        day:  day to plot the illuminance along the x direction [-]
        hour: Time of day (0,24) to plot the illuminance along the x direction [h]
        jj:   Number of element (0,Ly) to plot the illuminance along the x direcion [-]
        
    
    y()
        Plot the illuminance along the y direction at a specific value of x:
        day:  day to plot the illuminance along the x direction [-]
        hour: Time of day (0,24) to plot the illuminance along the y direction [h]
        ii:   Number of element (0,Lx) to plot the illuminance along the y direcion [-]

    """

    def __init__(self,archivo):
        pd.set_option('precision',25)
        parameters = pd.read_csv(archivo,sep=' ',nrows=1,skiprows=(0,1,2),header=None)
        self.xmin   = parameters[0]
        self.ymin   = parameters[1]
        self.xmax   = parameters[3]
        self.ymax   = parameters[7]
        self.deltax = parameters[9]
        self.deltay = parameters[10]
        self.nx     = int(((self.xmax - self.xmin) / self.deltax ).round())
#         self.nx     = math.floor(((self.xmax - self.xmin) / self.deltax ))
        self.ny     = int(((self.ymax - self.ymin) / self.deltay).round())
#         self.ny     = math.floor(((self.ymax - self.ymin) / self.deltay))
        ill = pd.read_csv(archivo,sep=',',skiprows=(0,1,2,3),header=None)
        dias, _ = ill.shape
        self.dias = int(dias/24)
        self.renglones, self.cols = ill.shape
        self.columnas = np.arange(6,self.cols)
        self.ill_data = ill[self.columnas]
        print("nx: {}".format(self.nx))
        print("ny: {}".format(self.ny))
        print("Lx: {:.2f} [m]".format(self.xmax[0]-self.xmin[0]))
        print("Ly: {:.2f} [m]".format(self.ymax[0]-self.ymin[0]))
        print("dx: {:.2f} [m]".format(self.deltax[0]))
        print("dy: {:.2f} [m]".format(self.deltay[0]))

    def UDI(self,E_LL,E_UL,t_min,t_max,dC):
        dC =  dC + 1
        result = pd.DataFrame()
        for d in range(0,self.dias):
            min = (d+1)*24-(24-t_min)
            max = (d+1)*24-(24-t_max)
            result = result.append(self.ill_data.iloc[min-1:max-1])
        renglones, cols = result.shape
        UDI_sub = np.zeros(len(self.columnas))
        UDI_u   = np.zeros(len(self.columnas))
        UDI_sob = np.zeros(len(self.columnas))

        for i in range(renglones):
            f = result.iloc[i] < E_LL
            UDI_sub[f] = (UDI_sub[f] + 1)
            f = (result.iloc[i] >= E_LL) & (result.iloc[i] <= E_UL)
            UDI_u[f] =( UDI_u[f] + 1)
            f = result.iloc[i] > E_UL
            UDI_sob[f] = (UDI_sob[f] + 1)

        UDI_sub = (UDI_sub /((t_max-t_min)*self.dias)*100).reshape(self.ny,self.nx)
        UDI_u   = (UDI_u   /((t_max-t_min)*self.dias)*100).reshape(self.ny,self.nx)
        UDI_sob = (UDI_sob /((t_max-t_min)*self.dias)*100).reshape(self.ny,self.nx)

    #GRAFICADO DE LOS UDISself.
        fig = plt.figure(figsize=(10,8))
        levels = np.linspace(0,100,dC)
        x = np.linspace(self.xmin,self.xmax,self.nx)
        y = np.linspace(self.ymin,self.ymax,self.ny)
        ax1 = fig.add_subplot(231)    
        plt.xlabel('$x$ $[m]$')
        plt.ylabel('$y$ $[m]$')
        plt.title('$UDI_{sub}$')
        plt.set_cmap('gist_heat')
        plt.set_cmap('gnuplot')
        
        z_contourR = ax1.contourf(x,y,UDI_sub,levels=levels)
        cbarR = plt.colorbar(z_contourR,ticks=np.linspace(0,100,6))
        ax2 = fig.add_subplot(232)
        plt.title('$UDI_u$')
        z_contourI = ax2.contourf(x,y,UDI_u,levels=levels)
        cbarI = plt.colorbar(z_contourI,ticks=np.linspace(0,100,6))
        ax3 = fig.add_subplot(233)
        plt.title('$UDI_{sob}$')
        z_contourJ = ax3.contourf(x,y,UDI_sob,levels=levels)
        cbarI = plt.colorbar(z_contourJ,ticks=np.linspace(0,100,6))
        plt.tight_layout()
        plt.show()
        print("FCV = {:.2}%".format(np.average(UDI_u)) )
        

        
    def udi(self):
        interact_manual(self.UDI,
                 E_LL=widgets.IntSlider(min=50,max=1000,step=50,value=300),
                 E_UL=widgets.IntSlider(min=500,max=2500,step=50,value=1500),
                 t_min=widgets.IntSlider(min=6,max=12,step=1,value=8),
                 t_max=widgets.IntSlider(min=12,max=20,step=1,value=18),
                 dC=widgets.IntSlider(min=5,max=50,step=5,value=5))
          
  
    def MAP(self,dia,hora,Lmax):
        position = (dia-1)*24-(24-hora-1)
        mapa = self.ill_data.iloc[position].values.reshape(self.ny,self.nx)
        fig = plt.figure(figsize=(10,8))
        levels = np.linspace(0,Lmax,50)
        x = np.linspace(self.xmin,self.xmax,self.nx)
        y = np.linspace(self.ymin,self.ymax,self.ny)
        ax1 = fig.add_subplot(111)    
        plt.xlabel('$x$ $[m]$')
        plt.ylabel('$y$ $[m]$')
        plt.title('Illuminance $[lx]$')
        plt.set_cmap('gist_heat')
        plt.set_cmap('gnuplot')
        
        z_contourR = ax1.contourf(x,y,mapa,levels=levels)
        cbarR = plt.colorbar(z_contourR,ticks=np.linspace(0,Lmax,6))
        plt.show()
        
    def X(self,dia,hora,jj):
        position = (dia-1)*24-(24-hora-1)
        mapa = self.ill_data.iloc[position].values.reshape(self.ny,self.nx)
#         print(jj*self.deltay+self.deltay/2.)
        x = np.linspace(self.xmin,self.xmax,self.nx)
        ymax = self.ymax - self.ymin + jj*self.deltay + self.deltay/2.
#         print(ymax)
        y = np.linspace(self.ymin,self.ymax,self.ny)
        print("y ={:.2f} [m]".format(y[jj]))
        fig = plt.figure(figsize=(10,2))
        ax1 = fig.add_subplot(111)    
        plt.xlabel('$x$ $[m]$')
        plt.ylabel('Illuminance $[lx]$')
        
        x_plot = ax1.plot(x,mapa[jj,:])
        x_plot = ax1.scatter(x,mapa[jj,:])
        plt.show()
        print('#x\tIl')
        print('#[m]\t[lx]')
        for i in range(len(x)):
            print("{:.2f}\t{:.2f}".format(x[i],mapa[jj,i])) 
      
   
        
    def y(self):
        interact_manual(self.Y,
                 dia=widgets.IntSlider(min=1,max=365,step=1,value=180),
                 hora=widgets.IntSlider(min=0,max=23,step=1,value=12),
                 ii=widgets.IntSlider(min=0,max=self.nx-1,step=1,value=0))
    def Y(self,dia,hora,ii):
        position = (dia-1)*24-(24-hora-1)
        mapa = self.ill_data.iloc[position].values.reshape(self.ny,self.nx)
#         print(ii*self.deltax + self.deltax/2.)
        y = np.linspace(self.ymin,self.ymax,self.ny)
        x = np.linspace(self.xmin,self.xmax,self.nx)
        print("x ={:.2f} [m]".format(x[ii]))
        fig = plt.figure(figsize=(10,2))
        ax1 = fig.add_subplot(111)    
        plt.xlabel('$y$ $[m]$')
        plt.ylabel('Illuminance $[lx]$')
#         mapa = np.transpose(mapa)
        x_plot = ax1.plot(y,mapa[:,ii])
        x_plot = ax1.scatter(y,mapa[:,ii])
        plt.show()
        print('#y\tIl')
        print('#[m]\t[lx]')
        for i in range(len(y)):
            print("{:.2f}\t{:.2f}".format(y[i],mapa[i,ii])) 
        
        
    def x(self):
        interact_manual(self.X,
                 dia=widgets.IntSlider(min=1,max=365,step=1,value=180),
                 hora=widgets.IntSlider(min=0,max=23,step=1,value=12),
                 jj=widgets.IntSlider(min=0,max=self.ny-1,step=1,value=0))
        
    def map(self):
        interact_manual(self.MAP,
                 dia=widgets.IntSlider(min=1,max=365,step=1,value=180),
                 hora=widgets.IntSlider(min=6,max=20,step=1,value=12),
                 Lmax=widgets.IntSlider(min=0,max=35000,step=100,value=5000))
        
