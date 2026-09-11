class PIDController:
    def __init__(self):
        pass
    
class Gateway:
    def __init__(self):
        self.opcua_client = None
        
        

class PIDBubbleControl:
    def __init__(self, kp, ki, kd):
        self.set_parameters(kp, ki, kd)
        self.integral = 0
        self.previous_error = 0
        
    def temperature_control(self, setpoint, measured_value, dt):
        error = setpoint - measured_value
        self.integral += error * dt
        derivative = (error - self.previous_error) / dt if dt > 0 else 0
        
        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        self.previous_error = error

        return output
    

    def schedule(self, event_input_name, event_input_value, Kp, Ki, Kd, LIM_LOW, LIM_HIGH):
        if event_input_name == "INIT":
            self.set_parameters(Kp, Ki, Kd)
            self.reset()
        elif event_input_name == "REQ":
            temperature = 20.0
            if event_input_value < LIM_LOW:
                self.reset()
            elif event_input_value > LIM_HIGH:
                self.reset()
            else:
                pass

    def update(self, setpoint, measured_value, dt):
        error = setpoint - measured_value
        self.integral += error * dt
        derivative = (error - self.previous_error) / dt if dt > 0 else 0

        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        self.previous_error = error

        return output
    
    def reset(self):
        self.integral = 0
        self.previous_error = 0
        
    def set_parameters(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        
        