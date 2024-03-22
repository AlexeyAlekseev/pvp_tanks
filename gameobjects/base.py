"""
base.py: This module is part of the gameobjects package.

The base module contains the fundamental classes and functions
that underpin the other modules in the gameobjects package.
"""

from abc import ABC
from typing import List, Any


class GameObject(ABC):
    """This is an abstract base class representing a game object.

    Attributes:
        objects_list (list): A list containing all game objects.

    Methods:
         __init__(objects_list): Initializes the game object by adding
    itself to the objects_list.
        update(): Abstract method to update the game object.
        draw(): Abstract method to draw the game object.
        damage(**kwargs): Abstract method to handle damage to the game object.
    """
    objects_list = []

    def __init__(self, objects_list: List[Any]) -> None:
        """Initialize the class with a list of objects.

        Args:
            objects_list (List[Any]): A list of objects to be initialized with.

        Returns:
            None: This method does not return anything.
        """
        objects_list.append(self)
        self.objects_list = objects_list

    def update(self) -> None:
        """
        Update method.

        This method is used to update a certain data or perform a specific
        action.

        Parameters:
            self: The object itself.

        Returns:
            None.

        Raises: NotImplementedError: This method is not implemented and
        should be overridden by child classes.
        """
        raise NotImplementedError

    def draw(self) -> None:
        """
        Method to draw the object.

        :param self: The object instance.
        :type self: object
        :return: None
        :rtype: None
        """
        raise NotImplementedError

    def damage(self, value: int, **kwargs: Any) -> None:
        """
        Damage the entity with the specified amount of damage.

        :param value: The amount of damage to be inflicted on the entity.
        :type value: int
        :param **kwargs: Additional keyword arguments for customization.
        (Optional)
        :type **kwargs: Any
        :return: None
        :rtype: None
        """
        raise NotImplementedError
