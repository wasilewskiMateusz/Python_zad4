from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import math
import random

init_pos_limit = 200
sheep_move_dist = 10
wolf_move_dist = 20

side = 2 * 1.5 * init_pos_limit
half_side = side / 2

number_of_sheeps = 0
sheeps = []
sheeps_points = []
wolf = [[half_side, half_side]]
wolf_point = None


def find_nearest_point():
    distances = []
    for i in range(len(sheeps)):
        if sheeps[i] is not None:
            distances.append(math.sqrt((wolf[0][0] - sheeps[i][0]) ** 2 + (wolf[0][1] - sheeps[i][1]) ** 2))
        else:
            distances.append(None)
    return sheeps[distances.index(min(dis for dis in distances if dis is not None))]


def move_sheeps():
    direction = [-1, 1]
    for i in range(len(sheeps)):
        if sheeps[i] is not None:
            sheeps[i][random.randrange(2)] += (direction[random.randrange(2)] * sheep_move_dist)

            canvas.coords(sheeps_points[i], sheeps[i][0] - 2, sheeps[i][1] - 2, sheeps[i][0] + 2, sheeps[i][1] + 2)


def move_wolf():
    closest_sheep = find_nearest_point()
    dist_to_closest_sheep = math.sqrt((wolf[0][0] - closest_sheep[0]) ** 2 + (wolf[0][1] - closest_sheep[1]) ** 2)
    if dist_to_closest_sheep < wolf_move_dist:
        print("Sheep {} has been eaten!".format(closest_sheep[2]))
        sheep_index = sheeps.index(closest_sheep)
        sheeps[sheep_index] = None
        canvas.delete(sheeps_points[sheep_index])
        global number_of_sheeps
        number_of_sheeps -= 1
        var.set(f'Number of sheep: {number_of_sheeps}')
        if number_of_sheeps is 0:
            messagebox.showinfo('Information', 'The last sheep has been eaten!')
    else:
        wolf[0][0] = wolf[0][0] - ((wolf_move_dist * (wolf[0][0] - closest_sheep[0])) / dist_to_closest_sheep)
        wolf[0][1] = wolf[0][1] - ((wolf_move_dist * (wolf[0][1] - closest_sheep[1])) / dist_to_closest_sheep)
    canvas.coords(wolf_point, wolf[0][0] - 2, wolf[0][1] - 2, wolf[0][0] + 2, wolf[0][1] + 2)


def add_sheep(event):
    sheeps_points.append(canvas.create_oval(event.x - 2, event.y - 2, event.x + 2, event.y + 2, fill='blue'))
    sheeps.append([event.x, event.y, len(sheeps)+1])
    global  number_of_sheeps
    number_of_sheeps += 1
    var.set(f'Number of sheep: {number_of_sheeps}')


def change_wolf_position(event):
    canvas.coords(wolf_point, event.x - 2, event.y - 2, event.x + 2, event.y + 2)
    global wolf
    wolf = [[event.x, event.y]]


def step():
    if number_of_sheeps is not 0:
        move_sheeps()
        move_wolf()
    else:
        messagebox.showinfo('Information', 'There are no sheep on field.')


def reset():
    canvas.delete("all")
    global wolf_point, sheeps, sheeps_points
    wolf_point = canvas.create_oval(half_side-2, half_side-2, half_side+2, half_side+2, fill='red')
    canvas.create_line(0, half_side, side, half_side, dash=(2, 2))  # x-axis
    canvas.create_line(half_side, 0, half_side, side, dash=(2, 2))  # y-axis
    sheeps = []
    sheeps_points = []
    global number_of_sheeps
    number_of_sheeps = 0
    var.set(f'Number of sheep: {number_of_sheeps}')


if __name__ == '__main__':
    window = Tk()
    window.title("Task 4")
    size = '{0}x{1}'.format(int(side), int(side)+60)
    window.geometry(size)
    window.resizable(False, False)

    canvas = Canvas(window, height=side, width=side, bg='green')

    var = StringVar()
    var.set(f'Number of sheep: {number_of_sheeps}')
    label = Label(window, textvariable=var)
    label.pack()
    canvas.create_line(0, half_side, side, half_side, dash=(2, 2))  # x-axis
    canvas.create_line(half_side, 0, half_side, side, dash=(2, 2))  # y-axis
    canvas.bind('<Button-1>', add_sheep)  # sheeps creation
    wolf_point = canvas.create_oval(half_side-2, half_side-2, half_side+2, half_side+2, fill='red')  # wolf creation
    canvas.bind('<Button-2>', change_wolf_position)  # changing the position of the wolf
    canvas.pack()
    step_button = ttk.Button(window, text='Step', command=step).pack(side=LEFT)
    reset_button = ttk.Button(window, text='Reset', command=reset).pack(side=RIGHT)
    window.mainloop()



