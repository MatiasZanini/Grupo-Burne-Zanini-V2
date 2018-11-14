class PIDController:

    def __init__(self, setpoint, kp=1.0, ki=0.0, kd=0.0):

        self.setpoint = setpoint
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.last_error = 0
        self.p_term = 0
        self.i_term = 0
        self.d_term = 0

    def calculate(self, feedback_value):
        error = self.setpoint - feedback_value

        delta_error = error - self.last_error

        self.p_term = self.kp * error
        self.i_term += error
        self.d_term = delta_error

        self.last_error = error

        return self.p_term + (self.ki * self.i_term) + (self.kd * self.d_term)



lazo = PIDController(42, 3, 2, 1)

while True:

    signal = read()

    actuator = lazo.calculate(signal)

    write(actuator)
