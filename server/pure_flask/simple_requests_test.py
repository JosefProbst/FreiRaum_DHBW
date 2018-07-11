import requests
import datetime


base_url = "http://josef.gpplanet.de:8080/FreiRaum/FreiRaum/1.0.0/"

valid_date_format = "%Y-%m-%dT%H:%M:%S"

invalid_date_format = "%Y-%m-%dT%H:%M"

now = datetime.datetime.strftime(datetime.datetime.now(), valid_date_format)
now_plus_3h = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(hours=3), valid_date_format)

now_invalid = datetime.datetime.strftime(datetime.datetime.now(), invalid_date_format)
now_plus_3h_invalid = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(hours=3), invalid_date_format)

now_plus_15d = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=15), valid_date_format)
now_plus_15d3h = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=15, hours=3), valid_date_format)

now_minus_15d = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=-15), valid_date_format)
now_minus_15d3h = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=-15, hours=3), valid_date_format)


r = requests.get(base_url + "classes/TIT16")
assert r.status_code == requests.codes.ok
r = requests.get(base_url + "classes")
assert r.status_code == requests.codes.ok
r = requests.get(base_url + "rooms")
assert r.status_code == requests.codes.ok
r = requests.get(base_url + "rooms/H222")
assert r.status_code == requests.codes.ok
r = requests.get(base_url + "rooms?starttime=" + now + "&endtime=" + now_plus_3h + "&category=all")
assert r.status_code == requests.codes.ok

# no category
r = requests.get(base_url + "rooms?starttime=" + now + "&endtime=" + now_plus_3h)
assert r.status_code == 400
# no endtime
r = requests.get(base_url +"rooms?starttime=" + now + "&category=all")
assert r.status_code == 400
# no starttime
r = requests.get(base_url + "rooms?endtime=" + now_plus_3h + "&category=all")
assert r.status_code == 400
# category is not valid
r = requests.get(base_url + "rooms?starttime=" + now + "&endtime=" + now_plus_3h + "&category=not_valid")
assert r.status_code == 400
# endtime before starttime
r = requests.get(base_url + "rooms?starttime=" + now_plus_3h + "&endtime=" + now + "&category=all")
assert r.status_code == 400
# starttime is not valid
r = requests.get(base_url + "rooms?starttime=" + now_invalid + "&endtime=" + now_plus_3h + "&category=all")
assert r.status_code == 400
# endtime is not valid
r = requests.get(base_url + "rooms?starttime=" + now + "&endtime=" + now_plus_3h_invalid + "&category=all")
assert r.status_code == 400
# both times are not valid
r = requests.get(base_url + "rooms?starttime=" + now_invalid + "&endtime=" + now_plus_3h_invalid + "&category=all")
assert r.status_code == 400

# requested date is "older" than 14 days
r = requests.get(base_url + "rooms?starttime=" + now_minus_15d + "&endtime=" + now_minus_15d3h + "&category=all")
assert r.status_code == 403

# requested date is "newer" than 14 days
r = requests.get(base_url + "rooms?starttime=" + now_plus_15d + "&endtime=" + now_plus_15d3h + "&category=all")
assert r.status_code == 403

# class does not exits
r = requests.get(base_url + "classes/TIT1615")
assert r.status_code == 404
# room does not exits
r = requests.get(base_url + "rooms/H2222")
assert r.status_code == 404
# /class is not defined
r = requests.get(base_url + "class")
assert r.status_code == 404

print("All Tests succeeded")

