import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt

# HYPERPARAMETERS
FORMER_INNER_RADIUS = 13.5 #mm
COPPER_RESISTIVITY = 1.7e-8

SPOOL_WIDTH = 14.0 #mm
SPOOL_HEIGHT = 12.5 #mm

# 25 mm diameter assuming all flux goes through center cylinder
CORE_DIAMETER = 25
MEAN_PATH_LENGTH = 34 / 1000
PERMEABILITY_SPACE = 4e-7 * np.pi
REL_PERMEABILITY = 980
IRON_SAT = 1.6 # Teslas

IRON_AREA = np.pi * ((CORE_DIAMETER / 2000) ** 2)
DIM = np.array([SPOOL_WIDTH, SPOOL_HEIGHT])
RELUCTANCE = MEAN_PATH_LENGTH / (PERMEABILITY_SPACE * REL_PERMEABILITY * IRON_AREA)
IRON_H_CUTOFF = IRON_SAT / (PERMEABILITY_SPACE * REL_PERMEABILITY)

# Loading AWG Data
AWG = genfromtxt('awg.csv', delimiter=',', dtype=float)

class BatteryModel:
    # Lifespan in seconds please
    def __init__(self, peak, end, lifespan, output_resistance, isr = 0):
        self.set_params(peak, end, lifespan, output_resistance, isr)

    def use(self, duration):
        self.v = self.v - duration * self._gradient
        if self.v < self._boundary[1]:
            raise Exception("Battery model exceeds boundaries")

    def reset(self):
        self.v = self._boundary[0]

    def set_params(self, peak, end, lifespan, output_resistance, isr):
        self.v = peak
        self.isr = isr
        self.output_resistance = output_resistance
        self.lifespan = lifespan
        self.usage_time = 0
        self._gradient = (peak - end) / lifespan
        self._boundary = (peak, end)

class MagnetModel:
    def __init__(self, verbose=False, saturate=False):
        self.verbose = verbose
        self.saturate = saturate
        self.awg = 27
        self.winding = 400
    
    def set_params(self, awg, winding):
        self.awg = awg
        self.winding = winding

    """
    Get the AWG copper and enamel thickness
    Returns:
        copper radius, enamel radius
    """
    def get_awg_params(self):
        return (AWG[self.awg][1]/2, AWG[self.awg][2]/2)

    """
    Calculates the maximum number of windings in a given cross-sectional area
    Params: 
        insulator_radius: Copper radius including enamel in mm
    Returns:
        Array describing the max windings [max x, max y]
    """
    def calc_max_windings(self, insulator_radius):
        return np.floor(DIM / (insulator_radius * 2)).astype(int)

    """
    Calculates the packing factor in a cross sectional slice
    Params: 
    conductor_radius: Copper radius excluding enamel in mm
    windings: Number of windings passing through the cross sectional slice
    """
    def calc_packing_factor(self, conductor_radius):
        winding_area = DIM[0] * DIM[1]
        conductor_area = np.pi * (conductor_radius ** 2) * self.winding
        return conductor_area / winding_area

    def calc_winding_shape(self, max_windings):
        windings_shape = np.zeros(max_windings[0] * max_windings[1])

        # Set the used windings to 1
        for i in range(self.winding):
            windings_shape[i] = 1

        # Reshape to account for changing radius
        # Flipping order to make sure each row consists of the same wire loop circumference
        return windings_shape.reshape(max_windings[1], max_windings[0])

    """
    Calculate the winding length by forming a matrix that describes the windings
    Params:
        windings: Number of windings passing through the cross sectional slice
        max_windings: Array describing the max windings [max x, max y]
    Output:
        Total winding length in mm
    """
    def calc_winding_length(self, windings_shape, insulator_radius):
        insulator_dia = insulator_radius * 2 
        length = 0.0 # in mm
        for i, row in enumerate(windings_shape):
           radius = FORMER_INNER_RADIUS + (i * insulator_dia) + insulator_radius 
           winding_count = np.sum(row)
           length += winding_count * 2 * np.pi * radius
        
        return length

    """
    Calculate the winding resistance
    Params:
        winding_length: in mm
        conductor_radius: in mm
    Output:
        Total winding resistance in Ohms
    """
    def calc_winding_resistance(self, winding_length, conductor_radius):
        # Converting to meters and calculating area
        winding_length_m = winding_length / 1000
        conductor_area_m = np.pi * (conductor_radius / 1000) ** 2
        return (COPPER_RESISTIVITY * winding_length_m) / conductor_area_m

    """
    Calculate the winding current
    """
    def calc_winding_current(self, winding_resistance, internal_resistance, voltage):
        return voltage / (winding_resistance + internal_resistance)
    
    """
    Calculate the magnetic flux density
    """
    def calc_flux_density(self, winding_current):
        # METHOD 1
        # flux_density = PERMEABILITY * winding_current * (windings / 0.014) 

        # METHOD 2 with hard cutt
        # More complex calculation
        # mmf = self.winding * winding_current
        # flux = mmf / RELUCTANCE
        # flux_density = flux / IRON_AREA # Units of tesla
 
        # if(flux_density > IRON_SAT and self.saturate):
        #    flux_density = IRON_SAT

        # METHOD 3 using a linear approximation of B-H curve
        h = (self.winding * winding_current) / MEAN_PATH_LENGTH
        if h < IRON_H_CUTOFF:
            flux_density = PERMEABILITY_SPACE * REL_PERMEABILITY * h
        else:
            flux_density = PERMEABILITY_SPACE * REL_PERMEABILITY * IRON_H_CUTOFF + PERMEABILITY_SPACE * (h - IRON_H_CUTOFF)

        return flux_density

    """
    Calculate the pulling force
    """
    def calc_pulling_force(self, flux_density):
        return ((flux_density ** 2) * IRON_AREA)/(8e-7 * np.pi)

    def run(self, bat: BatteryModel):
        # Changing height is going to change the circumference of wire required
        # Units in mm
        conductor_radius, insulator_radius = self.get_awg_params()

        max_windings = self.calc_max_windings(insulator_radius)
            
        max_winding_count = max_windings[0] * max_windings[1]

        # Clamping the winding count to the maximum
        if self.winding > max_winding_count:
            self.winding = max_winding_count
     
        packing_factor = self.calc_packing_factor(conductor_radius)
        winding_shape = self.calc_winding_shape(max_windings) 
        winding_length = self.calc_winding_length(winding_shape, insulator_radius)
        winding_resistance = self.calc_winding_resistance(winding_length, conductor_radius)
        winding_current = self.calc_winding_current(winding_resistance, bat.isr, bat.v) 
        flux_density = self.calc_flux_density(winding_current)
        pull = self.calc_pulling_force(flux_density)

        if(self.verbose):
            print("\nPARAMS | (AWG: {}, WINDING: {}, VOLTAGE: {}, ISR: {})".format(self.awg, self.winding, bat.v, bat.isr))
            print("Max Windings: {}".format(max_windings))
            print("Packing Factor: {} %".format(packing_factor))
            print("Winding length: {} meters".format(winding_length/1000))
            print("Winding resistance: {} Ohms".format(winding_resistance))
            print("Winding current: {} A".format(winding_current))
            print("Flux Density: {} T".format(flux_density))
            print("Pulling Force: {} kg".format(pull/9.81))

        return pull/9.81, winding_current
