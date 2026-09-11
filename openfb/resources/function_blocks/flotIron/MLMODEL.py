import math

class MLMODEL:
    def __init__(self):
        self.air_sp_base = 0.6
        self.reagent_sp_base = 15.0
        self.valve_sp_base = 0.55
        self.level_sp_base = 0.55

        self.valve_lim_h = 1.0
        self.valve_lim_l = 0.05
        
        self.air_lim_h = 0.90
        self.air_lim_l = 0.20

        self.reagent_lim_h = 50.0
        self.reagent_lim_l = 5.0

    def schedule(self, event_input_name, event_input_value, CURRENTLEVEL, CURRENTVALVEPOS, CURRENTFROTHFLOW, CURRENTBUBBLESIZE,
                 CURRENTAIRFLOW, CURRENTREAGENTFEED):
        
        if event_input_name == "REQ":
            delta_level = 0.0
            delta_air = 0.0
            delta_reagent = 0.0

            if CURRENTVALVEPOS > 0.80:
                delta_level -= (CURRENTVALVEPOS - 0.80) * 1.2
                delta_air -= 0.03

            elif CURRENTVALVEPOS < 0.20:
                delta_level += 0.05

            if CURRENTLEVEL > 3.5 and CURRENTFROTHFLOW < 0.001:
                delta_reagent += 2.0
                delta_level += 0.03

            if CURRENTBUBBLESIZE > 2.0:
                delta_air -= 0.05
                delta_reagent += 1.0
            elif 0.0 < CURRENTBUBBLESIZE < 0.8:
                delta_reagent -= 1.0

            sp_level = max(0.05, min(1.0, self.level_sp_base + delta_level))
            sp_air = max(self.air_lim_l, min(self.air_lim_h, self.air_sp_base + delta_air))
            sp_reagent = max(self.reagent_lim_l, min(self.reagent_lim_h, self.reagent_sp_base + delta_reagent))

            print(f"[MLMODEL] Target Level: {sp_level:.3f}m | Valve Limits: [{self.valve_lim_l}..{self.valve_lim_h}] | Air: {sp_air:.2f}")

            return (
                event_input_value,
                round(sp_level, 3), self.valve_lim_h, self.valve_lim_l,
                round(sp_air, 3), self.air_lim_h, self.air_lim_l,
                round(sp_reagent, 3), self.reagent_lim_h, self.reagent_lim_l
            )