import math

class BUBBLESIZEGEN:
    
    def get_bubble_size_by_level(H_p):
        H_tot = 4.5
        d_min = 1.2
        k_coalesce = 3.3
        
        if H_p >= H_tot:
            return d_min
            
        H_f = H_tot - H_p
        d_b = d_min * math.exp(k_coalesce * H_f)
        return round(d_b, 2)
    
    def schedule(self, event_input_name, event_input_value, LEVEL):

        if event_input_name == "REQ":
            bubblesize = None
            if LEVEL:
                bubblesize = self.get_bubble_size_by_level(LEVEL)
            return event_input_value, bubblesize