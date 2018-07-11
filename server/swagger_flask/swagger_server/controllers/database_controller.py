import json
import os
import random
from datetime import datetime

file_path_database = os.path.join(os.path.curdir,
                                  "swagger_server",  # use ".." if you want to create random data
                                  "data",
                                  "data.json")

valid_date_format = "%Y-%m-%dT%H:%M:%S"

database = None


def open_database():
    with open(file_path_database, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def update_database(new_lectures,
                    new_rooms,
                    new_classes):
    """

    :param new_lectures: a list of lectures created with create_lecture()
    :param new_rooms: a list of rooms created with create_room()
    :param new_classes: a list of classes created with create_class()
    :return:
    """
    new_database = dict()
    new_database["lectures"] = new_lectures
    new_database["rooms"] = new_rooms
    new_database["classes"] = new_classes

    os.remove(file_path_database)
    with open(file_path_database, 'w') as f:
        json.dump(new_database, f, indent=4)

    database = open_database()


def create_lecture(start_time,
                   end_time,
                   room_id,
                   class_id,
                   name):
    """

    :param start_time: string, datetime-format: %Y-%m-%dT%H:%M:%S
    :param end_time: string, datetime-format: %Y-%m-%dT%H:%M:%S
    :param room_id: string, room where the lecture is given: O511
    :param class_id: string, class which is registered for this lecture: TIT15
    :param name: string, name of the lecture
    :return:
    """

    # check if the timestamps have the correct format
    try:
        datetime.strptime(start_time, valid_date_format)
        datetime.strptime(end_time, valid_date_format)
    except ValueError:
        print("invalid date-format, try:" + valid_date_format)

    lecture = dict()
    lecture["startTime"] = start_time
    lecture["endTime"] = end_time
    lecture["roomId"] = room_id
    lecture["classId"] = class_id
    lecture["name"] = name
    return lecture


def create_room(building,
                category,
                chairs,
                chairs_max,
                pc,
                room_id,
                tables_exam):
    """

    :param building: string, human readable name of the building, example: Hauptgebäude
    :param category: string, category of the room, valid: "Seminarraum", "Labor", "Meeting", "Büro", "Projektraum"
    :param chairs: string, number of chairs in the room
    :param chairs_max: string, maximum number of chairs that can be placed in that room
    :param pc: string, number of computers in that room
    :param room_id: string,  name / id of the room, example: H222
    :param tables_exam: string, max number of tables in that room which can be placed with a wide enough gap for an exam
    :return:
    """
    room = dict()
    room["building"] = building
    room["category"] = category
    room["chairs"] = chairs
    room["chairs_max"] = chairs_max
    room["pc"] = pc
    room["roomId"] = room_id
    room["tables_exam"] = tables_exam
    return room


def create_class(class_id,
                 category):
    """

    :param class_id: string, short name / id of the class, example: TIT15
    :param category: string, name of the classgroup, example: TIT
    :return:
    """
    klass = dict()
    klass["classId"] = class_id
    klass["category"] = category
    return klass


def create_random_database():
    list_of_rooms = []
    list_of_classes = []
    list_of_lectures = []
    room_categories = ["Seminarraum", "Labor", "Meeting", "Büro", "Projektraum"]
    cls = ["TIT15","TIT16","TIT17","TIM15","TIM16","TIM17","TEA15","TAE16","TEA17","TLA15","TLA16","TLA17","TMP15","TMP16","TMP17","TAA15","TAA16","TAA17"]
    rms = ["O511", "O512", "H002", "H003", "H004", "H005", "H006", "H102", "H103", "H130", "H222", "H223", "H224", "H225", "H226", "H227", "H228", "H229"]
    Vorlesungen = ["Mathe", "Physik", "Elektrotechnik", "Elektronik", "BWL", "IT-Sicherheit", "Data Mining", "Web Engineering", "Software Engineering"]
    days = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28"]
    months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
    years = ["2018","2019"]
    for _ in range(6000):
        lec = dict()
        day = random.choice(days)
        month = random.choice(months)
        year = random.choice(years)
        start = str(random.randint(10, 14))
        end = str(random.randint(15, 20))
        lec["startTime"] = year + "-" + month + "-" + day + "T" + start + ":00:00"
        lec["endTime"] = year + "-" + month + "-" + day + "T" + end + ":00:00"
        lec["roomId"] = random.choice(rms)
        lec["classId"] = random.choice(cls)
        lec["name"] = random.choice(Vorlesungen)
        list_of_lectures.append(lec)

    for x in cls:
        rm = dict()
        rm["category"] = x[:3]
        rm["classId"] = x
        list_of_classes.append(rm)

    for y in rms:
        building_name = "DHBW Friedrichshafen"
        if y.startswith("O"):
            building_name = "Container Ost"
        if y.startswith("H"):
            building_name = "Hauptgebäude"

        cl = dict()
        cl["building"] = building_name
        cl["category"] = random.choice(room_categories)
        cl["chairs"] = str(random.randint(0, 32))
        cl["chairs_max"] = str(random.randint(0, 32))
        cl["pc"] = str(random.randint(0, 32))
        cl["roomId"] = y
        cl["tables_exam"] = str(random.randint(0, 32))
        list_of_rooms.append(cl)
        update_database(list_of_lectures, list_of_rooms, list_of_classes)


#create_random_database() # change file_path_database accordingly


def get_list_of_lectures():
    return database["lectures"]


def get_list_of_rooms():
    return database["rooms"]


def get_list_of_classes():
    return database["classes"]


def get_list_of_class_ids():
    class_id_set = set()
    for x in range(len(database["classes"])):
        class_id_set.add(database["classes"][x]["classId"])
    return class_id_set


def get_list_of_room_ids():
    room_id_set = set()
    for x in range(len(database["rooms"])):
        room_id_set.add(database["rooms"][x]["roomId"])
    return room_id_set



