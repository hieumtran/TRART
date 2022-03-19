from tkinter import *

root = Tk()
root.title('Codemy.com')
root.iconbitmap("dnd.ico")
root.geometry('800x600')

w = 600
h = 400
x = w / 2
y = h / 2

myCanvas = Canvas(root, width = w, heigh = h, bg = "white")
myCanvas.pack(pady = 20)


img = PhotoImage(file = r'C:\Users\Tri Nguyen\Desktop\TenzerHackRacs\building\something.png')
myImage = myCanvas.create_image(260, 125, anchor = NW, image = img)


def move(e):
    global img
    img = PhotoImage(file = r'C:\Users\Tri Nguyen\Desktop\TenzerHackRacs\building\something.png')
    myImage = myCanvas.create_image(e.x, e.y, image = img)
    myLabel.config(text = 'Coordinates: x|' + str(e.x) + " y|" + str(e.y))



#root.bind("<Left>", left)
#root.bind("<Right>", right)
#root.bind("<Up>", up)
#root.bind("<Down>", down)

myLabel = Label(root, text = '')
myLabel.pack(pady = 20)

myCanvas.bind('<B1-Motion>', move) 

root.mainloop()