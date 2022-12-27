'''Tools for sending notifications.'''

import datetime
import os
import subprocess
import time


# Attemp to use ToastNotifier (if installed) on Windows.
try:
    from win10toast import ToastNotifier
except ImportError:
    print('No ToastNotifier module installed for notifications')
else:
    TOASTER = ToastNotifier()


def ns(title='Hello!', msg='', icon_path=None, duration=5, threaded=True, max_tries=5):
    '''Sends a desktop notification.'''
    msg = msg or 'Have a good {}!'.format(datetime.datetime.now().strftime('%A'))
    if os.name == 'nt':
        if 'TOASTER' not in globals():
            raise Exception('Not sure how to send notification without ToastNotifier')

        for tries in range(max_tries):
            try:
                res = TOASTER.show_toast(
                    title=title, msg=msg, icon_path=icon_path, duration=duration, threaded=threaded)
            except Exception as err:
                print('Failed to send ({}/{}):\n{}'.format(tries, max_tries, err))
                time.sleep(duration)
            else:
                if res:
                    break
                # If res is False, it means notification wasn't sent, so we try again.
                time.sleep(duration)
    else:
        subprocess.call("ns '%s'" % msg, shell=True)
