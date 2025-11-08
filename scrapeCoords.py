longlat = {
    "Campus Center": [42.391732874644994, -72.52696175141477], 
    "Herter": [42.38789103527097, -72.52735983389012],
    "Union": [42.391008373343716, -72.52766653198437],
    "Black Box": [42.391008373343716, -72.52766653198437], # theater, Same as Student Union
    "Du Bois": [42.38986050847985, -72.52830521146252], 
    "Lot 44": [42.39902629983547, -72.52442471703874], # Sylvan Woods Lot
    "RecWell": [42.388893339150904, -72.53172427493728],
    "New Africa": [42.388978951484276, -72.5206839584861],
    "Goodell": [42.38878200984664, -72.52918860130535],
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
    "The House": [42.386293393123054, -72.52029108425877],
    "Fernald": [42.38858307076012, -72.52238824887029],
    "Lederle Graduate Research Center": [42.39392005479079, -72.52769594465809], # LGRC, or ~Science and Engineering Library
    "LGRC": [42.39392005479079, -72.52769594465809],
    "Integrative Learning Center": [42.390942445908365, -72.52566971655749],
    "ILC": [42.390942445908365, -72.52566971655749],
    "Honors College": [42.38819221356291, -72.53051117860147],
    "Manning": [42.395246017909464, -72.53080788616757], #includes both computer science laboratories
    "Football Stadium": [42.377252931569565, -72.53600655080845] #McGuirk Alumni Stadium
}

def getCoords(location):
    if location in longlat:
        return longlat[location]
    else:
        return None
    
def normalizeCoords(location): # turns lat, long arrays into capy coords, 3000x3000.
    coords = getCoords(location)
    if coords is None:
        return None
    lat = round(coords[0],11)
    long = round(coords[1],11)
    x = ((lat-42.3742) * 10**5)
    y = (-(long+72.52024) * 10**5)*1.9
    return [round(x), round(y)]

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


if __name__ == "__main__":
    test()