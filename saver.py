import shelve

shelve_name = "data"


def savePref(user, key, value):
    d = shelve.open(shelve_name)
    d[str(user) + '.' + str(key)] = value
    d.close()


def openPref(user, key, default):
    d = shelve.open(shelve_name)
    if (str(user) + '.' + str(key)) in d:
        return d[str(user) + '.' + str(key)]
    else:
        return default
