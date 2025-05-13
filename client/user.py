from microbit import *
import OLED
import radio
import time
import music

OLED.init_display()

points, my_id = 0, 0
microphone.set_threshold(SoundEvent.QUIET, 30)
microphone.set_threshold(SoundEvent.LOUD, 70)


def get_id():
    global my_id
    send_message("request_id")
    while True:
        
        incoming = radio.receive()
        if incoming:
            data = decode_message(incoming)
            if data["target_id"] == -2:
                my_id = int(data["msg"])
                display.scroll(my_id)
                return False
        
    # server microbit requires a give_id() function
    # which, when called (by receiving the message "request_id")
    # returns a id_number to the user, and increments id_number by 1 for the next user

def get_point():
    display.show(Image.HAPPY)
    music.play(music.BA_DING)
    time.sleep(1)
    OLED.clear_display()
    display.clear()

def send_message(msg):
    global my_id
    id = my_id
    x = "{};{};-1".format(id, msg)
    radio.send(x)

def decode_message(msg) -> dict:
    x = msg.split(";") 
    return {
        "sender_id": int(x[0]),
        "msg": x[1],
        "target_id": int(x[2])
    }

def incoming_command(msg):
    result = decode_message(msg)
    x = "{}".format(result["msg"])
    if result["sender_id"] == -1:
        if result["target_id"] == my_id:
            if x == "point":
                get_point()
            elif x == "no_point":
                lose_point()
            elif x == "win":
                game_win()
            elif x == "lose":
                game_lose()
            else:
                OLED.show("",3)
                sleep(10)
                OLED.show(x,3)
                send_answer()
    # When message is recieved from server, display on line 3 (e.g "Press A")
    # If the target_id matches my_id, check for "win","lose","point"
    # This relies on the server sending a specific message
    # With the ID of whoever answered first.
    # EVERY message sent from the server must be in the format "{id};{message};{target_id}"
    # When sending instructions, set the id of the server to -1
    # This is so microbits playing the game cannot interfere with each other

def lose_point():
    display.show(Image.SAD)
    music.play(music.WAWAWAWAA)
    time.sleep(1)
    OLED.clear_display()
    display.clear()

def send_answer():
    player_answer = ""
    while True:
        thing = radio.receive()
        if thing:
            x = decode_message(thing)
            if x["target_id"] == my_id and x["msg"] == "no_point":
                lose_point()
                return
        if button_a.is_pressed():
            player_answer = "1"
            break
            
        elif button_b.is_pressed():
            player_answer = "2"
            break
    
        elif pin_logo.is_touched():
            player_answer = "3"
            break
    
        elif accelerometer.is_gesture("shake"):
            player_answer = "4"
            break
            
        elif accelerometer.is_gesture("right"):
            player_answer = "5"
            break
    
        elif accelerometer.is_gesture("left"):
            player_answer = "6"
            break
    
        elif accelerometer.is_gesture("face down"):
            player_answer = "7"
            break
    
        elif microphone.current_event() == SoundEvent.LOUD:
            player_answer = "8"
            break

    send_message(player_answer)

def game_win():
    OLED.show("You Win!",3)
    OLED.show("Enter 3 letters:",4)
    
    
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'SEND', 'CANCEL']
    pos = 0
    initials = ""
    while True:

        if pin_logo.is_touched():
            letter = letters[pos]
            if letter == "SEND":
                if len(initials) == 3:
                    send_message(initials)
                    initials = ""
                    display.clear() 
                    OLED.clear_display()
                    OLED.show("Reset to try again")
                    return False
                else: 
                    OLED.show("Please enter 3 letters:",4)
            elif letter == "CANCEL": 
                initials = ""
            elif len(initials) < 3:
                initials += letter
            OLED.show(initials, 7)
            sleep(100)
        
        if button_a.is_pressed():
            pos -= 1
            sleep(100)
        
            if pos < 0:
                pos = len(letters) - 1
    
        if button_b.is_pressed():
            pos += 1
            sleep(100)
            pos %= len(letters)
    
        letter = letters[pos]
        if letter == "SEND":
            display.show(Image.YES)
        elif letter == "CANCEL": 
            display.show(Image.NO)
        else:
            display.show(letters[pos])
        # When game is won, display a keyboard for the user to type a 3 letter name, and send it to the server
        # Server requires to enter a function when game is ended which sends a message with server id and "win" to the winner
        # as well as "lose" to the loser
        # This function awaits for one last message from the winner of their name
        # and sends it to the computer to be added to a dictionary which tracks wins for each name
        # This function will then reset the game so that players can restart quickly

def game_lose():
    OLED.show("You lose :(",3)
    OLED.show("Reset to try again",4)

radio.config(channel=8, group=2)
radio.on()
get_id()

while True:
    incoming = radio.receive()
    if incoming:
         incoming_command(incoming)
  


