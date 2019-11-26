import tkinter as tk
import random


class Controller(object):
    """
    A class to control the movement of the snake in the game
    """
    def __init__(self, screen):
        """
        Binds the arrow keys to the game canvas.

        Parameters:
             screen (Canvas): The canvas for the Snake game.
        """
        self._screen = screen
        screen.bind("<Left>", self.left_move)
        screen.bind("<Right>", self.right_move)
        screen.bind("<Up>", self.up_move)
        screen.bind("<Down>", self.down_move)
        screen.focus_set()

    def left_move(self, e):
        """Changes the direction of the snake head to 'left' when the left key is pressed."""
        if self._screen.get_direction() == 'right':
            pass
        else:
            self._screen.set_direction('left')
            self._screen.delete(self._screen.get_snake_id())
            self._screen.change_x_axis(-10)
            self._screen.create_snake_head()

    def right_move(self, e):
        """Changes the direction of the snake head to 'right' when the right key is pressed."""
        if self._screen.get_direction() == 'left':
            pass
        else:
            self._screen.set_direction('right')
            self._screen.delete(self._screen.get_snake_id())
            self._screen.change_x_axis(10)
            self._screen.create_snake_head()

    def up_move(self, e):
        """Changes the direction of the snake head to 'up' when the up key is pressed."""
        if self._screen.get_direction() == 'down':
            pass
        else:
            self._screen.set_direction('up')
            self._screen.delete(self._screen.get_snake_id())
            self._screen.change_y_axis(-10)
            self._screen.create_snake_head()

    def down_move(self, e):
        """Changes the direction of the snake head to 'down' when the down key is pressed."""
        if self._screen.get_direction() == 'up':
            pass
        else:
            self._screen.set_direction('down')
            self._screen.delete(self._screen.get_snake_id())
            self._screen.change_y_axis(10)
            self._screen.create_snake_head()


class Screen(tk.Canvas):
    """
    A canvas class that displays the game
    """
    def __init__(self, master):
        """
        Construct the canvas of the game on the root window.

        Parameters:
            master (tk.Tk): The root window for the Snake game.
        """
        super().__init__(master)
        self._master = master
        self._width = 500
        self._height = 300
        self.config(bg='white', width=self._width, height=self._height)
        self._x = self._width
        self._y = self._height
        self._game_status = True
        self._direction = 'right'

        self._snake = self.create_oval
        self.create_snake_head()
        self._snack = self.create_oval
        self.create_snack()

        self._tail_number = 0
        self._tail_list = []
        self._tail = self.create_line([(0, 0), (0, 0)])

    def get_snake_id(self):
        """Returns the id of the snake head.

        Returns:
            snake (int): The id of the snake head.
        """
        return self._snake

    def get_direction(self):
        """Returns the current direction of the snake head.

        Returns:
            direction (str): The direction of the snake head.
        """
        return self._direction

    def get_tail_number(self):
        """Returns the length of the tail of the snake.

        Returns:
            tail_number (int): The current length of the tail.
        """
        return self._tail_number

    def get_game_status(self):
        """Returns the current status of the game. True if the game is running,
        False otherwise.

        Returns:
            game_status (bool): The current status of the game
        """
        return self._game_status

    def set_direction(self, direction):
        """
        Changes the movement direction of the snake

        Parameter:
            direction (str): The new direction of the snake.
        """
        self._direction = direction

    def change_x_axis(self, change):
        """
        Changes the value of the x-axis.

        Parameter:
            change (int): Changes the x-axis by this value.
        """
        self._x += change

    def change_y_axis(self, change):
        """
        Changes the value of the y-axis.

        Parameter:
            change (int): Changes the y-axis by this value.
        """
        self._y += change

    def check_collision(self):
        """
        Checks for any collision between the snake head and its tail
        or with the snack in the game.
        """
        snake_coords = self.coords(self._snake)
        snack_coords = self.coords(self._snack)
        x1, y1, x2, y2 = snack_coords
        xx1, yy1, xx2, yy2 = snake_coords

        # Checks for collision between the snake head and the snake
        if xx1 <= x1 <= xx2:
            if yy1 <= y1 <= yy2:
                self.delete(self._snack)
                self._tail_number += 10

                self.create_snack()
        elif xx1 <= x2 <= xx2:
            if yy1 <= y2 <= yy2:
                self.delete(self._snack)
                self._tail_number += 10
                self.create_snack()

        # Checks for collision between the snake head and the tail
        for tail in self._tail_list:
            tail_coords = self.coords(tail)
            x1, y1, x2, y2 = tail_coords

            if xx1 <= x1 <= xx2:
                if yy1 <= y1 <= yy2:
                    self._game_status = False
            elif xx1 <= x2 <= xx2:
                if yy1 <= y2 <= yy2:
                    self._game_status = False

    def create_snack(self):
        """
        Creates the snack in the game based on random coordinates.
        """
        random_x = random.randint(0, self._width-5)
        random_y = random.randint(0, self._height-5)
        self._snack = self.create_oval(random_x, random_y, random_x + 5, random_y + 5, fill='red', outline='red')

    def create_snake_head(self):
        """
        Creates the snake head in the game.
        """
        circle_size = (self._x / 2, self._y / 2)
        x, y = circle_size

        # Resets the x and y coordinates of the snake head if it makes contact
        # with the boundaries of the game.
        if (self._width*2) < self._x+10:
            self._x = 0
        elif self._x < 0:
            self._x = (self._width*2)

        if (self._height*2) < self._y+10:
            self._y = 0
        elif self._y < 0:
            self._y = (self._height*2)

        self._snake = self.create_oval(x, y, x + 10, y+10, fill='black')

    def create_tail(self):
        """
        Creates and keeps track of the tail of the snake based on the current score
        as well as the movement direction.
        """
        snake_coords = self.coords(self._snake)
        x1, y1, x2, y2 = snake_coords
        x = (x1+x2)/2
        y = (y1+y2)/2
        tail_size = 10
        self._tail_list += [self._tail, ]

        if self._direction == 'right':
            self._tail = self.create_line([(x-tail_size, y), (x, y)])
        elif self._direction == 'left':
            self._tail = self.create_line([(x+tail_size, y), (x, y)])
        elif self._direction == 'up':
            self._tail = self.create_line([(x, y+tail_size), (x, y)])
        else:
            self._tail = self.create_line([(x, y-tail_size), (x, y)])

        # Removes any tail-lines created after the length of the tail exceeds the score
        if len(self._tail_list) > self._tail_number:
            self.delete(self._tail_list.pop(0))


class SnakeGame(object):
    """
    A game of Snake Xenzia
    """
    def __init__(self, master):
        """
        Construct the main game window

        Parameters:
            master (tk.Tk): The root window for the Snake game.
        """
        self._master = master
        self._master.title("Snake Game")

        self._canvas = Screen(master)
        self._controls = Controller(self._canvas)
        self._canvas.pack(side=tk.BOTTOM)
        self._score = tk.Label(master, bg='black', fg='white')
        self._score.pack(fill='x')

        self._speed = 50
        self._master.after(self._speed, self.animation)

    def animation(self):
        """
        Animates and constructs the snake head and tail. Checks the
        the score and game status at every cycle and updates accordingly.
        """
        if self._canvas.get_direction() == 'right':
            self._controls.right_move('')
        elif self._canvas.get_direction() == 'left':
            self._controls.left_move('')
        elif self._canvas.get_direction() == 'up':
            self._controls.up_move('')
        else:
            self._controls.down_move('')

        self._canvas.check_collision()

        if not self._canvas.get_game_status():
            self.game_end()

        self._canvas.create_tail()
        self.update_score()
        speed = self._speed - (self._canvas.get_tail_number()//10)
        self._master.after(speed, self.animation)

    def update_score(self):
        """
        Updates the game score on the label widget of the main window.
        """
        self._score.config(text=f'Score: {self._canvas.get_tail_number()}')

    def game_end(self):
        """
        Hides the game canvas and increases the size of the score label.
        """
        self._canvas.pack_forget()
        self._score.config(font='Courier, 30')
        self._score.pack(ipadx=200, ipady=200)


if __name__ == '__main__':
    root = tk.Tk()
    game = SnakeGame(root)
    root.resizable(False, False)
    root.mainloop()
