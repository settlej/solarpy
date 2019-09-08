#!/usr/bin/env python3

import socket
import threading
import subprocess
import time
import os
import sys
import shutil


class ping_device():
    def __init__(self, ip, dns=None, column=None, row=None, status=None):
        self.ip = ip
       # self.dns = dns
        if dns == '' or dns == None:
            self.dns = ip
        else:
            self.dns = dns
        self.column = column
        self.row = row
        self.status = status
    def __repr__(self):
        return self.ip
 
def clear_screen():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')


def createalldeviceobjects(alldeviesdict):
    localdeviceslist = []
    for devip, devname in alldeviesdict.items():
        localdeviceslist.append(ping_device(ip=devip, dns=devname))
    return localdeviceslist

def do_pings(devicesobjects, amount=2, timeout=1):
    returnlist = []
    processlist = []
    localdeviceslist = []
    for dev in devicesobjects:
        if os.name == 'posix':
            proc = subprocess.Popen('ping {} -c {} -W {}'.format(dev.ip, amount, timeout),shell=True, stdout=subprocess.PIPE)
        else:
            proc = subprocess.Popen('ping {} -n {} -w {}'.format(dev.ip, amount, timeout), stdout=subprocess.PIPE)
        processlist.append(proc)
    for num,process in enumerate(processlist):
        process.wait()
        result = (process.communicate())
        if '-name' in sys.argv:
            displayname = devicesobjects[num].dns
        else:
            displayname = devicesobjects[num].ip
        if os.name == 'posix':
            if r"100% packet loss" in str(result):
                devicesobjects[num].status = '\x1b[1;31;40m{:20}\x1b[0m'.format(displayname) 
            #elif not r"0% packet loss" in str(result):
            #    devicesobjects[num].status = '\x1b[1;33;40m{:20}\x1b[0m'.format(displayname) 
            else:
                devicesobjects[num].status = '\x1b[1;32;40m{:20}\x1b[0m'.format(displayname)            
        else:
            if r"(100% loss)" in str(result):
                devicesobjects[num].status = '\x1b[1;31;40m{:20}\x1b[0m'.format(displayname) 
            #elif not r"(0% loss)" in str(result):
            #    devicesobjects[num].status = '\x1b[1;33;40m{:20}\x1b[0m'.format(displayname) 
            else:
                devicesobjects[num].status = '\x1b[1;32;40m{:20}\x1b[0m'.format(displayname)
    return devicesobjects
    

def terminalgrouping(grouplist,devicelist, x, y):
    for dev in sorted(grouplist, key=lambda a: (a.status, a.ip)):
        dev.column = x
        dev.row = y
        x += 21
        if x > 64:
            y += 1
            x = 2
    for item in grouplist:
        print('\x1b[{};{}H{}\x1b[0m'.format( item.row,item.column,item.status))
    return devicelist, y

def percentage(part, whole):
  return 100 * float(part)/float(whole)


class TerminalResize(Exception):
    """Terminal Resized"""
    pass



#def restart():
#    while True:
#        if msvcrt.kbhit():
#            key = msvcrt.getch()
#            #print('hi')
#            if key == chr(32):
#                print('hasdfasdfasdf')
#                raise TerminalResize   # just to show the result
#
#
#t = threading.Thread(target=restart)
#t.daemon = True
#t.start()



if __name__ == '__main__':
    timeinterval = None
    if len(sys.argv) > 1:
        try:
            t_location = sys.argv.index('-t')
            timeinterval = sys.argv[t_location + 1]
        except IndexError:
            print('Invalid Option argument, needs to have a number')
            sys.exit()
        except ValueError or NameError:
            timeinterval = None
        if '-h' in sys.argv:
            print('Usage: solary.py [-t refresh_time_interval] [-name]\n' + 
                   '\t(10 sec) Example: solar.py -t 10 ' + 
                   '\n\t*Default time is 5 sec')
            sys.exit()
        if '-name' in sys.argv and not '-t' in sys.argv:
            pass
        elif all(('-name' in sys.argv, '-t' in sys.argv, len(sys.argv) > 3)):
            if not timeinterval.isdigit():
                print('Invalid Option argument, needs to be a number')
                sys.exit()
        #elif all('-name' in sys.argv, '-t' in sys.argv, len(sys.argv) == 3):
        #    t_location = sys.argv.index('-t')
        #    if not sys.argv[t_location + 1].isdigit():
        #        print('Invalid Option argument, needs to be a number')
        #        sys.exit()        
        #elif not sys.argv[1] == '-t':
        #    print('Invalid Option use "-t or -name or -h"')
        #    sys.exit()
        #elif sys.argv[1] == '-t' and len(sys.argv) > 2:
        #    if not sys.argv[2].isdigit():
        #        print('Invalid Option argument, needs to be a number')
        #        sys.exit()
        #elif sys.argv[1] == '-t' and len(sys.argv) == 2:
        #    print('Invalid Option argument, needs to have a number')
        #    sys.exit()
    
    clear_screen()
    print('Starting...')

    alldeviesdict = {
        '8.8.8.8': 'a',
        '8.8.8.9': 'b',
        '8.8.8.10': 'c',
        '8.8.8.11': 'd',
        '8.8.8.12': 'e',
        '8.8.8.13': 'f',
        '1.1.1.1': 'g',
        '2.2.2.2': 'a',
        '2.2.2.4': 'a',
        '8.8.8.8': 'a',
        '4.4.4.4': 'a',
        '98.138.219.232': 'a',
        '72.30.35.9': 'a',
        '72.30.35.10': 'a',
        '98.137.246.7': 'a',
        '98.137.246.8': 'a',
        '98.138.219.231': 'a',
        '13.107.21.200': 'a',
        '204.79.197.200': 'a',
        '172.217.8.142': 'a',
        '98.138.219.232': 'a',
        '72.30.35.9': 'a',
        '72.30.35.10': 'a',
        '98.137.246.7': 'a',
        '98.137.246.8': 'a',
        '40.97.161.50': 'a',
        '40.97.164.146': 'a',
        '40.97.116.82': 'a',
        '40.97.128.194': 'a',
        '40.97.148.226': 'a',
        '40.97.153.146': 'a',
        '40.97.156.114': 'a',
        '40.97.160.2': 'a',
        '106.10.248.150': 'a',
        '124.108.115.100': 'a',
        '212.82.100.150': 'a',
        '74.6.136.150': 'a',
        '98.136.103.23': 'a'
        }
    
    alldeviesdict = alldeviesdict
    devices_APIC = []
    devices_leafs = []
    devices_dmvpn = []
    devices_ise = []
    devices_Important_servers = []
    devices_Routers = []
    
    a = time.time()
    deviceobjects = createalldeviceobjects(alldeviesdict)
    deviceobjects = do_pings(deviceobjects, amount=2)
   
    for devobject in deviceobjects:
        if devobject.ip in [
                '8.8.8.8',
                '8.8.8.9',
                '8.8.8.10',
                '1.1.1.1',
                '2.2.2.2'
                ]:
            devices_APIC.append(devobject)
        elif devobject.ip in [
                '98.138.219.232',
                '72.30.35.9',
                '72.30.35.10',
                '98.137.246.7',
                '98.137.246.8',
                '98.138.219.231'
                ]:
            devices_ise.append(devobject)
        elif devobject.ip in [
                '13.107.21.200',
                '204.79.197.200',
                '172.217.8.142',
                '98.138.219.232'
                ]: 
            devices_leafs.append(devobject)
        elif devobject.ip in [
                '8.8.8.11',
                '8.8.8.12',
                '8.8.8.13',
                '106.10.248.150',
                '124.108.115.100',
                '212.82.100.150',
                '74.6.136.150',
                '98.136.103.23'
                ]:
            devices_dmvpn.append(devobject)
        elif devobject.ip in [
                '2.2.2.4',
                '4.4.4.4',
                '40.97.161.50',
                '40.97.164.146',
                '40.97.116.82',
                '40.97.128.194',
                '40.97.148.226',
                '40.97.153.146',
                '40.97.156.114',
                '40.97.160.2'
                ]:
            devices_Important_servers.append(devobject)

    clear_screen()
    terminalsize = shutil.get_terminal_size((80,20))
    counter = 1

    while True:
        try:
            x = 2 
            y = 2
            print('\x1b[{};{}H\x1b[1;37;40m{:-^57}\x1b[0m'.format(y,x,'APIC'))
            y += 1
            deviceobjects,y = terminalgrouping(devices_APIC,deviceobjects, x, y)
        
            y += 2
            print('\x1b[{};{}H\x1b[1;37;40m{:-^57}\x1b[0m'.format(y,x,'ISE'))
            y += 1    
            deviceobjects,y = terminalgrouping(devices_ise,deviceobjects, x, y)

            y += 2
            print('\x1b[{};{}H\x1b[1;37;40m{:-^57}\x1b[0m'.format(y,x,'Leaf'))
            y += 1
            deviceobjects,y = terminalgrouping(devices_leafs,deviceobjects, x, y)
            
            y += 2
            print('\x1b[{};{}H\x1b[1;37;40m{:-^57}\x1b[0m'.format(y,x,'DMVPN')) 
            y += 1
            deviceobjects,y = terminalgrouping(devices_dmvpn,deviceobjects, x, y)
            
            y += 2
            print('\x1b[{};{}H\x1b[1;37;40m{:-^57}\x1b[0m'.format(y,x,'SERVERS')) 
            y += 1
            deviceobjects,y = terminalgrouping(devices_Important_servers,deviceobjects, x, y)
            y += 2
            if timeinterval:
                #print(t_location)
                speed = int(timeinterval)
            else:
                speed = 5
            b = time.time()

            print('\n\n')
            print(' Uptime: {}\n Refresh Count: {}\n Refresh Interval: {} sec'.format(round(b-a, 2), int(counter), speed))
            counter += 1
            
            if terminalsize != shutil.get_terminal_size((80,20)):
                terminalsize = shutil.get_terminal_size((80,20))
                clear_screen()
                continue
    
            progressbar = 1
            bottomline = terminalsize.lines
            
            for s in range(speed-1):
                if speed > 2:
                    stringa = " \x1b[{};1H [%-{}s] %d%%   \x1b[?25l".format(y,speed)
                    print(stringa % ('='*(s+1), percentage(progressbar, speed)))
                if terminalsize != shutil.get_terminal_size((80,20)):
                    terminalsize = shutil.get_terminal_size((80,20))
                    raise TerminalResize
                time.sleep(1)
                progressbar +=1
                if progressbar == speed and speed > 2:
                    print(stringa % ('='*(s+2), percentage(progressbar, speed)))
    
            deviceobjects = do_pings(deviceobjects)
            
        except TerminalResize:
            print('\x1b[?25l ')
            clear_screen()
            continue
        except KeyboardInterrupt:
            print('\x1b[8')
            print('\x1b[?25h')
            print('\n\n Ending Program....')
            sys.exit()
