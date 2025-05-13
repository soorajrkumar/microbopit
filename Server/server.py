from microbit import *
import radio
import time
import random

uart.init(baudrate=115200, parity=True)

my_id, set_id = -1, 1
players = {}

def check_winner(x,winner):
    if decode_message(x)["received_id"] == winner:
        winner_name = decode_message(x)["msg"]
        return winner_name

def send_message(msg,target):
    global my_id
    
    x = "{};{};{}".format(my_id,msg,target)
    radio.send(x)

def decode_message(msg) -> dict:
    x = msg.split(";")
    return {
        "received_id": int(x[0]),
        "msg": x[1]
    }

def receive_message(msg):
    global set_id
    global my_id
    global winner
    result = decode_message(msg)
    if result["msg"] == "request_id":
        send_message(str(set_id),-2)
        display.scroll(set_id, wait=False)
        players[set_id] = 0
        set_id+=1

def play_game():
    global players
    
    instructions={
            "1":"Press A!",
            "2":"Press B!",
            "3":"Press Logo!",
            "4":"Shake!",
            "5":"Tilt Right!",
            "6":"Tilt Left!",
            "7":"Turn Upside-Down!",
            "8":"Make a Sound!",
        }
    
    while True:
        for each in players:
            if players[each] > 19:
                return each

        time.sleep(1)
        answer_count = 0
        correct_answer = str(random.randint(1,8))
        current_instruction = instructions[correct_answer]
        for each in players:
            send_message(current_instruction,each)
        while True:
            answer = radio.receive()
            if answer:
                answer_check = decode_message(answer)
                if answer_check["msg"] == correct_answer:
                    for each in players:
                        if each == answer_check["received_id"]:
                            send_message("point", each)
                            players[each] += 1
                        else:
                            send_message("no_point", each)
                    break 
                else:
                    answer_count+=1
                    if answer_count >= len(players):
                        for each in players:
                            send_message("no_point", each)
                        break 
                    

def endgame(winner):
    while True:
        incoming = radio.receive()
        if incoming:
            x = check_winner(incoming,winner)
            display.scroll(str(x))
            uart.write("{}\n".format(x))
            #the name from the winner is then passed into the 
            #connected computer to be stored and displayed as a bar chart
            return
    
radio.config(channel=8, group=2)
radio.on()

while True:
    
    incoming = radio.receive()
    if incoming:
        receive_message(incoming)
    if button_a.is_pressed():
        winner = play_game()
        for each in players:
            if each == winner:
                send_message("win",each)
            else:
                send_message("lose",each)
        endgame(winner)
        sleep(2000)
        reset()