import os
import pickle
import random
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
from pygame import mixer


class Player(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()

        mixer.init()

        if os.path.exists('songs.pickle'):
            with open('songs.pickle', 'rb') as f:
                self.playlist = pickle.load(f)
        else:
            self.playlist = []

        self.current = 0
        self.paused = True
        self.played = False

        self.create_frames()
        self.control_widget()
        self.tracklist_widget()
        self.track_widget()

    def create_frames(self):
        self.track = tk.LabelFrame(self, text="Track", font=("Bradley Hand ITC", 15, "bold"),
                                   bg="#579492", fg="Black", bd=5, relief=tk.GROOVE)
        self.track.configure(width=555, height=310)
        self.track.grid(row=0, column=0, padx=3, pady=3)

        self.tracklist = tk.LabelFrame(self, text=f'playlist - {str(len(self.playlist))}',
                                       font=("Bradley Hand ITC", 15, "bold"),
                                       bg="#6aadab", fg="Black", bd=7, relief=tk.GROOVE)
        self.tracklist.configure(width=230, height=400)
        self.tracklist.grid(row=0, column=1, rowspan=3, pady=3, padx=3)

        self.controls = tk.LabelFrame(self, font=("Bradley Hand ITC", 15, "bold"),
                                      bg="#8ed0ce", fg="Black", bd=7, relief=tk.GROOVE)
        self.controls.configure(width=655, height=80)
        self.controls.grid(row=1, column=0, padx=3, pady=3)

    def track_widget(self):
        self.canvas = tk.Label(self.track, image=img, bg="#579492")
        self.canvas.configure(width=540, height=240)
        self.canvas.grid(row=0, column=0)

        self.songtrack = tk.Label(self.track, font=("Bradley Hand ITC", 15, "bold"),
                               bg="#6aadab", fg="Black")
        self.songtrack['text'] = "Music Player"
        self.songtrack.configure(width=40, height=1)
        self.songtrack.grid(row=1, column=0)

    def control_widget(self):
        self.loadsongs = tk.Button(self.controls, bg="#e8a0eb", fg="grey", font=10)
        self.loadsongs['text'] = 'Load Songs'
        self.loadsongs['command'] = self.retrieve_songs
        self.loadsongs.grid(row=0, column=0, padx=3)

        self.prev = tk.Button(self.controls, image=prev)
        self.prev['command'] = self.prev_song
        self.prev.grid(row=0, column=1)

        self.pause = tk.Button(self.controls, image=pause)
        self.pause['command'] = self.pause_song
        self.pause.grid(row=0, column=2)

        self.next = tk.Button(self.controls, image=next)
        self.next['command'] = self.next_song
        self.next.grid(row=0, column=3)

        self.shuffle = tk.Button(self.controls, image=shuffle)
        self.shuffle['command'] = self.shuffle_song
        self.shuffle.grid(row=0, column=5)

        self.volume = tk.DoubleVar()
        self.slider = tk.Scale(self.controls, from_ =0, to=10, orient=tk.HORIZONTAL)
        self.slider['variable'] = self.volume
        self.slider.set(8)
        mixer.music.set_volume(0.8)
        self.slider['command'] = self.change_volume
        self.slider.grid(row=0, column=4, padx=3)

    def tracklist_widget(self):
        self.scrollbar = tk.Scrollbar(self.tracklist, orient=tk.VERTICAL)
        self.scrollbar.grid(row=0, column=1, rowspan=5, sticky='ns')

        self.list = tk.Listbox(self.tracklist, selectmode=tk.SINGLE,
                               yscrollcommand=self.scrollbar.set, selectbackground='sky blue')
        self.enumerate_songs()
        self.list.config(height=22)
        self.list.bind('<Double-1>', self.play_song)
        self.scrollbar.config(command=self.list.yview)
        self.list.grid(row=0, column=0, rowspan=5)

    def enumerate_songs(self):
        for index, song in enumerate(self.playlist):
            self.list.insert(index, os.path.basename(song))

    def retrieve_songs(self):
        self.songlist = []
        directory = filedialog.askdirectory()
        for root_, dirs, files in os.walk(directory):
            for file in files:
                if os.path.splitext(file)[1] == '.mp3':
                    path = (root_ + '/' + file).replace('\\','/')
                    self.songlist.append(path)

        with open('songs.pickle', 'wb') as f:
            pickle.dump(self.songlist, f)

        self.playlist = self.songlist
        self.tracklist['text'] = f'playlist - {str(len(self.playlist))}'
        self.list.delete(0, tk.END)
        self.enumerate_songs()

    def play_song(self, event=None):
        if event is not None:
            self.current = self.list.curselection()[0]
            for i in range(len(self.playlist)):
                self.list.itemconfigure(i, bg="grey")

        mixer.music.load(self.playlist[self.current])
        self.pause['image'] = play
        self.paused = False
        self.played = True
        self.songtrack['anchor'] = 'w'
        self.songtrack['text'] = os.path.basename(self.playlist[self.current])
        self.list.activate(self.current)
        self.list.itemconfigure(self.current, bg="sky blue")
        mixer.music.play()

    def pause_song(self):
        if not self.paused:
            self.paused = True
            mixer.music.pause()
            self.pause['image'] = pause
        else:
            if self.played == False:
                self.play_song()
            self.paused = False
            mixer.music.unpause()
            self.pause['image'] = play

    def prev_song(self):
        if self.current > 0:
            self.current -= 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current, bg="white")
        self.play_song()

    def next_song(self):
        if self.current < len(self.playlist) - 1:
            self.current += 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current, bg="white")
        self.play_song()

    def change_volume(self, event=None):
        self.v = self.volume.get()
        mixer.music.set_volume(self.v / 10)

    def shuffle_song(self):
        random.shuffle(self.playlist)
        self.play_song()


root = tk.Tk()
root.geometry('800x400')
root.wm_title('Music Player')

img = PhotoImage(file="img1.png")
prev = PhotoImage(file="prev.png")
pause = PhotoImage(file="pause.png")
play = PhotoImage(file="play.png")
next = PhotoImage(file="next.png")
shuffle = PhotoImage(file="shuffle.png")

app = Player(master=root)
app.mainloop()
