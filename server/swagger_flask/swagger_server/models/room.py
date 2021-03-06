# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Room(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, room_id: str=None, building: str=None, chairs: int=None, chairs_max: int=None, tables_exam: int=None, pc: int=None, category: str=None):  # noqa: E501
        """Room - a model defined in Swagger

        :param room_id: The room_id of this Room.  # noqa: E501
        :type room_id: str
        :param building: The building of this Room.  # noqa: E501
        :type building: str
        :param chairs: The chairs of this Room.  # noqa: E501
        :type chairs: int
        :param chairs_max: The chairs_max of this Room.  # noqa: E501
        :type chairs_max: int
        :param tables_exam: The tables_exam of this Room.  # noqa: E501
        :type tables_exam: int
        :param pc: The pc of this Room.  # noqa: E501
        :type pc: int
        :param category: The category of this Room.  # noqa: E501
        :type category: str
        """
        self.swagger_types = {
            'room_id': str,
            'building': str,
            'chairs': int,
            'chairs_max': int,
            'tables_exam': int,
            'pc': int,
            'category': str
        }

        self.attribute_map = {
            'room_id': 'roomId',
            'building': 'building',
            'chairs': 'chairs',
            'chairs_max': 'chairs_max',
            'tables_exam': 'tables_exam',
            'pc': 'pc',
            'category': 'category'
        }

        self._room_id = room_id
        self._building = building
        self._chairs = chairs
        self._chairs_max = chairs_max
        self._tables_exam = tables_exam
        self._pc = pc
        self._category = category

    @classmethod
    def from_dict(cls, dikt) -> 'Room':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Room of this Room.  # noqa: E501
        :rtype: Room
        """
        return util.deserialize_model(dikt, cls)

    @property
    def room_id(self) -> str:
        """Gets the room_id of this Room.


        :return: The room_id of this Room.
        :rtype: str
        """
        return self._room_id

    @room_id.setter
    def room_id(self, room_id: str):
        """Sets the room_id of this Room.


        :param room_id: The room_id of this Room.
        :type room_id: str
        """
        if room_id is None:
            raise ValueError("Invalid value for `room_id`, must not be `None`")  # noqa: E501

        self._room_id = room_id

    @property
    def building(self) -> str:
        """Gets the building of this Room.


        :return: The building of this Room.
        :rtype: str
        """
        return self._building

    @building.setter
    def building(self, building: str):
        """Sets the building of this Room.


        :param building: The building of this Room.
        :type building: str
        """
        if building is None:
            raise ValueError("Invalid value for `building`, must not be `None`")  # noqa: E501

        self._building = building

    @property
    def chairs(self) -> int:
        """Gets the chairs of this Room.


        :return: The chairs of this Room.
        :rtype: int
        """
        return self._chairs

    @chairs.setter
    def chairs(self, chairs: int):
        """Sets the chairs of this Room.


        :param chairs: The chairs of this Room.
        :type chairs: int
        """
        if chairs is None:
            raise ValueError("Invalid value for `chairs`, must not be `None`")  # noqa: E501

        self._chairs = chairs

    @property
    def chairs_max(self) -> int:
        """Gets the chairs_max of this Room.


        :return: The chairs_max of this Room.
        :rtype: int
        """
        return self._chairs_max

    @chairs_max.setter
    def chairs_max(self, chairs_max: int):
        """Sets the chairs_max of this Room.


        :param chairs_max: The chairs_max of this Room.
        :type chairs_max: int
        """

        self._chairs_max = chairs_max

    @property
    def tables_exam(self) -> int:
        """Gets the tables_exam of this Room.


        :return: The tables_exam of this Room.
        :rtype: int
        """
        return self._tables_exam

    @tables_exam.setter
    def tables_exam(self, tables_exam: int):
        """Sets the tables_exam of this Room.


        :param tables_exam: The tables_exam of this Room.
        :type tables_exam: int
        """
        if tables_exam is None:
            raise ValueError("Invalid value for `tables_exam`, must not be `None`")  # noqa: E501

        self._tables_exam = tables_exam

    @property
    def pc(self) -> int:
        """Gets the pc of this Room.


        :return: The pc of this Room.
        :rtype: int
        """
        return self._pc

    @pc.setter
    def pc(self, pc: int):
        """Sets the pc of this Room.


        :param pc: The pc of this Room.
        :type pc: int
        """
        if pc is None:
            raise ValueError("Invalid value for `pc`, must not be `None`")  # noqa: E501

        self._pc = pc

    @property
    def category(self) -> str:
        """Gets the category of this Room.


        :return: The category of this Room.
        :rtype: str
        """
        return self._category

    @category.setter
    def category(self, category: str):
        """Sets the category of this Room.


        :param category: The category of this Room.
        :type category: str
        """
        if category is None:
            raise ValueError("Invalid value for `category`, must not be `None`")  # noqa: E501

        self._category = category
