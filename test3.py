from functools import partial

from bokeh.core.properties import value
from bokeh.io import curdoc, show
from bokeh.layouts import layout
from bokeh.layouts import widgetbox as wb
from bokeh.models import widgets as wd
from bokeh.models.widgets import Button, Paragraph, Slider

import time
import re
import serial

# ardunio connection
## TODO: change port
USB_PORT = 'COM3'
ARDUINO_DATA = serial.Serial(USB_PORT,9600)


# boat sail
SAIL_LABEL = 'SAIL'

slider_sail = Slider(start=0, end=180, value=0, step=.1, title=SAIL_LABEL)

# boat rudder
RUDDER_LABEL = 'RUDDER'

slider_rudder = Slider(start=0, end=180, value=0, step=.1, title=RUDDER_LABEL)

# Refresh the value
btn_refresh = Button(label="Refresh")

# Get call back
def onClick(idx=-1, name=None):
    print('onClick: ', name, idx)


def onChange(attr, old, new, name=None):
    print("onChange: {}:{}".format(name, new))


# Send to ardunio
def sendCommand(attr, old, new, name=None):
    val = new
    search_sail = re.search( r'Sail', name, re.M|re.I)
    if search_sail:
        # servo = 'Sail'
        val = new
    search_rudder = re.search( r'Rudder', name, re.M|re.I)
    if search_rudder:
        # servo = 'Rudder'
        val = new + 360
    ARDUINO_DATA.write(b'%.2f'%val)
    # time.sleep(5.0)           # May not required?
    print("Send command from {} successfully.".format(name))


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
