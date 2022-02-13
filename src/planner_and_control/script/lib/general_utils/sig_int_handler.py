import sys
import signal

class Activate_Signal_Interrupt_Hander:
    def __init__(self):
        self.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        print('\nYou pressed Ctrl+C! Never use Ctrl+Z!')
        sys.exit(0)