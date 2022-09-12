# @author: claudio rogerio claudiorogerio@unifap.br
# date: 4.09.2022
#
# TODO:
#   - enviar arquivos via socket
# MAKED:
#   - MSG com tags de açoes
#   - RECEBER nome do arquivo enviado

import socket
import os, subprocess, time, sys
from files import *
from service_time import *

# Define the port on which you want to connect
port = 5600
ip_server = '127.0.0.1'

if ( len(sys.argv) > 2 ):
    SERVICE = sys.argv[1]       # inicio de coleta
    upload_file = sys.argv[2]
else:
    if ( len(sys.argv) > 1 ):
        SERVICE = sys.argv[1]       # inicio de coleta
    else:
        SERVICE = 'ACK_START'

download_dir  = './files/download/'
download_file = ''
#download_file = download_dir  +'testesprovedor-0.1.5.zip'

script_file = "/script_provedor"

UPLOAD_ON = 0
upload_dir  = './files/upload/'
#upload_file = upload_dir + '######.zip'

RQS = ''
service_time = ''

s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
s.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )

id = str( os.getlogin() ) + ' ' + SERVICE

if SERVICE == 'ACK_START':

    print( ' [', Fore.BLUE + 'CLIENT-SEND' + Fore.RESET + ' ]', id )

    # connect to the server on local computer
    s.connect( ( ip_server, port ) )
    s.sendall( id.encode() )
    # receive data from the server and decoding to get the string.
    msg_server = s.recv( 1024 ).decode()
    msg_server = msg_server.split()
    print( ' [', Fore.GREEN + 'CLIENT-RECV' + Fore.RESET +  ' ]', msg_server )
    RQS = msg_server[0]
    project_file = msg_server[1]
    download_file = download_dir + project_file
    service_time = msg_server[2:]

    s.close()

if RQS == 'RCV_START':
    print( ' [', Fore.GREEN + 'CLIENT-RECV' + Fore.RESET + ' ] Download file:', download_file )
    #recv_files( filename = download_file, receiver = s )
    RQS = ''

    #START_SERVICE = True


if SERVICE == "ACK_START":
    print( " [ CLIENT   ON ] Opening software ", download_file )
    #cmd = 'unzip -o ' + download_file + ' -d ' + download_dir + ' '
    #os.system( cmd )
    print( " [ CLIENT   ON ] Requesting the Service Time (ST) ... ", service_time )
    print( " [ CLIENT   ON ] Starting Service period on: ", service_time )
    print( " [ CLIENT   ON ] Service: ", get_service_txt(service_time) )
    cmd = 'cd ' + download_file[:-4]
    cmd = subprocess.check_output( "pwd", shell= True )
    cmd = cmd.decode( "utf-8" ).split( '\n' )
    #print(cmd[0],'.....>')
    #print( cmd[0]+'/'+download_file[2:-4] , '1111' )
    cmd = 'cd ' + cmd[0] + '/' + download_file[ 2 : -4 ]  # retira o inicio './' e final '.zip'
    file = open( 'script_provedor_start', 'w' )
    file.write( cmd )
    file.close()
    #os.system( "source script_provedor_start" )
    #cmd = subprocess.check_output( "source script_provedor_start", shell= False )

    ##### executar script ####
    #os.system( 'pwd' )
    cmd = download_file[:-4] + script_file + get_service_txt( service_time ) + ' ' + download_file[:-4] #retira ponto e zip
    print('\n [ CLIENT   ON ] BASH:', cmd )
    time.sleep(2)
    os.system( cmd )

if SERVICE == 'ACK_UPLOAD':
    print( ' [ CLIENT UPLD ] UPLOAD RAW data: ', upload_file )
    s.connect( ( ip_server, port ) )

    id += ' ' + upload_file
    s.sendall( id.encode() )
    print( ' [', Fore.GREEN + 'CLIENT-SEND' + Fore.RESET +  ' ]', id )

    send_files( upload_file, s )
    print( ' [', Fore.GREEN + 'CLIENT-SEND' + Fore.RESET +  ' ] Send archive:', upload_file )

    #msg_server = s.recv( 2048 ).decode()
    #msg_server = msg_server.split()
    s.close()
