import subprocess

import xbmc
import xbmcaddon
import xbmcgui


class Screensaver(xbmcgui.WindowXMLDialog):
    """
    Run the appropriate vcgencmd commands to turn the display on and off
    """

    class Monitor(xbmc.Monitor):
        """
        Enable a command to be run when the screensaver is deactivated
        """

        def __init__(self, callback):
            self._callback = callback

        def onScreensaverDeactivated(self):
            self._callback()

    def _run_vcgencmd(self, enable):
        """
        Run the vcgencmd command to enable or disable the display
        """
        subprocess.call(['/opt/vc/bin/vcgencmd', 'display_power', enable])

    def onInit(self):
        """
        Enable power saving mode and monitor the screensaver
        """
        self._monitor = self.Monitor(self._exit)
        self._run_vcgencmd('0')

    def _exit(self):
        """
        Deactivate power saving mode and close the window
        """
        self._run_vcgencmd('1')
        self.close()


if __name__ == '__main__':
    screensaver = Screensaver(
        'plugin-screensaver-vcgencmd.xml',
        xbmcaddon.Addon().getAddonInfo('path'),
        'default',
    )
    screensaver.doModal()
    del screensaver
