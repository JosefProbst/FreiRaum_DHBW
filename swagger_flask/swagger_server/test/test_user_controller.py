# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.lecture import Lecture  # noqa: E501
from swagger_server.models.model_class import ModelClass  # noqa: E501
from swagger_server.models.room import Room  # noqa: E501
from swagger_server.test import BaseTestCase


class TestUserController(BaseTestCase):
    """UserController integration test stubs"""

    def test_search_class_plan(self):
        """Test case for search_class_plan

        Suche in den lokalen RAPLA-Daten nach Vorlesungsplänen
        """
        response = self.client.open(
            '/FreiRaum/FreiRaum/1.0.0/classes/{classId}'.format(classId='classId_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_search_classes(self):
        """Test case for search_classes

        Suche in den lokalen RAPLA-Daten nach allen Kursen
        """
        response = self.client.open(
            '/FreiRaum/FreiRaum/1.0.0/classes',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_search_room_plan(self):
        """Test case for search_room_plan

        Suche in den lokalen RAPLA-Daten nach Raumbelegungsplänen
        """
        response = self.client.open(
            '/FreiRaum/FreiRaum/1.0.0/rooms/{roomId}'.format(roomId='roomId_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_search_rooms(self):
        """Test case for search_rooms

        Suche in den lokalen RAPLA-Daten nach allen/freien Räumen
        """
        query_string = [('starttime', 'starttime_example'),
                        ('endtime', 'endtime_example'),
                        ('category', 'category_example')]
        response = self.client.open(
            '/FreiRaum/FreiRaum/1.0.0/rooms',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
