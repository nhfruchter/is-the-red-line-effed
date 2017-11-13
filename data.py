from collections import OrderedDict
colornames = {
    "blue": "#3F51B5",
    "orange": "#FF9800",
    "red": "#D50000",
    "green": "#4CAF50",
    "bus": "#FFEA00",
    "cr": "#9C27B0"
}

routenames = OrderedDict(
    [("Red", "Red Line"),
    ("Mattapan", "Red/Mattapan"),
    ("Blue", "Blue Line"),
    ("Orange", "Orange Line"),
    ("Green-B", "Green Line - B"),
    ("Green-C", "Green Line - C"),
    ("Green-D", "Green Line - D"),
    ("Green-E", "Green Line - E"),
    ("741", "SL1"),
    ("742", "SL2"),
    ("751", "SL4"),
    ("749", "SL5"),
    ("CR-Fairmount", "CR Fairmount"),
    ("CR-Fitchburg", "CR Fitchburg"),
    ("CR-Worcester", "CR Framingham/Worcester"),
    ("CR-Franklin", "CR Franklin"),
    ("CR-Greenbush", "CR Greenbush"),
    ("CR-Haverhill", "CR Haverhill"),
    ("CR-Kingston", "CR Kingston/Plymouth"),
    ("CR-Lowell", "CR Lowell"),
    ("CR-Middleborough", "CR Middleborough/Lakeville"),
    ("CR-Needham", "CR Needham"),
    ("CR-Newburyport", "CR Newburyport/Rockport"),
    ("CR-Providence", "CR Providence/Stoughton")]
)
bus_prefixes = ('1', '2', '3', '4', '5', '6', '8', '9', 'c')

def names(route):
    if route.startswith("CR"):
        return "%s Line" % route.split("-")[1]
    elif route[0].lower() in bus_prefixes:
        return "%s Bus" % (route)
    elif route.startswith("Green"):
        return routenames.get(route)
    else:
        result = routenames.get(route)
        if result:
            return "%s" % result
        else:
            return "%s Line" % route
    
def colors(route):
    route = str(route).lower()
        
    if "green" in route:
        return colornames['green'] or "#000"
    elif route.startswith("cr"):
        return colornames['cr']
    elif route[0] in bus_prefixes:
        return colornames['bus']
    else:
        return colornames.get(route) or '#646464'
        
        
        