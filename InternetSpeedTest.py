import speedtest # for speedtest
import tkinter as tk # for GUI
import threading # for threading
import requests # for get public ip or request
import asyncio # for async and await

from colorVariables import *  # for color variable
from hoverEvent import * # for hover event



def startApp():
	global title,startButton,app

	app = tk.Tk()
	app.title("Internet Speed Test")
	app.minsize(800,480)
	#app.resizable(False, False)
	app.attributes("-fullscreen", False)
	app.configure(bg="#242424")



	# Button
	startButton = tk.Button(app, text="START", bg=colorBG, fg=colorFG, activebackground=colorBG, activeforeground="#404040", font=("Arial", 40, "bold"), borderwidth=0, command=lambda: threading.Thread(target = startTest).start())
	startButton.place(relx=0.5, rely=0.5, anchor="center")

	# Label
	title = tk.Label(app, text="Internet Speed Test", bg=colorBG, fg=colorFG, font=("Lato", 20, "bold"))
	title.place(relx=0.5, rely=0.05, anchor="center")

	# Static keybind
	app.bind("<Escape>", lambda event: app.destroy())


def startTest():
	global st
	global topLeftFrame,resultFrame
	global displayDownloadTitle,displayDownloadResult,displayDownloadUnit,displayUploadTitle,displayUploadResult,displayUploadUnit,displayPingTitle,displayPingResult,displayPingUnit
	global displayISPname,displayServerInfo,displayPublicIP
	global retryButton,retryLabel

	# Check internet connection
	try:
		st = speedtest.Speedtest()
	except:
		return startTestFailed()


	# Destroy start button
	try:startButton.destroy()
	except:pass
	

	# Top left frame
	topLeftFrame = tk.Frame(app, bg=colorBG, width=400, height=100)
	topLeftFrame.place(relx=0.15, rely=0.2, anchor="w")

	# Internet info
	bestServer = st.get_best_server()
	## ISP name
	ISPname = bestServer["sponsor"]

	displayISPname = tk.Label(topLeftFrame, text=ISPname, bg=colorBG, fg=colorFG, font=("Arial", 15, "bold"))
	displayISPname.place(relx=0, rely=0.3, anchor="w")

	## Server name
	serverName = bestServer["name"]
	serverLocation = bestServer["country"]

	displayServerInfo = tk.Label(topLeftFrame, text=serverName+", "+serverLocation, bg=colorBG, fg=colorFG, font=("Arial", 15, "bold"))
	displayServerInfo.place(relx=0, rely=0.7, anchor="w")

	### Hover event
	# Hover text
	ISPhoverText = "This data may not be accurate if you're using a VPN or proxy."
	hoverTextWidgetEvent([displayISPname, displayServerInfo], ISPhoverText, colorBG, colorFG, "Arial", 10, "left", 0.5, "#FFFFFF")

	## Public IP (this task can be very slow. so i use function for threading)
	displayPublicIP = tk.Label(app, text="Detecting...", bg=colorBG, fg=colorFG, font=("Arial", 15, "bold"))
	displayPublicIP.place(relx=0.85, rely=0.2, anchor="e")
	def getPublicIP():
		global displayPublicIP
		publicIP = requests.get("https://api.ipify.org").text

		displayPublicIP.config(text=publicIP)

	# Result frame
	resultFrame = tk.Frame(app, bg=colorBG, width=800, height=200)
	resultFrame.place(relx=0.5, rely=0.55, anchor="center")

	# Internet speed
	## Download
	displayDownloadTitle = tk.Label(resultFrame, text="Download", bg=colorBG, fg=colorFG, font=("Lato", 20))
	displayDownloadTitle.place(relx=0.25, rely=0.2, anchor="center")

	displayDownloadResult = tk.Label(resultFrame, text="-", bg=colorBG, fg=colorFG, font=("Lato", 40))
	displayDownloadResult.place(relx=0.25, rely=0.5, anchor="center")

	displayDownloadUnit = tk.Label(resultFrame, text="Mb/s", bg=colorBG, fg=colorFG, font=("Lato", 15))
	displayDownloadUnit.place(relx=0.25, rely=0.75, anchor="center")

	## Upload
	displayUploadTitle = tk.Label(resultFrame, text="Upload", bg=colorBG, fg=colorFG, font=("Lato", 20))
	displayUploadTitle.place(relx=0.5, rely=0.2, anchor="center")

	displayUploadResult = tk.Label(resultFrame, text="-", bg=colorBG, fg=colorFG, font=("Lato", 40))
	displayUploadResult.place(relx=0.5, rely=0.5, anchor="center")

	displayUploadUnit = tk.Label(resultFrame, text="Mb/s", bg=colorBG, fg=colorFG, font=("Lato", 15))
	displayUploadUnit.place(relx=0.5, rely=0.75, anchor="center")

	## Ping
	displayPingTitle = tk.Label(resultFrame, text="Ping", bg=colorBG, fg=colorFG, font=("Lato", 20))
	displayPingTitle.place(relx=0.75, rely=0.2, anchor="center")

	displayPingResult = tk.Label(resultFrame, text="-", bg=colorBG, fg=colorFG, font=("Lato", 40))
	displayPingResult.place(relx=0.75, rely=0.5, anchor="center")

	displayPingUnit = tk.Label(resultFrame, text="ms", bg=colorBG, fg=colorFG, font=("Lato", 15))
	displayPingUnit.place(relx=0.75, rely=0.75, anchor="center")

	# Display public IP
	threading.Thread(target = getPublicIP).start()

	# Continue to get result
	getResult()


def startTestFailed():
	global noConnectionTitle

	startButton.destroy()
	
	noConnectionTitle = tk.Label(app, text="You're not connected to the internet!", bg=colorBG, fg=colorSlow, font=("Lato", 18))
	noConnectionTitle.place(relx=0.5, rely=0.5, anchor="center")

	replaceWithRetryButton()


def retry():
	replaceWithRetryLabel()
	try:
		noConnectionTitle.destroy()
	except:
		displayISPname.destroy();displayServerInfo.destroy();displayPublicIP.destroy()
		resultFrame.destroy()
	
	startTest()


def replaceWithRetryLabel():
	# Replace retry button with label
	try:retryButton.destroy()
	except:pass
	retryLabel = tk.Label(app, text="RETRY (Enter)", bg=colorBG, fg="#404040", font=("Lato", 15))
	retryLabel.place(relx=0.5, rely=0.9, anchor="center")
	app.unbind("<Return>")
	app.bind("<Return>", None)


def replaceWithRetryButton():
	# Replace retry label with button
	try:retryLabel.destroy()
	except:pass
	retryButton = tk.Button(app, text="RETRY (Enter)", bg=colorBG, fg=colorFG, activebackground=colorBG, activeforeground="#404040", font=("Arial",15), borderwidth=0, command=lambda: threading.Thread(target = retry).start())
	retryButton.place(relx=0.5, rely=0.9, anchor="center")
	app.unbind("<Return>")
	app.bind("<Return>", lambda event: threading.Thread(target = retry).start())


def getResult():
	async def getResultDownload():
		global downloadSpeed
		downloadSpeed = round(st.download() / 1000000, 2)
		displayDownloadResult.config(text=str(downloadSpeed))
		changeColor("download")

	async def getResultUpload():
		global uploadSpeed
		uploadSpeed = round(st.upload() / 1000000, 2)
		displayUploadResult.config(text=str(uploadSpeed))
		changeColor("upload")

	async def getResultPing():
		global ping
		ping = round(st.results.ping, 2)
		displayPingResult.config(text=int(ping))
		changeColor("ping")

	async def getResult():
		await asyncio.gather(getResultDownload(), getResultUpload(), getResultPing())
		replaceWithRetryButton()

	asyncio.run(getResult())


def changeColor(type):
	# Change connection text color
	if type == "download":
		if downloadSpeed >= 20 :displayDownloadResult.config(fg=colorFast)
		elif downloadSpeed >= 5 :displayDownloadResult.config(fg=colorAverage)
		else :displayDownloadResult.config(fg=colorSlow)

	if type == "upload":
		if uploadSpeed >= 20 :displayUploadResult.config(fg=colorFast)
		elif uploadSpeed >= 5 :displayUploadResult.config(fg=colorAverage)
		else :displayUploadResult.config(fg=colorSlow)

	if type == "ping":
		if ping >= 100 :displayPingResult.config(fg=colorSlow)
		elif ping >= 50 :displayPingResult.config(fg=colorAverage)
		else :displayPingResult.config(fg=colorFast)

	app.update()


startApp()
app.mainloop()