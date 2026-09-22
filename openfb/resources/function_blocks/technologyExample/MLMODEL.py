class MLMODEL:
    def __init__(self):
        self.level_lim_h = 100.0 # can be more flexible
        self.level_lim_l = 0
        self.target_level = 3.8

        self.air_lim_h = 0.90
        self.air_lim_l = 0.20

        self.reagent_lim_h = 50.0
        self.reagent_lim_l = 5.0

    def schedule(self, event_input_name, event_input_value, CURRENTLEVEL, CURRENTVALVEPOS, CURRENTFROTHFLOW, CURRENTBUBBLESIZE):
        if event_input_name == "REQ":
            delta_level = 0.0
            delta_air = 0.0
            delta_reagent = 0.0

            level_error = self.target_level - CURRENTLEVEL
            delta_level = 0.1 * level_error  

            if CURRENTBUBBLESIZE is not None and CURRENTBUBBLESIZE > 0:
                if CURRENTBUBBLESIZE > 2.0:
                    delta_air -= 0.05
                    delta_reagent += 0.5
                elif CURRENTBUBBLESIZE < 1.0:
                    delta_air += 0.05
                    if CURRENTBUBBLESIZE < 0.8:
                        delta_reagent -= 0.5

            if CURRENTVALVEPOS > 0.80 and CURRENTLEVEL > self.target_level:
                delta_air -= 0.02

            if CURRENTLEVEL > 3.5 and CURRENTFROTHFLOW < 0.001:
                delta_reagent += 1.0

            return (
                event_input_value,
                round(delta_level, 4), self.level_lim_h, self.level_lim_l,
                round(delta_air, 4), self.air_lim_h, self.air_lim_l,
                round(delta_reagent, 4), self.reagent_lim_h, self.reagent_lim_l
            )
        
        return event_input_value, 0.0, self.level_lim_h, self.level_lim_l, 0.0, self.air_lim_h, self.air_lim_l, 0.0, self.reagent_lim_h, self.reagent_lim_l