from gui_helper import createLoopGui, lightsOff, lightOn
from constants import M50_NORTHBOUND_PATH, M50_SOUTHBOUND_PATH
import turtle, json

def lightLogic(FILE_PATH, LANES, t):
    with open(FILE_PATH, 'r', encoding='utf8') as f:
        last_line = json.loads(f.readlines()[-1].replace("'", "\""))   
        if last_line['timestamp'] != t:
            lanes = [False,False,False,False]
            if last_line['lane 1'] != '0':
                lightOn(LANES[0])
                lanes[0] = True
            if last_line['lane 2'] != '0':
                lightOn(LANES[1])
                lanes[1] = True
            if last_line['lane 3'] != '0':
                lightOn(LANES[2])
                lanes[2] = True
            if last_line['lane 4'] != '0':
                lightOn(LANES[3])  
                lanes[3] = True
            for i in range(len(lanes)):
                if lanes[i] is False:
                    lightsOff([LANES[i]]) 
            return last_line['timestamp']
            
if __name__ == '__main__':

    wn = turtle.Screen()
    wn.title("inductive loop lightS")
    wn.bgcolor("black")

    Nb_l1, Nb_l2, Nb_l3, Nb_l4, Sb_l1, Sb_l2, Sb_l3, Sb_l4 = createLoopGui()
    nb_lanes = [Nb_l1, Nb_l2, Nb_l3, Nb_l4]
    sb_lanes = [Sb_l1, Sb_l2, Sb_l3, Sb_l4]
    t1 = ''
    t2 = ''
    while True:
        t1 = lightLogic(M50_NORTHBOUND_PATH, nb_lanes, t1)
        t2 = lightLogic(M50_SOUTHBOUND_PATH, sb_lanes, t2)

    wn.mainloop()



