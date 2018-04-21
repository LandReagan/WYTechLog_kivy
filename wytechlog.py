import kivy
kivy.require('1.0.5')
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.app import App

import re
from decimal import Decimal, getcontext


class LabelBG(Label):
    pass


class TextInputNumBG(TextInput):

    def insert_text(self, substring, from_undo=False):
        pattern = re.compile('[0-9]|[.]')
        if re.match(pattern, substring):
            s = substring
        else:
            s = ''
        TextInput.insert_text(self, s, from_undo=from_undo)

    def on_double_tap(self):
        """ Overriding i.o.t avoid text selection """
        pass


class WYTechLog(BoxLayout):

    arr_fuel = ObjectProperty(None)
    fuel_fig_bef_ref = ObjectProperty(None)
    fuel_used_on_grd = ObjectProperty(None)
    dep_fuel = ObjectProperty(None)
    metered_fuel = ObjectProperty(None)
    sg = ObjectProperty(None)
    cf = ObjectProperty(None)
    met_uplift = ObjectProperty(None)
    tot_onboard = ObjectProperty(None)
    actual_uplift = ObjectProperty(None)
    discrepancy = ObjectProperty(None)

    def calculateFuelUsedOnBoard(self):
        if len(self.arr_fuel.text) > 0 and len(self.fuel_fig_bef_ref.text) > 0:
            arr_fuel = int(self.arr_fuel.text)
            fuel_fig_bef_ref = int(self.fuel_fig_bef_ref.text)
            self.fuel_used_on_grd.text = str(arr_fuel - fuel_fig_bef_ref)
        else:
            self.fuel_used_on_grd.text = ''

    def calculateMeteredUplift(self):
        getcontext().prec = 4
        if len(self.sg.text) > 0:
            sg = Decimal(self.sg.text)
            cf = 1 / sg
            self.cf.text = str(cf)
            if len(self.metered_fuel.text) > 0:
                metered_fuel = int(self.metered_fuel.text)
                self.met_uplift.text = str(int(metered_fuel / float(cf)))
            else:
                self.met_uplift.text = ''
        else:
            self.cf.text = ''

    def calculateActualUplift(self):
        if len(self.fuel_fig_bef_ref.text) > 0 and\
                len(self.tot_onboard.text) > 0:
            ffbr = int(self.fuel_fig_bef_ref.text)
            to = int(self.tot_onboard.text)
            self.actual_uplift.text = str(to - ffbr)
        else:
            self.actual_uplift.text = ''

    def calculateDiscrepancy(self):
        getcontext().prec = 2
        if len(self.actual_uplift.text) > 0 and len(self.met_uplift.text) > 0:
            au = int(self.actual_uplift.text)
            mu = int(self.met_uplift.text)
            discrepancy = float((au - mu) / au * 100)
            signe = '+' if discrepancy >= 0 else '-'
            discrepancy = getcontext().create_decimal(abs(discrepancy))
            self.discrepancy.text = signe + str(discrepancy)
        else:
            self.discrepancy.text = ''

    def reCalculateEverything(self):
        self.calculateFuelUsedOnBoard()
        self.calculateMeteredUplift()
        self.calculateActualUplift()
        self.calculateDiscrepancy()


class WYTechLogApp(App):

    def build(self):
        return WYTechLog()


if __name__ == '__main__':
        WYTechLogApp().run()
