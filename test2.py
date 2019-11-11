from functools import partial

from bokeh.core.properties import value
from bokeh.io import curdoc, show
from bokeh.layouts import layout
from bokeh.layouts import widgetbox as wb
# from bokeh.models import ColumnDataSource
# from bokeh.models import CustomJS
from bokeh.models import widgets as wd
from bokeh.models.widgets import Button, Paragraph, Slider

from pyfirmata import Arduino, util
import time
import re
import serial

# # ardunio connection
# ## TODO: change port
USB_port = 'COM3'
# board = Arduino(USB_port)
arduino_data = serial.Serial(USB_port,9600)

# iterator = util.Iterator(board)
# iterator.start()


# boat sail
sail_label = 'SAIL'

slider_sail = Slider(start=0, end=360, value=0, step=.1, title=sail_label)

# boat rudder
rudder_label = 'RUDDER'

slider_rudder = Slider(start=0, end=360, value=0, step=.1, title=rudder_label)

# Refresh the value
btnRefresh = Button(label="Refresh")

# Get call back
def onClick(idx=-1, name=None):
    print('onClick: ', name, idx)


def onChange(attr, old, new, name=None):
    print("onChange: {}:{}".format(name, new))


# # Send to ardunio

def sendCommand(attr, old, new, name=None):
    val = new
    search_sail = re.search( r'Sail', name, re.M|re.I)
    if search_sail:
        servo = 'Sail'
    search_rudder = re.search( r'Rudder', name, re.M|re.I)
    if search_rudder:
        servo = 'Rudder'
    arduino_data.write([val, servo])
    time.sleep(5.0)

# def onChangeCallBack(attr, old, new, name=None):
#     global board
#     val = new
#     ## TODO: which pin to use
#     search_sail = re.search( r'Sail', name, re.M|re.I)
#     if search_sail:
#         command = board.get_pin('::o')
#         command.write(val)
#     search_rudder = re.search( r'Rudder', name, re.M|re.I)
#     if search_rudder:
#         command = board.get_pin('::o')
#         command.write(val)
#     # time.sleep(1.0)


slider_sail.on_change("value", partial(onChange, name="Silder Sail"))
slider_sail.on_change("value", partial(sendCommand, name="Silder Sail"))

slider_rudder.on_change("value", partial(onChange, name="Silder Rudder"))
slider_rudder.on_change("value", partial(sendCommand, name="Silder Rudder"))

# Layout
# TODO:eidit layout
boat_control = layout(
    [
        [wb(slider_sail, width=1000)],
        [wb(slider_rudder, width=1000)]
    ]
)

# Create page
page = wd.Panel(child=boat_control, title="Boat Control")
tab = wd.Tabs(tabs=[page])

curdoc().add_root(tab)
