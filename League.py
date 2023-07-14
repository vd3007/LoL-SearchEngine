from PIL import ImageTk
import os
import requests
from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
import PIL.Image
import random

root = Tk()
root.geometry("1750x750")
root.title("英雄聯盟搜尋器")
root.iconbitmap("League.ico")
champList = []
champEng = []
champCh = []

ch_url = "https://www.leagueoflegends.com/zh-tw/champions/"

ch_r = requests.get(ch_url)
ch_soup = BeautifulSoup(ch_r.text, 'html.parser')

for link in ch_soup.find_all('span', {'class':'style__Name-n3ovyt-2 cMGedC'}):
	for l in link.find_all('span', {'class':'style__Text-n3ovyt-3 gMLOLF'}):
		s = l.get_text()
		champCh.append(s)

for link in ch_soup.find_all('div', {'class':'style__List-sc-13btjky-2 dLJiol'}):
	for a in link.find_all('a'):
		href = a.get('href')
		if (href[0:17] == "/zh-tw/champions/"):
			s = href[17:].rstrip('/')
			champEng.append(s)

def champ():
	global ch_url
	global list_champ
	global list_skill
	global label_story
	global label_pic
	global champ_img
	global img_files
	global folder_path

	champ_index = list_champ.curselection()
	url = ch_url + champEng[int(champ_index[0])] + "/"
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')

	#champion story 
	for link in soup.find_all('div',{'class':'style__Desc-sc-8gkpub-9 efkwqI'}):
		for l in link.find_all("p", {'data-testid':'overview:description'}):
			story = l.get_text()
			label_story.configure(text = story, justify="left")

	#champion skill
	list_skill.delete(0, 'end')
	skill_text = ''
	pqwer_index = 0
	for link in soup.find_all('div', {'class':'style__AbilityInfo-sc-1bu2ash-6 IhSOT'}):
		for l in link.find_all('li'):
			skill_temp = l.find_all('p', {'class':'style__AbilityInfoItemDesc-sc-1bu2ash-11 iqHSEh'})
			h5 = l.find_all('h5', {'class':'style__AbilityInfoItemName-sc-1bu2ash-10 gUFHLu'})
			tags = [ss.get_text() for ss in skill_temp]
			h5_tags = [ss.get_text() for ss in h5]
			pqwer = ['P', 'Q', 'W', 'E', 'R']
			skill_text += pqwer[pqwer_index] + ' (' + ''.join(h5_tags) + ')：' +' '.join(tags)+'\n\n'
			pqwer_index+=1
			
		for line in skill_text.splitlines():
			list_skill.insert('end', line)

	#champion class
	for link in soup.find_all('li', {'class':'style__SpecsItem-sc-8gkpub-12 hsnFYj'}):
		champ_class = link.find('div', {'class':'style__SpecsItemValue-sc-8gkpub-15 kPaHxk'}).get_text()
	for link in soup.find_all('li', {'class':'style__SpecsItem-sc-8gkpub-12 kZfoPV'}):
		champ_diff = link.find('div', {'class':'style__SpecsItemValue-sc-8gkpub-15 kPaHxk'}).get_text()
	champ_style = f"職業： {champ_class}\n難度： {champ_diff}" 
	label_class.configure(text = champ_style)


	#delete file in folder
	if os.path.isdir("skin"):
		print("already gotten!")
	else:
		print("floder created!")
		os.makedirs("skin")

	for filename in os.listdir("skin"):
		file_path = os.path.join("skin", filename)
		if os.path.isfile(file_path):
			os.remove(file_path)
		elif os.path.isdir(file_path):
			clear_folder(file_path)
			os.rmdir(file_path)

	#download skin into folder
	for link in soup.find_all('div', {'class':'style__Slideshow-gky2mu-2 jQOWwL'}):
		download = [ img for img in link.find_all('img',{'class':'style__NoScriptImg-g183su-0 style__Img-g183su-1 cipsic dBitJH'})]
		download_links = [each.get('src') for each in download]
		for each in download_links:
			if (each[0:8] == "https://"):
				filename="skin/"+each.split('/')[-1]
				print(filename) 
				try:
					urllib.request.urlretrieve(each, filename)
				except:
					print("Error")

	#set champion skin
	folder_path = "skin/"
	img_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
	selected_img = random.choice(img_files)
	image_path = os.path.join(folder_path, selected_img)
	champ_img = ImageTk.PhotoImage(PIL.Image.open(image_path).resize((640,378)))
	

	label_pic = Label(image = champ_img)
	label_story.grid(row = 1, column = 1)
	list_skill.grid(row = 0, column = 2)
	search_btn.grid(row = 1, column = 0)
	label_pic.grid(row = 0, column = 1)
	label_class.grid(row = 1, column = 2)



champ_var = StringVar()
champ_var.set(champCh)

list_champ = Listbox(root, listvariable = champ_var, font = ('',20), relief='groove', bd=5)
list_skill = Listbox(root, width=30, font=('Arial',20))
label_story = Label(root, font=('Arial', 20), width=60, wraplength = 650)
label_pic = Label(root, font=('Arial', 20), width=8)
label_class = Label(root, font=('Arial', 20), width=20)
search_btn = Button(root, text='搜尋', command = champ, font=('Arial', 30))

scrollbary = Scrollbar(root)
scrollbary.grid(row=0, column=3, sticky='ns')
scrollbarx = Scrollbar(root, orient='horizontal')
scrollbarx.grid(row=1, column=2, sticky='e'+'w'+'n')

list_skill.config(yscrollcommand=scrollbary.set)
list_skill.config(xscrollcommand=scrollbarx.set)
scrollbary.config(command=list_skill.yview)
scrollbarx.config(command=list_skill.xview)

list_champ.grid(row = 0, column = 0)
list_skill.grid(row = 0, column = 2)
label_story.grid(row = 1, column = 1)
label_pic.grid(row = 0,column = 1)
label_class.grid(row = 1,column = 2)
search_btn.grid(row = 1, column = 0)

root.mainloop()