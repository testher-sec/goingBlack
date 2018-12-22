import sys
import getopt


def usage():
    print "BHP Net Tool"
    print
    print "Usage: bhpnet.py -t target_host -p port"
    print "-l --listen                  - listen on [host]:[port] for incoming connections"
    print "-e --execute=file_to_run     - execute the given file upon receiving a connection"
    print "-c --command                 - initialize a command shell"
    print "-u --upload=destination      - upon receiving connection upload a file and write to [destination]"
    print
    print
    print "Examples: "
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -c"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
    print "echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135"
    sys.exit(0)


def main():

    if not len(sys.argv[1:]):
        usage()

    try:
        # opts is the list of option-value pair
        # args is the rest of the arguments not processed
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    # I know you dont like elif, but using just ifs there is not 'else' at the end for unknown or missing options
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option " + str(o)

