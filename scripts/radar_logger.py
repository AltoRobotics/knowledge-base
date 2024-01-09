import time, os
from pyModbusTCP.client import ModbusClient

def bit(reg_content, bit_pos):
    return (reg_content[0] >> bit_pos) & 0x01

def check_control_unit_state(client):
    control_unit_state = client.read_holding_registers(41000, 1)
    if control_unit_state:
        # the detection in one field indicates that at least
        # one ofthe sensors has detected a target in that field
        msg = "Control unit state: "
        if (bit(control_unit_state, 4) == 0):
            msg = msg + "Restart feedback = Waiting manual restart"
        else:
            msg = msg + "Restart feedback = System running"
        if (bit(control_unit_state, 5) == 0):
            msg = msg + " - Stop feedback = Emergency request"
        else:
            msg = msg + " - Stop feedback = System running"
        if (bit(control_unit_state, 6) == 0):
            msg = msg + " - System diagnostic = System fault"
        else:
            msg = msg + " - System diagnostic = System running"
        if (bit(control_unit_state, 7) == 0):
            msg = msg + " - Configuration feedback = Configuration phase"
        else:
            msg = msg + " - Configuration feedback = System running"
        print("[%.4f] %s" % (time.time(), msg))

        msg = "Detection fields signal"
        if (bit(control_unit_state, 0) == 0):
            msg = msg + " - D.F. 1 [x]"
        else:
            msg = msg + " - D.F. 1 [ ]"
        if (bit(control_unit_state, 1) == 0):
            msg = msg + " - D.F. 2 [x]"
        else:
            msg = msg + " - D.F. 2 [ ]"
        if (bit(control_unit_state, 2) == 0):
            msg = msg + " - D.F. 3 [x]"
        else:
            msg = msg + " - D.F. 3 [ ]"
        if (bit(control_unit_state, 3) == 0):
            msg = msg + " - D.F. 4 [x]"
        else:
            msg = msg + " - D.F. 4 [ ]"
    else:
        msg = msg + " - Read error"
    print("[%.4f] %s" % (time.time(), msg))

def check_restart_feedback_signal(client):
    restart_feedback_signal = client.read_holding_registers(41000, 1)
    msg = "Restart feedback signal"
    if restart_feedback_signal:
        if (bit(restart_feedback_signal, 8) == 0):
            msg = msg + " - D.F. 1 [x]"
        else:
            msg = msg + " - D.F. 1 [ ]"
        if (bit(restart_feedback_signal, 9) == 0):
            msg = msg + " - D.F. 2 [x]"
        else:
            msg = msg + " - D.F. 2 [ ]"
        if (bit(restart_feedback_signal, 10) == 0):
            msg = msg + " - D.F. 3 [x]"
        else:
            msg = msg + " - D.F. 3 [ ]"
        if (bit(restart_feedback_signal, 11) == 0):
            msg = msg + " - D.F. 4 [x]"
        else:
            msg = msg + " - D.F. 4 [ ]"
    else:
        mgs = msg + " - Read Error"
    print("[%.4f] %s" % (time.time(), msg))

def check_static_object_detection_state(client):
    static_object_detection_state = client.read_holding_registers(41001, 1)
    msg = "Static object detection"
    if static_object_detection_state:
        if (bit(static_object_detection_state, 0) == 0):
            msg = msg + " - D.F. 1 [x]"
        else:
            msg = msg + " - D.F. 1 [ ]"
        if (bit(static_object_detection_state, 1) == 0):
            msg = msg + " - D.F. 2 [x]"
        else:
            msg = msg + " - D.F. 2 [ ]"
        if (bit(static_object_detection_state, 2) == 0):
            msg = msg + " - D.F. 3 [x]"
        else:
            msg = msg + " - D.F. 3 [ ]"
        if (bit(static_object_detection_state, 3) == 0):
            msg = msg + " - D.F. 4 [x]"
        else:
            msg = msg + " - D.F. 4 [ ]"
    else:
        print(" - Read error")
    print("[%.4f] %s" % (time.time(), msg))

def check_current_config_ID(client):
    current_config_ID = client.read_holding_registers(41002, 1)
    if current_config_ID:
        print("[%.4f] Current configuration ID = %s" % (time.time(), current_config_ID))
    else:
        print("[%.4f] Current configuration ID = %s" % (time.time(), "Read error"))

def check_muting_state(client):
    muting_state = client.read_holding_registers(41007, 1)
    msg = "Muting state"
    if muting_state:
        if (bit(muting_state, 0) == 0):
            msg = msg + " - Sensor 1 [x]"
        else:
            msg = msg + " - Sensor 1 [ ]"
        if (bit(muting_state, 1) == 0):
            msg = msg + " - Sensor 2 [x]"
        else:
            msg = msg + " - Sensor 2 [ ]"
    else:
        print(" - Read error")
    print("[%.4f] %s" % (time.time(), msg))

def check_sensor_state(client, sensor_num):
    register = 41008 + (sensor_num - 1)
    sensor_state = client.read_holding_registers(register, 1)
    if sensor_state:
        msg = "Sensor " + str(sensor_num) + " status: "
        if (bit(sensor_state, 4) == 0):
            msg = msg + "Sensor faulted"
        else:
            msg = msg + "Sensor running OK"
        if (bit(sensor_state, 5) == 0):
            msg = msg + " - Sensor muted"
        if (bit(sensor_state, 7) == 1):
            msg = msg + " - Sensor not installed"
        print("\n[%.4f] %s" % (time.time(), msg))

        if (bit(sensor_state, 0) == 0):
            msg = "D.F. 1 [x]"
        else:
            msg = "D.F. 1 [ ]"
        if (bit(sensor_state, 1) == 0):
            msg = msg + " - D.F. 2 [x]"
        else:
            msg = msg + " - D.F. 2 [ ]"
        if (bit(sensor_state, 2) == 0):
            msg = msg + " - D.F. 3 [x]"
        else:
            msg = msg + " - D.F. 3 [ ]"
        if (bit(sensor_state, 3) == 0):
            msg = msg + " - D.F. 4 [x]"
        else:
            msg = msg + " - D.F. 4 [ ]"
        print("[%.4f] %s" % (time.time(), msg))

        # "Presence" means that the sensor has found a target in that field.
        # Differently from "Detection", "Presence" does not consider the restart time-out value.
        if (bit(sensor_state, 8) == 0):
            msg = "P.F. 1 [x]"
        else:
            msg = "P.F. 1 [ ]"
        if (bit(sensor_state, 9) == 0):
            msg = msg + " - P.F. 2 [x]"
        else:
            msg = msg + " - P.F. 2 [ ]"
        if (bit(sensor_state, 10) == 0):
            msg = msg + " - P.F. 3 [x]"
        else:
            msg = msg + " - P.F. 3 [ ]"
        if (bit(sensor_state, 11) == 0):
            msg = msg + " - P.F. 4 [x]"
        else:
            msg = msg + " - P.F. 4 [ ]"
        print("[%.4f] %s" % (time.time(), msg))

        if (bit(sensor_state, 12) == 0):
            msg = "W.M. 1: restart"
        else:
            msg = "W.M. 1: access"
        if (bit(sensor_state, 13) == 0):
            msg = msg + " - W.M. 2: restart"
        else:
            msg = msg + " - W.M. 2: access"
        if (bit(sensor_state, 14) == 0):
            msg = msg + " - W.M. 3: restart"
        else:
            msg = msg + " - W.M. 3: access"
        if (bit(sensor_state, 15) == 0):
            msg = msg + " - W.M. 4: restart"
        else:
            msg = msg + " - W.M. 4: access"
        print("[%.4f] %s" % (time.time(), msg))
    else:
        print("\n[%.4f] %s" % (time.time(), "Sensor " + str(sensor_num) + " status - Read error\n"))

def check_sensor_detection_field(client, sensor_num, d_f_num):
    distance_reg = 41014 + (sensor_num-1)*8 + (d_f_num-1)
    angle_reg = distance_reg + 1
    distance = client.read_holding_registers(distance_reg, 1)
    angle = client.read_holding_registers(angle_reg, 1)

    # print(str(distance) + "   " + str(angle))
    print("[%.4f] Sensor %i D.F. %i: distance = %dmm   angle = %d°" % (time.time(), sensor_num, d_f_num, distance[0], angle[0]))

def main():
    
    client = ModbusClient(host="192.168.0.20", port=502, auto_open=True)
    client.write_multiple_registers(41002,[1])
    while True:

        t0 = time.time()

        print("\n"+"-"*50+"\n")
        
        check_current_config_ID(client)
        # check_control_unit_state(client)
        # check_restart_feedback_signal(client)
        # check_static_object_detection_state(client)
        # # check_muting_state(client)

        check_sensor_state(client, 1)
        check_sensor_detection_field(client, 1, 1)
        check_sensor_detection_field(client, 1, 2)

        check_sensor_state(client, 2)
        check_sensor_detection_field(client, 2, 1)
        check_sensor_detection_field(client, 2, 2)

        t_now = time.time()
        if ((t_now - t0) < 2.0) : time.sleep((2.0 - (t_now - t0)))

	#os.system('cls||clear')
	

if __name__ == '__main__':
	main()

