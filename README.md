# Utilities to calculate Usefull Daylight Illumination, illuminance maps for a ILL file from Radiance

Ill file is an output from Radiance with a lot of data. Methods to calculate the
Usefull Daylight Iluminance, illuminance map, illuminance along a direction, are implemented to
visualize results.

A jupyter notebook is provided with typical output file.
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


nombres = ['t','Ein','Eout', 'Nin','Nout', 'Oin','Oout', 'Sin','Sout', 'Pin','Pout','Tein','Teout']
caso1 = ep.readEP('datos/cubo.csv',nombres)

caso1.datos.columns

p = figure(plot_width=900, plot_height=500,x_axis_type='datetime',
           toolbar_location="above")
formato de inicio y fin   YYYY-MM-DD
inicio = '2017-04-06'
fin    = '2017-04-07'

q = caso1.datos[inicio:fin]

p.line(q.index,q.Ein,color='blue',legend='Ei')
p.line(q.index,q.Eout,color='red',legend='Eout')
p.line(q.index,q.Pin,color='black',legend='Pi')
p.line(q.index,q.Pout,color='brown',legend='Pout')
show(p)


## Authors

* **Guillermo Barrios** - *Initial work* - [GEE-UNAM](https://github.com/Altamar)
* **Maximiliano Valdez** - *Spiritual leadership* - [IER-UNAM](https://github.com/garaged)

## License

This project is licensed under ...

## Acknowledgments

* Requests are welcomed
