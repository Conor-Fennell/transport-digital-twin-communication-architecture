from gui_helper import createLoopGui, lightsOff, lightOn
import turtle, json

wn = turtle.Screen()
wn.title("inductive loop lightS")
wn.bgcolor("black")

Nb_l1, Nb_l2, Nb_l3, Nb_l4, Sb_l1, Sb_l2, Sb_l3, Sb_l4 = createLoopGui()
while True:
    with open(r'consumed_topics\inductive_loops\0.txt', 'r', encoding='utf8') as f:
        last_line = json.loads(f.readlines()[-1].replace("'", "\""))
        if last_line['loop_id'] == 'M50_Southbound':
            lightsOff([Sb_l1,Sb_l2,Sb_l3,Sb_l4])
            if last_line['lane 1'] != '0':
                lightOn(Sb_l1)
            if last_line['lane 2'] != '0':
                lightOn(Sb_l2)
            if last_line['lane 3'] != '0':
                lightOn(Sb_l3)
            if last_line['lane 4'] != '0':
                lightOn(Sb_l4)
        if last_line['loop_id'] == 'M50_Northbound':
            lightsOff([Nb_l1,Nb_l2,Nb_l3,Nb_l4])
            if last_line['lane 1'] != '0':
                lightOn(Nb_l1)
            if last_line['lane 2'] != '0':
                lightOn(Nb_l2)
            if last_line['lane 3'] != '0':
                lightOn(Nb_l3)
            if last_line['lane 4'] != '0':
                lightOn(Nb_l4)

wn.mainloop()



