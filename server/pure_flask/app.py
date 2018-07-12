from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta

import database_controller
import repeated_timer as rt

app = Flask(__name__)
CORS(app, resources=r"/FreiRaum/FreiRaum/1.0.0/*")

valid_room_categories = ["seminarraum", "labor", "meeting", "büro", "projektraum", "all"]
valid_date_format = "%Y-%m-%dT%H:%M:%S"

valid_days_future = 14
valid_days_past = -14


@app.route("/FreiRaum/FreiRaum/1.0.0/classes/<requested_class_id>")
def search_class_plan(requested_class_id):  # noqa: E501
    """Suche in den lokalen RAPLA-Daten nach Vorlesungsplänen

    Eine Anfrage an diese Adresse gibt einen Vorlesungsplan zu einem entsprechenden Kurs zurück # noqa: E501

    :param requested_class_id: Übergebe String mit dem Kurskürzel, um den Vorlesungsplan zu bekommen
    :type requested_class_id: str

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
    if requested_class_id not in class_ids:
        return create_HTTP_error_json("Didn't find the requested class",
                                      "404",
                                      "Not Found"), 404

    all_lectures = db.get_list_of_lectures()

    # create a list with all lectures of the requested class
    lecture_list = []

    for x in range(len(all_lectures)):
        if all_lectures[x]["classId"] == requested_class_id:
            t_start = datetime.strptime(all_lectures[x]["startTime"], valid_date_format)
            t_end = datetime.strptime(all_lectures[x]["endTime"], valid_date_format)
            if not (t_start < datetime.now() + timedelta(days=valid_days_past)
                    or t_end > datetime.now() + timedelta(days=valid_days_future)):
                lecture_list.append(dict(startTime=all_lectures[x]["startTime"],
                                         endTime=all_lectures[x]["endTime"],
                                         name=all_lectures[x]["name"],
                                         roomId=all_lectures[x]["roomId"],
                                         classId=all_lectures[x]["classId"]))

    return jsonify(lecture_list)


@app.route("/FreiRaum/FreiRaum/1.0.0/classes")
def search_classes():  # noqa: E501
    """Suche in den lokalen RAPLA-Daten nach allen Kursen

    Eine Anfrage an diese Andresse gibt alle Kurse und deren Kategorien zurück # noqa: E501


    :rtype: List[ModelClass]
    """
    # create a list with all classes
    all_classes = db.get_list_of_classes()
    class_list = []
    for x in range(len(all_classes)):
        class_list.append(dict(classId=all_classes[x]["classId"],
                               category=all_classes[x]["category"]))
    return jsonify(class_list)


@app.route("/FreiRaum/FreiRaum/1.0.0/rooms/<requested_room_id>")
def search_room_plan(requested_room_id):  # noqa: E501
    """Suche in den lokalen RAPLA-Daten nach Raumbelegungsplänen

     # noqa: E501

    :param requested_room_id:
    :type requested_room_id: str

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
    if requested_room_id not in room_ids:
        return create_HTTP_error_json("Didn't find the requested room",
                                      "404",
                                      "Not Found"), 404

    # create a list with all lectures of the requested room
    lecture_list = []
    all_lectures = db.get_list_of_lectures()

    for x in range(len(all_lectures)):
        if all_lectures[x]["roomId"] == requested_room_id:
            t_start = datetime.strptime(all_lectures[x]["startTime"], valid_date_format)
            t_end = datetime.strptime(all_lectures[x]["endTime"], valid_date_format)
            if not (t_start < datetime.now() + timedelta(days=valid_days_past)
                    or t_end > datetime.now() + timedelta(days=valid_days_future)):
                lecture_list.append(dict(startTime=all_lectures[x]["startTime"],
                                         endTime=all_lectures[x]["endTime"],
                                         name=all_lectures[x]["name"],
                                         roomId=all_lectures[x]["roomId"],
                                         classId=all_lectures[x]["classId"]))

    return jsonify(lecture_list)


@app.route("/FreiRaum/FreiRaum/1.0.0/rooms")
def search_rooms():  # noqa: E501
    """Suche in den lokalen RAPLA-Daten nach allen/freien Räumen

    :rtype: List[Room]
    """
    requested_start_time = request.args.get('starttime', None)
    requested_end_time = request.args.get('endtime', None)
    requested_category = request.args.get('category', None)

    all_rooms = db.get_list_of_rooms()
    room_list = []

    # /rooms without any arguments should send a list of all rooms
    if requested_start_time is None and requested_end_time is None and requested_category is None:
        for x in range(len(all_rooms)):
            room_list.append(dict(building=all_rooms[x]["building"],
                                  category=all_rooms[x]["category"],
                                  chairs=all_rooms[x]["chairs"],
                                  chairs_max=all_rooms[x]["chairs_max"],
                                  pc=all_rooms[x]["pc"],
                                  roomId=all_rooms[x]["roomId"],
                                  tables_exam=all_rooms[x]["tables_exam"]))
        return jsonify(room_list)

    # a valid specific request on /rooms has to include starttime and endtime
    if requested_start_time is None or requested_end_time is None or requested_category is None:
        return create_HTTP_error_json(
            "category, starttime and endtime must me defined"
            + " valid starttime/endtime:" + valid_date_format
            + " valid categories: " + str(valid_room_categories),
            "400",
            "Bad Request"), 400

    # check if the timestamps have the correct format
    try:
        interval_start = datetime.strptime(requested_start_time, valid_date_format)
        interval_end = datetime.strptime(requested_end_time, valid_date_format)
    except ValueError:
        return create_HTTP_error_json("Invalid date format. Valid:" + valid_date_format,
                                      "400",
                                      "Bad Request"), 400

    if interval_start >= interval_end:
        return create_HTTP_error_json("Invalid dates: starttime >= endtime",
                                      "400",
                                      "Bad Request"), 400

    if interval_start < datetime.now() + timedelta(days=valid_days_past) \
            or interval_end > datetime.now() + timedelta(days=valid_days_future):
        return create_HTTP_error_json("Requests can only be made for the last 14 days, today or coming 14 days",
                                      "403",
                                      "Forbidden"), 403

    # check for valid category name
    if requested_category.lower() not in valid_room_categories:
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
        if requested_category == all_rooms[x]["category"] or requested_category == "all":
            if all_rooms[x]["roomId"] not in busy_rooms_subset:
                room_list.append(dict(building=all_rooms[x]["building"],
                                      category=all_rooms[x]["category"],
                                      chairs=all_rooms[x]["chairs"],
                                      chairs_max=all_rooms[x]["chairs_max"],
                                      pc=all_rooms[x]["pc"],
                                      roomId=all_rooms[x]["roomId"],
                                      tables_exam=all_rooms[x]["tables_exam"]))
    return jsonify(room_list)


def create_HTTP_error_json(detail, status, title):
    data = {
        'detail': detail,
        'status': status,
        'title': title,
        'type': "about:blank",
    }
    return jsonify(data)


if __name__ == "__main__":
    db = database_controller.DatabaseController()
    # non-blocking way to update the database every x seconds
    rt.RepeatedTimer(60, db.create_random_database)
    try:
        app.run(host="0.0.0.0", port=8080)
    finally:
        rt.stop()

