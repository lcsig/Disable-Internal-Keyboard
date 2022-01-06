#!/bin/python3
import os
import sys
import re

core_kb = -1
xinput_output = os.popen('xinput -list').read()


def get_id(str_input: str):
    int_list = re.findall(r"id=(\d+)", str_input)
    if len(int_list) > 0:
        return int(int_list[0])
    return -1
   

def attach(id: int, attach_to: int):
    command = f"xinput --reattach {id} {attach_to} 2>&1"
    xinput_output = os.popen(command).read()
    if xinput_output.strip() == "":
        print("[+] " + command + "\t ---> Done Successfully")
    else:
        print("[!] " + command + "\t ---> Error in Execution")
   
   
def detach(id: int):
    command = f"xinput --float {id} 2>&1"
    xinput_output = os.popen(command).read()
    if xinput_output.strip() == "":
        print("[+] " + command + "\t ---> Done Successfully")
    else:
        print("[!] " + command + "\t ---> Error in Execution")
    
    
def get_core_keyboard(): 
    global core_kb
    if core_kb == -1:
        output_splitted = xinput_output.split("\n")
        for i in range(len(output_splitted)):
            if "Virtual core keyboard" in output_splitted[i]:
                core_kb = get_id(output_splitted[i])
                break
        return core_kb
    else:
        return core_kb
    
    
def detach_all(): 
    output_splitted = xinput_output.split("\n")
    for i in range(len(output_splitted)):
        if ("hotkeys" in output_splitted[i].lower() 
            or "button" in output_splitted[i].lower()
            or "2 keyboard" in output_splitted[i].lower()
            or "DP-" in output_splitted[i]
            or "UNKNOWN" in output_splitted[i]):
            detach(get_id(output_splitted[i]))
        

def attach_all():
    output_splitted = xinput_output.split("\n")
    for i in range(len(output_splitted)):
        if "floating slave" in output_splitted[i].lower():
            attach(get_id(output_splitted[i]), get_core_keyboard())
            
            
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if "deattach" in sys.argv[1].lower() or "detach" in sys.argv[1].lower():
            detach_all()
            exit()
        elif "attach" in sys.argv[1].lower() or "reattach" in sys.argv[1].lower():
            attach_all()
            exit()
            
