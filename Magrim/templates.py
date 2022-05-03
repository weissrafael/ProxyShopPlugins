"""
MAGRIM'S TEMPLATES
"""

import os
import proxyshop.templates as temp
import proxyshop.text_layers as txt_layers
from proxyshop import format_text, gui
import proxyshop.constants as con
from proxyshop.settings import cfg
import proxyshop.helpers as psd
from photoshop import api as ps
from proxyshop.constants import con
app = ps.Application()
console = gui.console_handler

# Ensure scaling with pixels, font size with points
app.preferences.rulerUnits = ps.Units.Pixels
app.preferences.typeUnits = ps.Units.Points

def rgb_black():
    color = ps.SolidColor()
    color.rgb.red = 0
    color.rgb.green = 0
    color.rgb.blue = 0
    return color

def rgb_white():
    color = ps.SolidColor()
    color.rgb.red = 255
    color.rgb.green = 255
    color.rgb.blue = 255
    return color

def rgb_gold():
    color = ps.SolidColor()
    color.rgb.red = 255
    color.rgb.green = 223
    color.rgb.blue = 138
    return color

class PhyrexianWithFontTemplate (temp.NormalTemplate):
    """
     * From the Phyrexian secret lair promo with phyrexian font
    """
    def __init__ (self, layout, file):
        con.font_name_mplantin = "Phi_horizontal_gbrsh_9.8"
        super().__init__(layout, file)

    def template_file_name (self):
        return "Magrim/phyrexian-with-phyrexian-font"

    def template_suffix (self):
        return "Phyrexian With Font"

    def enable_frame_layers (self):
        # PT Box, no title boxes for this one
        if self.is_creature:
            psd.getLayer(self.layout.twins, con.layers['PT_BOX']).visible = True
        else: psd.getLayerSet(con.layers['PT_BOX']).visible = False

        # Pinlines
        if self.is_land:
            # Land Group
            psd.getLayer(self.layout.pinlines, con.layers['LAND_PINLINES_TEXTBOX']).visible = True
        else:
            # Nonland
            psd.getLayer(self.layout.pinlines, con.layers['PINLINES_TEXTBOX']).visible = True


class MinimalistTemplate (temp.NormalTemplate):
    """
     * Daniel's Minimalist Template
    """
    def template_file_name (self):
        return "Magrim/minimalist"

    def template_suffix (self):
        return "Minimalist"

    def basic_text_layers(self, text_and_icons):
        psd.getLayer(con.layers['TYPE_LINE_SHIFT'], text_and_icons).textItem.color = rgb_gold()
        psd.getLayer(con.layers['TYPE_LINE'], text_and_icons).textItem.color = rgb_gold()
        super().basic_text_layers(text_and_icons)

    def rules_text_and_pt_layers (self, text_and_icons):
        color = rgb_white()
        psd.getLayer(con.layers['RULES_TEXT_CREATURE'], text_and_icons).textItem.color = color
        super().rules_text_and_pt_layers(text_and_icons)

    # def enable_frame_layers (self):
    #     text_and_icons = psd.getLayerSet(con.layers['TEXT_AND_ICONS'])
    #     color = rgb_gold()
    #     if self.layout.twins == "W":
    #         color = rgb_gold()
    #     psd.getLayer(con.layers['TYPE_LINE'], text_and_icons).textItem.color = color


class ClassicBorderlessTemplate (temp.NormalClassicTemplate):
    """
     * Identical to NormalClassic
     * Border removed and art size adjusted
    """
    def template_file_name (self):
        return "Magrim/normal-classic-borderless"

    def template_suffix (self):
        return "Classic Borderless"


class ClassicTextlessTemplate (temp.NormalTemplate):
    """
     * Identical to NormalClassic
     * But full art textless
    """
    def template_file_name (self):
        return "Magrim/classic-textless"

    def template_suffix (self):
        return "Classic Textless"

    def rules_text_and_pt_layers (self, text_and_icons):
        if self.is_creature:
            # Creature card - set up creature layer for rules text and insert p/t
            power_toughness = psd.getLayer(con.layers['POWER_TOUGHNESS'], text_and_icons)
            rules_text = psd.getLayer(con.layers['RULES_TEXT_CREATURE'], text_and_icons)
            rules_text.visible = False
            self.tx_layers.extend([
                txt_layers.TextField(
                    layer = power_toughness,
                    text_contents = str(self.layout.power) + "/" + str(self.layout.toughness),
                    text_color = psd.get_text_layer_color(power_toughness)
                )
            ])
        else:
            # Noncreature card - use the normal rules text layer and disable the p/t layer
            psd.getLayer(con.layers['POWER_TOUGHNESS'], text_and_icons).visible = False

    def enable_frame_layers (self):
        # PT Box, no title boxes for this one
        psd.getLayerSet(con.layers['PT_BOX']).visible = False
        if self.is_creature:
            text_and_icons = psd.getLayerSet(con.layers['TEXT_AND_ICONS'])
            pt_box_reference = psd.getLayer("PT Box Reference", text_and_icons)
            type_line = psd.getLayer(con.layers['TYPE_LINE'], text_and_icons)
            self.tx_layers.extend([
                txt_layers.ScaledTextField(
                    layer = type_line,
                    text_contents = self.layout.type_line,
                    text_color = psd.get_text_layer_color(type_line),
                    reference_layer = pt_box_reference
                ),
            ])
            pt_box_reference.visible = False
            # Check if vehicle
            if "Vehicle" in self.layout.type_line:
                psd.getLayer("Vehicle", con.layers['PT_BOX']).visible = True
            else: psd.getLayer(self.layout.twins, con.layers['PT_BOX']).visible = True
        else: psd.getLayerSet(con.layers['PT_BOX']).visible = False

        # Land or not?
        if self.is_land: pinlines = psd.getLayerSet(con.layers['LAND_PINLINES_TEXTBOX'])
        else: pinlines = psd.getLayerSet(con.layers['PINLINES_TEXTBOX'])

        # Check if vehicle
        if self.layout.type_line.find("Vehicle") >= 0: psd.getLayer("Vehicle", pinlines).visible = True
        else: psd.getLayer(self.layout.pinlines, pinlines).visible = True
        psd.getLayerSet(con.layers['PT_BOX']).visible = False


class KhaldeimTextlessTemplate (temp.NormalTemplate):
    """
     * Identical to NormalClassic
     * Border removed and art size adjusted
    """
    def template_file_name (self):
        return "Magrim/kaldheim-textless"

    def template_suffix (self):
        return "Kaldheim Textless"

    def rules_text_and_pt_layers (self, text_and_icons):
        if self.is_creature:
            # Creature card - set up creature layer for rules text and insert p/t
            power_toughness = psd.getLayer(con.layers['POWER_TOUGHNESS'], text_and_icons)
            rules_text = psd.getLayer(con.layers['RULES_TEXT_CREATURE'], text_and_icons)
            rules_text.visible = False
            self.tx_layers.extend([
                txt_layers.TextField(
                    layer = power_toughness,
                    text_contents = str(self.layout.power) + "/" + str(self.layout.toughness),
                    text_color = psd.get_text_layer_color(power_toughness)
                )
            ])
        else:
            # Noncreature card - use the normal rules text layer and disable the p/t layer
            psd.getLayer(con.layers['POWER_TOUGHNESS'], text_and_icons).visible = False

    def enable_frame_layers (self):
        # PT Box, no title boxes for this one
        if self.is_creature:
            text_and_icons = psd.getLayerSet(con.layers['TEXT_AND_ICONS'])
            pt_box_reference = psd.getLayer("PT Box Reference", text_and_icons)
            type_line = psd.getLayer(con.layers['TYPE_LINE'], text_and_icons)
            self.tx_layers.extend([
                txt_layers.ScaledTextField(
                    layer = type_line,
                    text_contents = self.layout.type_line,
                    text_color = psd.get_text_layer_color(type_line),
                    reference_layer = pt_box_reference
                ),
            ])
            pt_box_reference.visible = False
            # Check if vehicle
            if "Vehicle" in self.layout.type_line:
                psd.getLayer("Vehicle", con.layers['PT_BOX']).visible = True
            else: psd.getLayer(self.layout.twins, con.layers['PT_BOX']).visible = True
        else: psd.getLayerSet(con.layers['PT_BOX']).visible = False

        # Land or not?
        if self.is_land: pinlines = psd.getLayerSet(con.layers['LAND_PINLINES_TEXTBOX'])
        else: pinlines = psd.getLayerSet(con.layers['PINLINES_TEXTBOX'])

        # Check if vehicle
        if self.layout.type_line.find("Vehicle") >= 0: psd.getLayer("Vehicle", pinlines).visible = True
        else: psd.getLayer(self.layout.pinlines, pinlines).visible = True