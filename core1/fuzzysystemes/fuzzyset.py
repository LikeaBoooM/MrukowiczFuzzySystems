import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from collections import Counter

# pierwsza zmienna wejściowa - wilgotność w pokoju (pobierana z czujnika DHT11)
humidity = ctrl.Antecedent(np.arange(0, 11), 'humidity in room (0-100%)/10')

# druga zmienna wejściowa - temperatura w pokoju (pobierana z czujnika DHT11)
roomtemperature = ctrl.Antecedent(np.arange(0, 31), 'temperature in room (0-30 celcius grades)')

# trzecie zmienna wejściowa - temperatura na piecu (pobierana stała wartość z serwera)
oventemeperature = ctrl.Antecedent(np.arange(0, 101), 'temperature on oven (0-100 calcius grade)')

# zmienna wyjściowa - ocena temperatury oraz wilgotności w pokoju
gradeofroomstate = ctrl.Consequent(np.arange(0, 11), 'general grade of atmospheric caonditions in room')

# funkcje przynaleznosci do pierwszej zmiennej wejsciowej (wilgotność w pokoju)
humidity['DRY'] = fuzz.trapmf(humidity.universe, [0, 0, 1, 3])
humidity['WELL'] = fuzz.trimf(humidity.universe, [1, 4, 7])
humidity['WET'] = fuzz.trapmf(humidity.universe, [4, 7, 10, 10])
humidity.view()


# funkcje przynaleznosci do pierwszej zmiennej wejsciowej (temperatura w pokoju)
roomtemperature['COLD'] = fuzz.trapmf(roomtemperature.universe, [0, 0, 10, 15])
roomtemperature['WELL'] = fuzz.trimf(roomtemperature.universe, [13, 18, 22])
roomtemperature['HIGH'] = fuzz.trapmf(roomtemperature.universe, [18, 22, 30, 30])
roomtemperature.view()


# funkcje przynaleznosci do pierwszej zmiennej wejsciowej (temperatura na piecu)
oventemeperature['LOW'] = fuzz.trapmf(oventemeperature.universe, [0, 0, 20, 40])
oventemeperature['WELL'] = fuzz.trimf(oventemeperature.universe, [30, 40, 55])
oventemeperature['HIGH'] = fuzz.trapmf(oventemeperature.universe, [40, 55, 100, 100])
oventemeperature.view()


# funkcje przynaleznosci do zmiennej wyjsciowej
gradeofroomstate['UNACCEPTABLE'] = fuzz.trapmf(gradeofroomstate.universe, [0, 0, 2, 4])
gradeofroomstate['ACCEPTABLE'] = fuzz.trimf(gradeofroomstate.universe, [2, 4, 6])
gradeofroomstate['GOOD'] = fuzz.trimf(gradeofroomstate.universe, [4, 6, 8])
gradeofroomstate['VERY_GOOD'] = fuzz.trapmf(gradeofroomstate.universe, [7, 8, 10, 10])
gradeofroomstate.view()


rules = []

rules.append(ctrl.Rule(humidity['DRY'] & roomtemperature['COLD'] & oventemeperature['LOW'],
                       gradeofroomstate['UNACCEPTABLE']))

rules.append(ctrl.Rule(humidity['WELL'] & roomtemperature['COLD'] & oventemeperature['LOW'],
                       gradeofroomstate['UNACCEPTABLE']))

rules.append(ctrl.Rule(humidity['WET'] & roomtemperature['COLD'] & oventemeperature['LOW'],
                       gradeofroomstate['UNACCEPTABLE']))

rules.append(ctrl.Rule(humidity['DRY'] & roomtemperature['WELL'] & oventemeperature['LOW'],
                       gradeofroomstate['ACCEPTABLE']))

rules.append(ctrl.Rule(humidity['WELL'] & roomtemperature['WELL'] & oventemeperature['LOW'],
                       gradeofroomstate['ACCEPTABLE']))

rules.append(ctrl.Rule(humidity['DRY'] & roomtemperature['HIGH'] & oventemeperature['LOW'],
                       gradeofroomstate['ACCEPTABLE']))

rules.append(ctrl.Rule(humidity['WELL'] & roomtemperature['HIGH'] & oventemeperature['LOW'],
                       gradeofroomstate['GOOD']))

rules.append(ctrl.Rule(humidity['WET'] & roomtemperature['HIGH'] & oventemeperature['LOW'],
                       gradeofroomstate['ACCEPTABLE']))

rules.append(ctrl.Rule(humidity['DRY'] & roomtemperature['COLD'] & oventemeperature['WELL'],
                       gradeofroomstate['ACCEPTABLE']))

rules.append(ctrl.Rule(humidity['WELL'] & roomtemperature['COLD'] & oventemeperature['WELL'],
                       gradeofroomstate['GOOD']))

rules.append(ctrl.Rule(humidity['WET'] & roomtemperature['COLD'] & oventemeperature['WELL'],
                       gradeofroomstate['UNACCEPTABLE']))

rules.append(ctrl.Rule(humidity['DRY'] & roomtemperature['WELL'] & oventemeperature['WELL'],
                       gradeofroomstate['VERY_GOOD']))

rules.append(ctrl.Rule(humidity['WELL'] & roomtemperature['WELL'] & oventemeperature['WELL'],
                       gradeofroomstate['VERY_GOOD']))

rules.append(ctrl.Rule(humidity['WET'] & roomtemperature['WELL'] & oventemeperature['WELL'],
                       gradeofroomstate['GOOD']))

rules.append(ctrl.Rule(humidity['DRY'] & roomtemperature['HIGH'] & oventemeperature['WELL'],
                       gradeofroomstate['VERY_GOOD']))

rules.append(ctrl.Rule(humidity['WELL'] & roomtemperature['HIGH'] & oventemeperature['WELL'],
                       gradeofroomstate['VERY_GOOD']))

rules.append(ctrl.Rule(humidity['WET'] & roomtemperature['HIGH'] & oventemeperature['WELL'],
                       gradeofroomstate['ACCEPTABLE']))

rules.append(ctrl.Rule(humidity['DRY'] & roomtemperature['COLD'] & oventemeperature['HIGH'],
                       gradeofroomstate['ACCEPTABLE']))

rules.append(ctrl.Rule(humidity['WELL'] & roomtemperature['COLD'] & oventemeperature['HIGH'],
                       gradeofroomstate['GOOD']))

rules.append(ctrl.Rule(humidity['WET'] & roomtemperature['COLD'] & oventemeperature['HIGH'],
                       gradeofroomstate['UNACCEPTABLE']))

rules.append(ctrl.Rule(humidity['DRY'] & roomtemperature['WELL'] & oventemeperature['HIGH'],
                       gradeofroomstate['GOOD']))

rules.append(ctrl.Rule(humidity['WELL'] & roomtemperature['WELL'] & oventemeperature['HIGH'],
                       gradeofroomstate['GOOD']))

rules.append(ctrl.Rule(humidity['WET'] & roomtemperature['WELL'] & oventemeperature['HIGH'],
                       gradeofroomstate['ACCEPTABLE']))

rules.append(ctrl.Rule(humidity['DRY'] & roomtemperature['HIGH'] & oventemeperature['HIGH'],
                       gradeofroomstate['GOOD']))

rules.append(ctrl.Rule(humidity['WELL'] & roomtemperature['HIGH'] & oventemeperature['HIGH'],
                       gradeofroomstate['VERY_GOOD']))

rules.append(ctrl.Rule(humidity['WET'] & roomtemperature['HIGH'] & oventemeperature['HIGH'],
                       gradeofroomstate['ACCEPTABLE']))


# definiujemy sterownik rozmyty
state_ctrl = ctrl.ControlSystem(rules)
# symulacja działania sterownika
state_simulation = ctrl.ControlSystemSimulation(state_ctrl)
# wyjście
state_simulation.input['humidity in room (0-100%)/10'] = 5
state_simulation.input['temperature in room (0-30 celcius grades)'] = 25
state_simulation.input['temperature on oven (0-100 calcius grade)'] = 55

state_simulation.compute()
gradeofroomstate.view(sim=state_simulation)
print(state_simulation.output['general grade of atmospheric caonditions in room'])
state_ctrl.view()
plt.show()





