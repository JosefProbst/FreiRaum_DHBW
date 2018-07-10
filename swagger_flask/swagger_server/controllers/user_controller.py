import connexion
import six

from swagger_server.models.lecture import Lecture  # noqa: E501
from swagger_server.models.model_class import ModelClass  # noqa: E501
from swagger_server.models.room import Room  # noqa: E501
from swagger_server import util
import swagger_server.controllers.database_controller as db

import json
import os.path
from datetime import datetime, timedelta


valid_room_categories = ["seminarraum", "labor", "meeting", "büro", "projektraum", "all"]
valid_date_format = "%Y-%m-%dT%H:%M:%S"


def search_class_plan(classId):  # noqa: E501
    """Suche in den lokalen RAPLA-Daten nach Vorlesungsplänen

    Eine Anfrage an diese Adresse gibt einen Vorlesungsplan zu einem entsprechenden Kurs zurück # noqa: E501

    :param classId: Übergebe String mit dem Kurskürzel, um den Vorlesungsplan zu bekommen
    :type classId: str

    :rtype: List[Lecture]
    """
    """
        cases:
        the class exists, but there are no lectures (empty list)
        the class exists and there are lectures (list of lectures)
        the class does not exists (404)
    """

    # if the class does not exist, then send an error message

    class_ids = db.get_list_of_class_ids()
    if classId not in class_ids:
        return create_HTTP_error_json("Didn't find the requested class",
                                      "404",
                                      "Not Found"), 404

    # create a list with all lectures of the requested class
    lecture_list = []
    all_lectures = db.get_list_of_lectures()

    for x in range(len(all_lectures)):
        if all_lectures[x]["classId"] == classId:
            if not (datetime.strptime(all_lectures[x]["startTime"], valid_date_format) < datetime.now() + timedelta(days=-14)
                    or datetime.strptime(all_lectures[x]["endTime"], valid_date_format) > datetime.now() + timedelta(days=14)):
                lecture_list.append(Lecture(start_time=all_lectures[x]["startTime"],
                                            end_time=all_lectures[x]["endTime"],
                                            name=all_lectures[x]["name"],
                                            room_id=all_lectures[x]["roomId"],
                                            class_id=all_lectures[x]["classId"]))

    return lecture_list


def search_classes():  # noqa: E501
    """Suche in den lokalen RAPLA-Daten nach allen Kursen

    Eine Anfrage an diese Andresse gibt alle Kurse und deren Kategorien zurück # noqa: E501


    :rtype: List[ModelClass]
    """
    # create a list with all classes
    all_classes = db.get_list_of_classes()
    class_list = []
    for x in range(len(all_classes)):
        class_list.append(ModelClass(class_id=all_classes[x]["classId"],
                                     category=all_classes[x]["category"]))
    return class_list


def search_room_plan(roomId):  # noqa: E501
    """Suche in den lokalen RAPLA-Daten nach Raumbelegungsplänen

     # noqa: E501

    :param roomId: 
    :type roomId: str

    :rtype: List[Lecture]
    """
    """
        cases:
        the room exists, but there are no lectures (empty list)
        the room exists and there are lectures (list of lectures)
        the room does not exists (404)
    """
    # if the room does not exist, then send an error message
    room_ids = db.get_list_of_room_ids()
    if roomId not in room_ids:
        return create_HTTP_error_json("Didn't find the requested class",
                                      "404",
                                      "Not Found"), 404

    # create a list with all lectures of the requested room
    lecture_list = []
    all_lectures = db.get_list_of_lectures()
    for x in range(len(all_lectures)):
        if all_lectures[x]["roomId"] == roomId:
            if not (datetime.strptime(all_lectures[x]["startTime"], valid_date_format) < datetime.now() + timedelta(days=-14)
                    or datetime.strptime(all_lectures[x]["endTime"], valid_date_format) > datetime.now() + timedelta(days=14)):
                lecture_list.append(Lecture(start_time=all_lectures[x]["startTime"],
                                            end_time=all_lectures[x]["endTime"],
                                            name=all_lectures[x]["name"],
                                            room_id=all_lectures[x]["roomId"],
                                            class_id=all_lectures[x]["classId"]))

    return lecture_list


def search_rooms(starttime=None, endtime=None, category=None):  # noqa: E501
    """Suche in den lokalen RAPLA-Daten nach allen/freien Räumen

     # noqa: E501

    :param starttime: 
    :type starttime: str
    :param endtime: 
    :type endtime: str
    :param category: 
    :type category: str

    :rtype: List[Room]
    """
    all_rooms = db.get_list_of_rooms()
    room_list = []

    # /rooms without any arguments should send a list of all rooms
    if starttime is None and endtime is None and category is None:
        for x in range(len(all_rooms)):
            room_list.append(Room(building=all_rooms[x]["building"],
                                  category=all_rooms[x]["category"],
                                  chairs=all_rooms[x]["chairs"],
                                  chairs_max=all_rooms[x]["chairs_max"],
                                  pc=all_rooms[x]["pc"],
                                  room_id=all_rooms[x]["roomId"],
                                  tables_exam=all_rooms[x]["tables_exam"]))
        return room_list

    # a valid specific request on /rooms has to include starttime and endtime
    if starttime is None or endtime is None or category is None:
        return create_HTTP_error_json(
            "category, starttime and endtime must me defined"
            + " valid starttime/endtime:" + valid_date_format
            + " valid categories: " + str(valid_room_categories),
            "400",
            "Bad Request"), 400

    # check if the timestamps have the correct format
    try:
        interval_start = datetime.strptime(starttime, valid_date_format)
        interval_end = datetime.strptime(endtime, valid_date_format)
    except ValueError:
        return create_HTTP_error_json("Invalid date format. Valid:" + valid_date_format,
                                      "400",
                                      "Bad Request"), 400

    if interval_start >= interval_end:
        return create_HTTP_error_json("Invalid dates: starttime >= endtime",
                                      "400",
                                      "Bad Request"), 400

    if interval_start < datetime.now() + timedelta(days=-14) \
            or interval_end > datetime.now() + timedelta(days=14):
        return create_HTTP_error_json("Requests can only be made for the last 14 days, today or coming 14 days",
                                      "403",
                                      "Forbidden"), 403

    # check for valid category name
    if category.lower() not in valid_room_categories:
        return create_HTTP_error_json(
            "Invalid category. Valid categories are: " + str(valid_room_categories),
            "400",
            "Bad Request"), 400

    # create a subset of all rooms which host lectures in the given interval [starttime-endtime]
    # this should increase performance for a "large" database
    busy_rooms_subset = set()
    all_lectures = db.get_list_of_lectures()
    for x in range(len(all_lectures)):
        if interval_start < datetime.strptime(all_lectures[x]["endTime"], valid_date_format) \
                and interval_end > datetime.strptime(all_lectures[x]["startTime"], valid_date_format):
            # if there is a lecture in the specified interval
            # then add the roomId to the busy_rooms_subset
            busy_rooms_subset.add(all_lectures[x]["roomId"])

    # create a list with all available rooms
    for x in range(len(all_rooms)):
        if category == all_rooms[x]["category"] or category == "all":
            if all_rooms[x]["roomId"] not in busy_rooms_subset:
                room_list.append(Room(building=all_rooms[x]["building"],
                                      category=all_rooms[x]["category"],
                                      chairs=all_rooms[x]["chairs"],
                                      chairs_max=all_rooms[x]["chairs_max"],
                                      pc=all_rooms[x]["pc"],
                                      room_id=all_rooms[x]["roomId"],
                                      tables_exam=all_rooms[x]["tables_exam"]))
    return room_list


def create_HTTP_error_json(detail, status, title):
    data = {
        'detail': detail,
        'status': status,
        'title': title,
        'type': "about:blank",
    }
    return data

