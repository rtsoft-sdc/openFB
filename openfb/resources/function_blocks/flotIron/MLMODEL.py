import math

class MLMODEL:
    def __init__(self):
        self.level_lim_h = 4.2
        self.level_lim_l = 3.5
        
        self.target_level_min = 3.85
        self.target_level_max = 3.95

        self.air_lim_h = 0.90
        self.air_lim_l = 0.20

        self.reagent_lim_h = 50.0
        self.reagent_lim_l = 5.0

    def schedule(self, event_input_name, event_input_value, CURRENTLEVEL, CURRENTVALVEPOS, CURRENTFROTHFLOW, CURRENTBUBBLESIZE):
        
        if event_input_name == "REQ":
            delta_level = 0.0
            delta_air = 0.0
            delta_reagent = 0.0

            if CURRENTLEVEL > self.target_level_max:
                delta_level = -0.05 * (CURRENTLEVEL - self.target_level_max)
            elif CURRENTLEVEL < self.target_level_min:
                delta_level = 0.05 * (self.target_level_min - CURRENTLEVEL)

            if CURRENTVALVEPOS > 0.80 and CURRENTLEVEL > self.target_level_min:
                delta_air -= 0.02
            elif CURRENTVALVEPOS < 0.20 and CURRENTLEVEL < self.target_level_max:
                pass

            if CURRENTLEVEL > 3.5 and CURRENTFROTHFLOW < 0.001:
                delta_reagent += 1.0

            if CURRENTBUBBLESIZE > 2.0:
                delta_air -= 0.05
                delta_reagent += 0.5
            elif 0.0 < CURRENTBUBBLESIZE < 0.8:
                delta_reagent -= 0.5

            print(f"[MLMODEL] Calculated Deltas -> Level: {delta_level:+.3f}m | Air: {delta_air:+.3f} | Reagent: {delta_reagent:+.3f}")

            return (
                event_input_value,
                round(delta_level, 3), self.level_lim_h, self.level_lim_l,
                round(delta_air, 3), self.air_lim_h, self.air_lim_l,
                round(delta_reagent, 3), self.reagent_lim_h, self.reagent_lim_l
            )