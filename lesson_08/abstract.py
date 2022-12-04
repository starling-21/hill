from abc import ABC, abstractmethod
from random import choice


class Shape(ABC):
    @abstractmethod
    def draw(self):
        pass


class Rectangle(Shape):
    """Change me"""

    def draw(self):
        print("----\n|   |\n----")


class Circle(Shape):
    """Change me"""

    def draw(self):
        print(" --\n-  -\n --")


def get_shape() -> Shape:
    """
    This function should return any instance of a Shape class
    In our example it is Rectangle or Circle
    """
    options: list[Shape] = [Rectangle(), Circle()]
    return choice(options)


def main():
    """
    In Rectangle is used I'd like to see:

    ----
    |  |
    ----

    If Circle is used:
      --
     -  -
      --
    """
    shape: Shape = get_shape()
    shape.draw()


if __name__ == "__main__":
    main()
