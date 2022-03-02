import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from lib import lib
import requests

username = "EternalDusk72"

response = requests.get("https://api.github.com/repos/EternalDusk/Infinite-Analysis/releases/latest")
print(response.json()["name"])

#api calls
with open('token.txt','r') as f:
    token = f.read()
lib = lib({'token': token})

profile = lib.halo.infinite['@0.3.9'].appearance({
  'gamertag': username
})

csr = lib.halo.infinite['@0.3.9'].stats.csrs({
  'gamertag': username,
  'season': 1,
  'version': 2
});

games = lib.halo.infinite['@0.3.9'].stats.matches.list({
  'gamertag': username,
  'limit': {
    'count': 25,
    'offset': 0
  },
  'mode': 'matchmade'
});

stats = lib.halo.infinite['@0.3.9'].stats['service-record'].multiplayer({
  'gamertag': username,
  'filter': 'matchmade:ranked'
});


print(profile["data"]["emblem_url"])
print(csr)

class tkinterApp(tk.Tk):

	# __init__ function for class tkinterApp
	def __init__(self, *args, **kwargs):

		# __init__ function for class Tk
		tk.Tk.__init__(self, *args, **kwargs)

		# creating a container
		container = tk.Frame(self)
		container.pack(side = "top", fill = "both", expand = True)

		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		# initializing frames to an empty array
		self.frames = {}

		# iterating through a tuple consisting
		# of the different page layouts
		for F in (StartPage, Page1, Page2):

			frame = F(container, self)

			# initializing frame of that object from
			# startpage, page1, page2 respectively with
			# for loop
			self.frames[F] = frame

			frame.grid(row = 0, column = 0, sticky ="nsew")

		self.show_frame(StartPage)

	# to display the current frame passed as
	# parameter
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()
