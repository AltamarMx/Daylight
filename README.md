# Utilities to calculate Usefull Daylight Illumination, illuminance maps for a ILL file from Radiance

Ill file is an output from Radiance with a lot of data. Methods to calculate the
Usefull Daylight Iluminance, illuminance map, illuminance along a direction, are implemented to
visualize results.

A jupyter notebook is provided with a typical output file.
## Getting Started  

Download the notebook using-UDI.ipynb, an example of each method is used.
The file Illumination.py must be saved in the folder "modulos" and the ill  file into the folder "data".


### Prerequisites



```
Pandas
Matplotlib
Numpy
Ipywidgets
```

### Using

from modulos import Eplus as ep
from bokeh.plotting import figure, output_file, show
from bokeh.io import output_notebook
output_notebook()


a = ill.daylight('data/cubo_map.ill')

print(a.__doc__)

a.udi()

a.map()

a.x()

a.y()



    udi()
        Calculate the UDI [https://patternguide.advancedbuildings.net/using-this-guide/analysis-methods/useful-daylight-illuminance]
        when defining the following parameters:
        E_LL:  Lower limit illumination level [lx]
        E_UL:  Upper limit illumination level [lx]
        t_min: Start hour of day to evaluate the UDI [h]
        t_http://localhost:8891/edit/modulos/illumination.py#max: End hout of day to evaluate the UDI [h]
        dC:    Number of color leves for the UDI [-]
        Once executed, prints the frequency of visual comfort (FVC).

        
        
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
    fvc()
        Frequency of visual comfort (average of the UDI_useful)





## Authors

* **Guillermo Barrios** - *Initial work* - [GEE-UNAM](https://github.com/Altamar)
* **Maximiliano Valdez** - *Spiritual leadership* - [IER-UNAM](https://github.com/garaged)

## License

This project is licensed under ...

## Acknowledgments

* Requests and suggestions are welcomed.
