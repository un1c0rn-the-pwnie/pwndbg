import pwndbg.color.theme as theme
from pwndbg.color import generateColorFunction
from pwndbg.gdblib import config

config_arrow_color = theme.add_color_param(
    "chain-arrow-color", "normal", "color of chain formatting (arrow)"
)
config_contiguous_color = theme.add_color_param(
    "chain-contiguous-marker-color", "normal", "color of chain formatting (contiguous marker)"
)


def arrow(x):
    return generateColorFunction(config.chain_arrow_color)(x)


def contiguous(x):
    return generateColorFunction(config.chain_contiguous_marker_color)(x)
