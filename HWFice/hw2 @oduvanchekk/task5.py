def get_root_property(my_root, val):
    for key in my_root:
        if type(my_root[key]) is dict and get_root_property(my_root[key], val) != 'null':
            return key
        elif val in my_root[key]:
            return key
    return 'null'


my_object = {
    "r1n": {
        "mkg": {
            "zma": [21, 45, 66, 111],
            "mii": {
                "ltf": [2, 5, 3, 9, 21]
            },
            "fv": [1, 3, 6, 9]
        },
        "rmk": {
            "amr": [50, 50, 100, 150, 250]
        }
    },
    "fik": {
        "er": [592, 92, 32, 13],
        "gp": [12, 34, 116, 29]
    }
}
print(get_root_property(my_object, 111))
