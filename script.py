import tkinter
from threading import Thread
from time import sleep
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog
from tkinter.ttk import Progressbar
import urllib.parse as urlparse
import urllib.request
from urllib.request import urlopen
import re
import os

# Logic

def requestTabs(progressBar):
	dir = filedialog.askdirectory()
	texts = entry.get("1.0", tkinter.END).rstrip().split('\n')
	stepSize = 100 / len(texts)

	startLoading()
	for text in texts:
		url = urlparse.urlparse(text)
		query = url.query
		queryId = urlparse.parse_qs(url.query)['ID'][0]
		printUrl = "https://www.harptabs.com/printsong.php?ID=" + queryId

		# Build the request
		opener = urllib.request.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]

		# Get the HTML within the page
		urllib.request.install_opener(opener)
		print('Downloading ' + printUrl)
		html = urlopen(printUrl).read().decode(errors='ignore').replace("&nbsp;", " ")  # Replace the non breaking spaces as they create errors with generated files

		# Extract the name from the HTML header
		title = re.search('(?<=<title>).+?(?=</title>)', html, re.DOTALL).group().strip()
		title = title.replace('*', '').replace('.', '').replace(':', '').replace('?', '')

		# Write the HTML file to disk
		filePath = os.path.join(dir, title + ".html")
		file = open(filePath, "w")
		file.write(html)
		file.close()
		progressBar['value'] += stepSize

	endLoading()

# UI Actions

def startLoading():
	button.configure(state="disabled")
	entry.configure(state="disabled")
	progressBar.start()

def endLoading():
	button.configure(state="normal")
	entry.configure(state="normal")
	entry.delete('1.0', END)
	progressBar.stop()
	messagebox.showinfo('Done!', 'The tabs are in your folder')

def onButtonClicked():
	t = Thread(target=requestTabs, args=[progressBar])
	t.start()

# UI Layout

window = Tk()
window.title("HarpGrabber by Ferdz")
window.resizable(False, False)

label = Label(window, justify="left",
			  text="Paste a list of all the HarpTabs links to download in the box below.\nFor example: \nhttps://www.harptabs.com/song.php?ID=28454\nhttps://www.harptabs.com/song.php?ID=28170\nhttps://www.harptabs.com/song.php?ID=28164")
label.grid(column=0, row=0, columnspan=2, pady=8)

entry = scrolledtext.ScrolledText(window, width=45, height=25)
entry.grid(column=0, row=1, columnspan=2, padx=8)
entry.focus()

progressBar = Progressbar(window, length=200, mode='determinate')
progressBar.grid(column=0, row=2, pady=8)

button = Button(window, text="Download tabs", command=onButtonClicked)
button.grid(column=1, row=2)

window.mainloop()