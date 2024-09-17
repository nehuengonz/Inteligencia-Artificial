import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# Crear variables de entrada y salida
traffic_flow = ctrl.Antecedent(np.arange(0, 101, 1), 'traffic_flow')
pedestrian_density = ctrl.Antecedent(np.arange(0, 101, 1), 'pedestrian_density')
green_time = ctrl.Consequent(np.arange(0, 61, 1), 'green_time')
red_time = ctrl.Consequent(np.arange(0, 61, 1), 'red_time')

# Definir funciones de membresía
traffic_flow['low'] = fuzz.trimf(traffic_flow.universe, [0, 0, 30])
traffic_flow['medium'] = fuzz.trimf(traffic_flow.universe, [20, 50, 80])
traffic_flow['high'] = fuzz.trimf(traffic_flow.universe, [70, 100, 100])

pedestrian_density['low'] = fuzz.trimf(pedestrian_density.universe, [0, 0, 30])
pedestrian_density['medium'] = fuzz.trimf(pedestrian_density.universe, [20, 50, 80])
pedestrian_density['high'] = fuzz.trimf(pedestrian_density.universe, [70, 100, 100])

green_time['very_short'] = fuzz.trimf(green_time.universe, [0, 0, 15])
green_time['short'] = fuzz.trimf(green_time.universe, [10, 25, 40])
green_time['medium'] = fuzz.trimf(green_time.universe, [30, 45, 60])
green_time['long'] = fuzz.trimf(green_time.universe, [45, 60, 60])

red_time['very_short'] = fuzz.trimf(red_time.universe, [0, 0, 15])
red_time['short'] = fuzz.trimf(red_time.universe, [10, 25, 40])
red_time['medium'] = fuzz.trimf(red_time.universe, [30, 45, 60])
red_time['long'] = fuzz.trimf(red_time.universe, [45, 60, 60])

traffic_flow.view();
pedestrian_density.view();
green_time.view();
red_time.view();

#Crear reglas
# Include green_time in the consequent list
rule1 = ctrl.Rule(traffic_flow['high'] & pedestrian_density['low'], [green_time['long'], red_time['short']]) 
rule2 = ctrl.Rule(traffic_flow['low'] & pedestrian_density['high'], [green_time['short'], red_time['long']]) 
rule3 = ctrl.Rule(traffic_flow['medium'] & pedestrian_density['medium'], [green_time['medium'], red_time['medium']]) 
#Crear el sistema de control
ctrl_sys = ctrl.ControlSystem([rule1, rule2, rule3])
#ctrl_system = ctrl.ControlSystem([rule1])
#sim = ctrl.ControlSystemSimulation(ctrl_system)
sim = ctrl.ControlSystemSimulation(ctrl_sys)

#Calcular la salida para un conjunto de entradas
sim.input['traffic_flow'] = 50
sim.input['pedestrian_density'] = 30
sim.compute()
print(sim.output['green_time'])
print(sim.output['red_time'])

green_time.view(sim=sim)
red_time.view(sim=sim)