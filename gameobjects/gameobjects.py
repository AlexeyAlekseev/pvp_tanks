"""
gameobjects.py: This module is part of the game project.

The gameobjects module defines the various interactive elements within the
game's environment. It encapsulates functionalities related to the behavior
of these elements, including how they interact with each other, the game
environment, and the player's actions.

This module may include classes for game characters, enemies, weapons,
power-ups, and interactive environment components.
"""

from gameobjects.base import GameObject
from gameobjects.pygame_ui import (
    screen,
    image_bangs,
    image_bonuses,
    image_tank, sound_effects
)


class Bang(GameObject):
    """
    Bang

    A class representing an explosion in a game.

    Attributes:
    - px (int): x-coordinate of the explosion's position.
    - py (int): y-coordinate of the explosion's position.
    - objects_list (list): List of game objects.

    Methods:
        - __init__(px, py, objects_list): Initializes a new instance of
    the Bang class.
        - get_rect(): Updates the rectangle position of the
    explosion based on its current position.
        - update(): Updates the frame
    and removes the explosion from the objects_list if necessary.
        - draw():
    Draws the explosion image on the screen.
        - damage(value): Applies damage
    to the explosion.

    """
    def __init__(self, px, py, objects_list: list):
        super().__init__(objects_list)
        self.type = 'bang'
        self.px, self.py = px, py
        self.frame = 0
        self.image = image_bangs[0]
        self.rect = self.image.get_rect(center=(self.px, self.py))

    def get_rect(self):
        """
        Sets the position of the rectangle based on the given image center
        coordinates.

        Parameters:
            self (object): The instance of the class.

        Return:
            None

        """
        self.rect = self.image.get_rect(center=(self.px, self.py))

    def update(self):
        """
        Updates the object state.

        This method increases the 'frame' attribute of the object by 0.3. If
        the 'frame' attribute becomes equal to or greater than 3, the object
        is removed from the 'objects_list' attribute *.

        Parameters:
            N/A

        Returns:
            N/A
        """
        self.frame += 0.3
        if self.frame >= 3:
            self.objects_list.remove(self)

    def draw(self):
        """
        Draws an image onto the screen at a specific position.

        :param self: The current instance of the class.
        :return: None

        """
        image = image_bangs[int(self.frame)]
        rect = image.get_rect(center=(self.px, self.py))
        screen.blit(image, rect)

    def damage(self, value, rank=None):
        pass


class Bonus(GameObject):
    """

    Class: Bonus(GameObject)

    This class represents a bonus object in the game. It is a subclass of the
    GameObject class.

    Attributes:
    - type (str): The type of the object, set to 'bonus'.
    - image (Surface): The image of the bonus.
    - rect (Rect): The rectangular area occupied by the bonus on the screen.
    - timer (int): The timer value for the bonus.
    - bonus_index (int): The index of the bonus.
    - objects_list (list): The list of game objects.

    Methods:
    - __init__(self, px, py, bonus_index, objects_list: list)
        Initializes a new instance of the Bonus class.
        Parameters:
            - px (int): The x-coordinate of the bonus's position.
            - py (int): The y-coordinate of the bonus's position.
            - bonus_index (int): The index of the bonus.
            - objects_list (list): The list of game objects.

    - update(self)
        Updates the bonus object.
        If the timer is greater than 0, decreases the timer by 1.
        Otherwise, removes the bonus from the objects list.
        Executes the corresponding bonus action based on the bonus index.

    - star(self)
        Executes the star bonus action.
        If the bonus collides with a tank object, increases the tank's rank, speed, and shoot delay.

    - bonus_tank(self)
        Executes the tank bonus action.
        If the bonus collides with a tank object, increases the tank's lives.

    - bonus_helmet(self)
        Executes the helmet bonus action.
        If the bonus collides with a tank object, increases the tank's hit points.

    - draw(self)
        Draws the bonus object on the screen.

    - damage(self, value, rank=None)
        Does nothing. This method is not implemented in the Bonus class.

    """
    def __init__(self, px, py, bonus_index, objects_list: list):
        super().__init__(objects_list)
        self.type = 'bonus'

        self.image = image_bonuses[bonus_index]
        self.rect = self.image.get_rect(center=(px, py))

        self.timer = 400
        self.bonus_index = bonus_index

    def update(self):
        """
            Updates the object's timer and performs a bonus action if applicable.

            This method is responsible for updating the object's timer
            attribute. If the timer is greater than 0, it decrements the
            timer by 1. Otherwise, it removes the object from the objects
            *_list attribute of the class.

            The method also defines a dictionary called bonus_actions, which
            maps each bonus_index value to a corresponding bonus action method.
            The bonus actions are as follows:
            - 0: Invokes the star method.
            - 1: Invokes the bonus_tank method.
            - 2: Invokes the bonus_helmet method.

            If the bonus_index is in the bonus_actions dictionary, it calls
            the corresponding bonus action method.

            Parameters:
                None

            Returns:
                None
            """
        if self.timer > 0:
            self.timer -= 1
        else:
            self.objects_list.remove(self)

        bonus_actions = {
            0: self.star,
            1: self.bonus_tank,
            2: self.bonus_helmet
        }

        if self.bonus_index in bonus_actions:
            bonus_actions[self.bonus_index]()

    def star(self):
        """

            Method Name: star

            Description: This method is used to increase the rank and
            attributes of a tank object when it collides with a star object.

            Parameters:
                - self: The current instance of the class.

            Return: None

        """
        for obj in self.objects_list:
            if obj.type == 'tank' and self.rect.colliderect(obj.rect):
                sound_effects["star"].play()
                if obj.rank < len(image_tank) - 1:
                    obj.rank += 1
                    obj.speed += 0.3
                    obj.shoot_delay -= 10
                else:
                    pass
                self.objects_list.remove(self)

    def bonus_tank(self):
        """
        Increments the lives of a tank object if it intersects with
        the bonus tank.

        Parameters:
        - self (object): The instance of the current class.

        Return:
        None
        """
        for obj in self.objects_list:
            if obj.type == 'tank' and self.rect.colliderect(obj.rect):
                sound_effects["bonus"].play()
                if obj.lives < 6:
                    obj.lives += 1
                else:
                    pass
                self.objects_list.remove(self)

    def bonus_helmet(self):
        """
        Increase the hit points of a tank object if the player's helmet
        collides with it.

        :param self: The current instance of the game object
        :return: None
        """
        for obj in self.objects_list:
            if obj.type == 'tank' and self.rect.colliderect(obj.rect):
                sound_effects["bonus"].play()
                if obj.hit_points < 9:
                    obj.hit_points += 1
                else:
                    pass
                self.objects_list.remove(self)

    def draw(self):
        """
        Draws the image on the screen object based on the timer.

        If the remainder of self.timer divided by 30 is less than 15,
        the image will be blitted onto the screen at the position specified
        by self.rect.

        Parameters:
            self: The instance of the class.

        Returns:
            None
        """
        if self.timer % 30 < 15:
            screen.blit(self.image, self.rect)

    def damage(self, value, rank=None):
        pass
