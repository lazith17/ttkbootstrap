"""
    Author: Israel Dryer
    Modified: 2021-06-08
    Adapted for ttkbootstrap from: https://github.com/israel-dryer/Mini-VLC-Player
"""
import ttkbootstrap as ttk

class Application(ttk.Application):

    def __init__(self):
        super().__init__(title="Media Player", theme="minty", position=(0, 0, NW))
        self.player = Player(self)
        self.player.pack(fill='both', expand='yes')

class Player(ttk.Frame):
    """
    An interface for a media player
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(padding=1)
        self.background = ttk.PhotoImage(
            file=r'src\ttkbootstrap\gallery\assets\mp_background.png')
        self.controls = {
            'skip-previous': '\u23EE',
            'play': '\u23F5',
            'pause': '\u23F8',
            'stop': '\u23F9',
            'skip-next': '\u23ED',
            'open-file': '\U0001f4c2'}

        # track information header
        self.setvar('track-info', 'Open a file to begin playback')
        header = ttk.Label(self, textvariable='track-info', padding=10, font='Helvetica 12', background='border')
        header.pack(fill='x', padx=2)

        # media container
        self.container = ttk.Label(self, image=self.background)
        self.container.pack(fill='both', expand='yes')

        # progress bar
        progress_frame = ttk.Frame(self, padding=10)
        progress_frame.pack(fill='x', expand='yes')
        self.time_elapsed = ttk.Label(progress_frame, text='00:00', font='Helvetica 12')
        self.time_scale = ttk.Scale(progress_frame, bootstyle='info')
        self.time_scale.pack(side='left', fill='x', expand='yes', padx=10)
        self.time_elapsed.pack(side='left')
        self.time_remaining = ttk.Label(progress_frame, text='00:00', font='Helvetica 12')
        self.time_remaining.pack(side='right')

        # button controls
        control_frame = ttk.Frame(self)
        control_frame.pack(fill='x', expand='yes')
        self.buttons = {
            'play': ttk.Button(control_frame, text=self.controls['play']),
            'skip-previous': ttk.Button(control_frame, text=self.controls['skip-previous']),
            'skip-next': ttk.Button(control_frame, text=self.controls['skip-next']),
            'pause': ttk.Button(control_frame, text=self.controls['pause']),
            'stop': ttk.Button(control_frame, text=self.controls['stop']),
            'open-file': ttk.Button(control_frame, text=self.controls['open-file'], bootstyle='secondary')}
        for button in ['skip-previous', 'play', 'skip-next', 'pause', 'stop', 'open-file']:
            self.buttons[button].pack(
                side='left', fill='x', expand='yes', ipadx=5, ipady=5, padx=2, pady=2)


if __name__ == '__main__':
    Application().run()
