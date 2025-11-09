from datetime import datetime, timedelta

longlat = {
    "Campus Center": [42.391732874644994, -72.52696175141477], 
    "Herter": [42.38789103527097, -72.52735983389012],
    "Union": [42.391008373343716, -72.52766653198437],
    "Black Box": [42.391008373343716, -72.52766653198437], # theater, Same as Student Union
    "BlackBox": [42.391008373343716, -72.52766653198437], # theater, Same as Student Union
    "Cape Cod": [42.391008373343716, -72.52766653198437], #Same as Student Union
    "Du Bois": [42.38986050847985, -72.52830521146252], 
    "Lot 44": [42.39902629983547, -72.52442471703874], # Sylvan Woods Lot
    "RecWell": [42.388893339150904, -72.53172427493728],
    "New Africa": [42.388978951484276, -72.5206839584861],
    "Goodell": [42.38878200984664, -72.52918860130535],
    "Malcolm": [42.38878200984664, -72.52918860130535], # same as Goodell
    "Newman": [42.38734314608258, -72.52179600130539],
    "Stonewall": [42.38872654054515, -72.52933880499367],
    "Latinx American Cultural": [42.38293841872035, -72.52976918781037],
    "Bartlett":[42.38795172262218, -72.52868483198448],
    "Marston":[42.39404096527618, -72.5292659148006],
    "Gunness":[42.39448180204377, -72.5297459318719],
    "Science and Engineering":[42.39453895082785, -72.52712835966646],
    "Hasbrouck":[42.39187412322282, -72.52578762798163],
    "Haigis": [42.38754936721991, -72.52614495029488], # same as Bromery Center for the arts
    "Bromery": [42.38754936721991, -72.52614495029488], # same as Haigis
    "Thompson": [42.39004393174647, -72.52995807123177],
    "Marcus": [42.393975958794165, -72.52864104570452],
    "Skinner":[42.3916126460103, -72.52482703343335],
    "Hampshire":[42.38383696295948, -72.53050583278933],
    "Franklin":[42.3892490047566, -72.52253813949663],
    "Worcester":[42.393334998276735, -72.52519140656085],
    "Berkshire":[42.381918109952196, -72.53002388883648],
    "Engineering Quad":[42.39363919455198, -72.52915897131636],
    "Totman":[42.39614141301196, -72.52589953361426],
    "Arnold":[42.394461192664224, -72.52606061681881],
    "Chenoweth":[42.391633906456946, -72.53032250248661],
    "Campus Pond":[42.389817764757524, -72.52698909306711],
    "Morrill": [42.39094027954138, -72.52404221011663],
    "Isenberg": [42.387339474242, -72.52483184802671],
    "CCPH": [42.385675388811926, -72.52849591573157],
    "Counseling and Psychological Health": [42.385675388811926, -72.52849591573157], # same as CCPH
    "The House": [42.386293393123054, -72.52029108425877],
    "Fernald": [42.38858307076012, -72.52238824887029],
    "Lederle Graduate Research Center": [42.39392005479079, -72.52769594465809], # LGRC, or ~Science and Engineering Library
    "LGRC": [42.39392005479079, -72.52769594465809],
    "Integrative Learning Center": [42.390942445908365, -72.52566971655749],
    "ILC": [42.390942445908365, -72.52566971655749],
    "Honors College": [42.38819221356291, -72.53051117860147],
    "Manning": [42.395246017909464, -72.53080788616757], #includes both computer science laboratories
    "Football Stadium": [42.377252931569565, -72.53600655080845], #McGuirk Alumni Stadium
    "OHill": [42.39188112425516, -72.51923077218746],
    "Old Chapel": [42.3889931002094, -72.52798157448849],
    "Northeast": [42.394813141060865, -72.52489040461563]
}

def getCoords(location: str):
    """Return coordinates from longlat if location name matches, else None."""
    for key in longlat:
        if key.lower() in location.lower():
            return longlat[key]
    return None

def normalizeCoords(location): # turns lat, long arrays into capy coords, 3000x3000.
    coords = getCoords(location)
    if coords is None:
        return None
    lat = round(coords[0],11)
    long = round(coords[1],11)
    y = 3000-(((lat-42.376) * 10**5)*1.3) 
    x = -((((long+72.51) * 10**5))*1.6)-1300
    return [round(x), round(y)]

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

class EventPrototype():
    from datetime import timedelta
    id: int
    title: str
    host: str
    description: str
    x_coord: float
    y_coord: float
    location: str
    time: datetime
    end_time: datetime
    
    def __init__(self, id:int, title:str, host:str, description:str, location:str, time:datetime):
        self.id = id
        self.title = title
        self.host = host
        self.description = description
        self.location = location
        self.time = time
        self.end_time = time + timedelta(hours=2)  # default 2 hour duration
        coords = normalizeCoords(location)
        if coords is not None:
            self.x_coord = coords[0]
            self.y_coord = coords[1]
        else:
            self.x_coord = -1
            self.y_coord = -1
    
    def __repr__(self):
        return f"EventPrototype(id={self.id}, title={self.title}, host={self.host}, description={self.description}, location={self.location}, time={self.time}, end_time={self.end_time}, x_coord={self.x_coord}, y_coord={self.y_coord})"


def parseEvent(lines, start_index, id):
    #Parse a single event starting at start_index, return (EventPrototype, next_index).
    title = lines[start_index].strip()
    date_line = lines[start_index + 1].strip()
    description = lines[start_index + 2].strip()
    host = lines[start_index + 3].strip()

    # Example: "Sunday, November 9 at 7:00PM EST"
    parts = date_line.split(',')
    day_part = parts[1].strip()  # "November 9 at 7:00PM EST"
    month, rest = day_part.split(' ', 1)
    day = int(rest.split(' ')[0])
    time_str = rest.split('at')[1].split('EST')[0].strip()
    dt_str = f"{months.index(month)+1}/{day}/2025 {time_str}"
    time = datetime.strptime(dt_str, "%m/%d/%Y %I:%M%p")
    
    location: str = "" # default location is "" if no location given
    for loc in longlat.keys():
        if loc.lower() in description.lower(): # find location in description
            location = loc
            break

    return EventPrototype(id, title, host, description, location, time), start_index + 4

def scanCapyEvents(n:int) -> list[EventPrototype]:
    events = []
    with open("CapyEvents.txt", "r", encoding="utf-8") as f:
        lines = [l for l in f.readlines() if l.strip() != ""]
    
    i = 0
    id = 3
    while i < len(lines) and len(events) < n:
        event, i = parseEvent(lines, i, id)
        if normalizeCoords(event.location):
            events.append(event)

        # Skip possible blank line separators
        while i < len(lines) and lines[i].strip() == "":
            i += 1
        id += 1
    return events

def test():
    xs:list[float] = []
    ys:list[float] = []
    for location in longlat:
        x,y = normalizeCoords(location)
        xs.append(x)
        ys.append(y)
        #print(f"{x}, {y}")
    print(f"X range: {min(xs)} to {max(xs)}")
    print(f"Y range: {min(ys)} to {max(ys)}")
    print(f"X span: {max(xs)-min(xs)}")
    print(f"Y span: {max(ys)-min(ys)}")
    #print mean
    print(f"X mean: {sum(xs)/len(xs)}")
    print(f"Y mean: {sum(ys)/len(ys)}")
    
    events = scanCapyEvents(100000)
    for event in events: #all events. WHEN TESTING, comment out  if normalizeCoords(event.location) in scanCapyEvents
        if (event.x_coord == -1 or event.y_coord == -1):
            print(f"Failed to normalize coords for event: {event}")

def normalizeAll():
    normalized = {}
    for location in longlat:
        coords = normalizeCoords(location)
        normalized[location] = coords
    print(normalized)

def normalizeDrawn(drawn:list[str]):
    normalized = {}
    for location in drawn:
        coords = normalizeCoords(location)
        normalized[location] = coords
    print(normalized)

drawn = [
"Campus Center", 
"Union",
"Du Bois", 
"RecWell",
"Goodell",
"Haigis", # same as Bromery Center for the arts
"Bromery", # same as Haigis
"Hampshire",
"Franklin",
"Worcester",
"Berkshire",
"Campus Pond",
"Morrill",
"Isenberg",
"Lederle Graduate Research Center", # LGRC, or ~Science and Engineering Library
"LGRC",
"Integrative Learning Center",
"ILC",
"Honors College",
"Manning", #includes both computer science laboratories
"Football Stadium",#McGuirk Alumni Stadium
"Old Chapel",
"OHill",
"Northeast"
]

if __name__ == "__main__":
    #test()
    normalizeDrawn(drawn)