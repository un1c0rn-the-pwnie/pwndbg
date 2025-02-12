import pwndbg.color.theme as theme
import pwndbg.gdblib.vmmap
from pwndbg.color import generateColorFunction
from pwndbg.color import normal
from pwndbg.gdblib import config

config_stack = theme.add_color_param("memory-stack-color", "yellow", "color for stack memory")
config_heap = theme.add_color_param("memory-heap-color", "blue", "color for heap memory")
config_code = theme.add_color_param("memory-code-color", "red", "color for executable memory")
config_data = theme.add_color_param(
    "memory-data-color", "purple", "color for all other writable memory"
)
config_rodata = theme.add_color_param(
    "memory-rodata-color", "normal", "color for all read only memory"
)
config_rwx = theme.add_color_param("memory-rwx-color", "underline", "color added to all RWX memory")


def stack(x):
    return generateColorFunction(config.memory_stack_color)(x)


def heap(x):
    return generateColorFunction(config.memory_heap_color)(x)


def code(x):
    return generateColorFunction(config.memory_code_color)(x)


def data(x):
    return generateColorFunction(config.memory_data_color)(x)


def rodata(x):
    return generateColorFunction(config.memory_rodata_color)(x)


def rwx(x):
    return generateColorFunction(config.memory_rwx_color)(x)


def get(address, text=None):
    """
    Returns a colorized string representing the provided address.

    Arguments:
        address(int): Address to look up
        text(str): Optional text to use in place of the address
              in the return value string.
    """
    address = int(address)

    page = pwndbg.gdblib.vmmap.find(int(address))

    if page is None:
        color = normal
    elif "[stack" in page.objfile:
        color = stack
    elif "[heap" in page.objfile:
        color = heap
    elif page.execute:
        color = code
    elif page.rw:
        color = data
    else:
        color = rodata

    if page and page.rwx:
        old_color = color
        color = lambda x: rwx(old_color(x))

    if text is None and isinstance(address, int) and address > 255:
        text = hex(int(address))
    if text is None:
        text = str(int(address))

    return color(text)


def legend():
    return "LEGEND: " + " | ".join(
        (stack("STACK"), heap("HEAP"), code("CODE"), data("DATA"), rwx("RWX"), rodata("RODATA"))
    )
