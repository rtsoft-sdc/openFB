import math

class FLOTMACHMODEL:
    def __init__(self, radius=1.2, height_max=4.5):
        self.name = "FLOTATIONMACHINEMODEL"
        
        self.radius = radius
        self.height_max = height_max
        self.square = math.pi * (self.radius ** 2)
        
        self.LevelMin = 3.5
        self.LevelMax = 4.2
        self.Level = 3.8
        
        self.BubbleSize = 1.2 #mm
        self.OutputFlow = 0.0 #m^3/s
        self.OutputFroth = 0.0 # m^3/s
        
        self.InputFlow = 0.1
        self.CurrentValvePos = 0.55
        self.CurrentAirValvePos = 0.60
        self.CurrentReagentFeed = 15.0 #gr/m^3
        
        self.K_valve_max = 0.45
        self.AirFlowMax = 0.1
        self.dt = 0.1

    def _calculate_bubble_size(self, air_flow, reagent_rate):
        base_size = 1.2
        air_effect = 0.8 * (air_flow / self.AirFlowMax)
        reagent_effect = math.exp(-0.05 * reagent_rate)
        
        bubble_size = (base_size + air_effect) * (0.4 + 0.6 * reagent_effect)
        return max(0.5, bubble_size)

    def _calculate_output_flow(self, level, valve_pos):
        if level <= 0 or valve_pos <= 0:
            return 0.0
        
        valve_characteristic = valve_pos ** 1.5
        hydrostatic_pressure = math.sqrt(level / self.LevelMax)
        return self.K_valve_max * valve_characteristic * hydrostatic_pressure

    def _calculate_froth_flow(self, level, air_flow, reagent_rate):
        if level < self.LevelMin:
            return 0.0
        
        # слой перелива
        overflow_head = level - self.LevelMin
        norm_head = overflow_head / (self.LevelMax - self.LevelMin)
        
        froth_stability = 1.0 - math.exp(-0.08 * reagent_rate)
        
        froth_flow = 0.15 * air_flow * norm_head * froth_stability
        return froth_flow

    def schedule(self, event_input_name, event_input_value, VALVEPOS, AIRVALVEPOS, REAGENTFEEDRATE, INPUTFLOW):
        if event_input_name == "INIT":
            self.Level = 3.8
            self.OutputFlow = 0.0
            self.OutputFroth = 0.0
            self.BubbleSize = 1.2
            return

        if event_input_name == "REQ":
            self.InputFlow = INPUTFLOW if INPUTFLOW >= 0.0 else self.InputFlow
            self.CurrentValvePos = max(0.0, min(1.0, VALVEPOS))
            self.CurrentAirValvePos = max(0.0, min(1.0, AIRVALVEPOS))
            self.CurrentReagentFeed = max(0.0, REAGENTFEEDRATE)

            current_air_flow = self.CurrentAirValvePos * self.AirFlowMax

            self.BubbleSize = self._calculate_bubble_size(current_air_flow, self.CurrentReagentFeed)
            self.OutputFlow = self._calculate_output_flow(self.Level, self.CurrentValvePos)
            self.OutputFroth = self._calculate_froth_flow(self.Level, current_air_flow, self.CurrentReagentFeed)

            # dV = (Q_in - Q_out_tail - Q_out_froth) * dt
            net_flow = self.InputFlow - self.OutputFlow - self.OutputFroth
            
            dLevel = (net_flow / self.square) * self.dt
            self.Level += dLevel

            self.Level = max(0.0, min(self.height_max, self.Level))
            
            return event_input_value, self.BubbleSize, self.Level, self.OutputFroth, self.CurrentAirValvePos, self.CurrentValvePos, current_air_flow, self.OutputFlow