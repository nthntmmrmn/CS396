import json, sys, os, re
import numpy as np
import pandas as pd
import string as str

### TODO
# business names -> city (eg, The Promenade)

# get path and run check as global var
path = sys.argv[1]
if not os.path.exists(path):
    raise Exception("PATH DOESN'T EXIST")

##### CLEANING FUNCTIONS #####
##############################

# remove unicode characters from string
def stripUnicode(word):
    printable = set(str.printable)
    return ''.join(filter(lambda x: x in printable, word))

# remove state abbreviation from string
def removeAbbr(word):
    return re.sub(',? AZ', '', word, flags=re.I)

# make only first letter of each word capitalized
def fixCapitalization(word):
    return re.sub(r'\b[a-z]', lambda x: x.group().upper(), word.lower())

# clean word, then find closest city name
def findClosest(word, cities):
    # cleaning
    word = stripUnicode(word)
    word = removeAbbr(word)
    word = fixCapitalization(word)

    # specific check for '' and 'Phx'
    if len(word) < 1 or word == 'Phx':
        return 'Phoenix'

    # if extra words added to city name, remove them and return just the city name
    # eg, "Westworld Scottsdale", "Metro Phoenix", "Chandler-Gilbert", etc.
    # cuts down from 77 to 61 unique cities
    for city in cities:
        if city in word:
            return city

    # make list of all cities that start with same letter
    sameLetterCities = [x for x in cities if x.startswith(word[0])]

    # init Levenshtein distances array to all zeros
    distances = np.zeros((len(sameLetterCities),))

    # calc LS distance b/w word and each city that starts with same letter
    for city in range(0, len(sameLetterCities)):
        distances[city] = LevenshteinDistance(word, sameLetterCities[city])
    
    # if min distance >= 3, likely not mispelled, so just return original
    if np.min(distances) >= 3:
        # print(f'Before: {word} \t After: {word} \t Distance: {np.min(distances)}')
        return word
    # else < 3, likely mispelled, so replace with closest city name
    else:
        # print(f'Before: {word} \t After: {sameLetterCities[np.argmin(distances)]} \t Distance: {np.min(distances)}')
        return sameLetterCities[np.argmin(distances)]

# calculates Levenshtein Distance b/w two strings
def LevenshteinDistance(str1, str2):

    # init distances matrix
    rows = len(str1)+1
    cols = len(str2)+1
    distance = np.zeros((rows,cols))

    for x in range(rows):
        distance[x][0] = x
    for y in range(cols):
        distance[0][y] = y
    
    # update distances in matrix
    for row in range(1, rows):
        for col in range(1, cols):
            if str1[row-1] == str2[col-1]:
                cost = 0
            else:
                cost = 1
            
            distance[row][col] = min(distance[row-1][col] + 1,
                                     distance[row][col-1] + 1,
                                     distance[row-1][col-1] + cost) 
    
    return distance[rows-1][cols-1]


##### MAIN #####
################

def main():
    ##### COLLECTING DATA #####

    # load businesses into dataframe
    df_business = pd.read_json(path+'/business.json', lines=True)

    # make df of just businesses in AZ
    df_AZ = df_business[df_business['state'] == 'AZ']

    # get all cities in AZ in numpy array
    # only need unique
    AZ_cities = np.unique(df_AZ['city'].to_numpy()) 

    # list of all cities in AZ for comparison with Levenshtein
    cities = ['Tucson', 'Glendale', 'Waddell', 'Tolleson', 'Surprise', 'Sunnyslope', 'Sun Lakes', 'Sun City', 'Snowflake', 'Sedona', 'Rainbow Valley', 'Paradise Valley', 'Litchfield Park', 'Laveen', 'Higley', 'Guadalupe', 'Fountain Hills', 'Fort McDowell', 'Estrella Village', 'East Mesa', 'Central City', 'Carefree', 'Arizona', 'Apache Trail', 'Ahwatukee', 'Phoenix', 'Tucson', 'Mesa', 'Chandler', 'Scottsdale', 'Glendale', 'Gilbert', 'Tempe', 'Peoria', 'Surprise', 'Yuma', 'San Tan Valley', 'Avondale', 'Goodyear', 'Buckeye', 'Flagstaff', 'Casas Adobes', 'Casa Grande', 'Lake Havasu City', 'Catalina Foothills', 'Maricopa', 'Marana', 'Prescott Valley', 'Oro Valley', 'Sierra Vista', 'Prescott', 'Queen Creek', 'Apache Junction', 'Bullhead City', 'Sun City', 'El Mirage', 'San Luis', 'Kingman', 'Sahuarita', 'Fortuna Foothills', 'Drexel Heights', 'Florence', 'Sun City West', 'Fountain Hills', 'Anthem', 'Green Valley', 'Nogales', 'Eloy', 'Rio Rico', 'Somerton', 'Tanque Verde', 'Douglas', 'Payson', 'Sierra Vista Southeast', 'Flowing Wells', 'New River', 'Sun Lakes', 'Fort Mohave', 'Paradise Valley', 'New Kingman-Butler', 'Coolidge', 'Verde Village', 'Cottonwood city', 'Tucson Estates', 'Chino Valley', 'Vail', 'Valencia West', 'Show Low', 'Camp Verde', 'Arizona City', 'Gold Canyon', 'Sedona', 'Saddlebrooke', 'Safford', 'Winslow', 'Tuba City', 'Golden Valley', 'Picture Rocks', 'Wickenburg', 'Catalina', 'Corona de Tucson', 'Page', 'Globe', 'Tolleson', 'Youngtown', 'Guadalupe', 'Village of Oak Creek (Big Park)', 'Litchfield Park', 'Rincon Valley', 'Snowflake', 'Cave Creek', 'Chinle', 'South Tucson', 'Doney Park', 'Three Points', 'Summit', 'Avra Valley', 'Bisbee', 'Thatcher', 'Williamson', 'Holbrook', 'Paulden', 'Lake Montezuma', 'Citrus Park', 'Eagar', 'Benson', 'Colorado City', 'Kayenta', 'Pinetop-Lakeside', 'San Carlos', 'Clarkdale', 'Taylor', 'Whiteriver', 'Fort Defiance', 'Dewey-Humboldt', 'Lake of the Woods', 'Carefree', 'Quartzsite', 'Oracle', 'San Manuel', 'Clifton', 'Willcox', 'Ajo', 'St. Johns', 'Avenue B and C', 'Swift Trail Junction', 'Window Rock', 'Williams', 'Parker', 'Cornville', 'Superior', 'Red Rock CDP', 'Wellton', 'Kachina Village', 'Mohave Valley', 'Black Canyon City', 'Linden', 'Desert Hills', 'Central Heights-Midland City', 'Sells', 'Pima', 'Dolan Springs', 'White Mountain Lake', 'Heber-Overgaard', 'Sacaton', 'Cordes Lakes', 'Star Valley', 'Cibecue', 'Whetstone', 'Kearny', 'Gila Bend', 'Rio Verde', 'Springerville', 'Valle Vista', 'Mayer', 'First Mesa', 'Cienega Springs', 'Pirtleville', 'Bylas', 'Miami', 'Huachuca City', 'Bagdad', 'Kaibito', 'Second Mesa', 'Morenci', 'Pinetop Country Club', 'St. David', 'Lukachukai', 'Blackwater', 'Parks', 'Mammoth', 'Peridot', 'North Fork', 'Scenic', 'Tonto Basin', 'Pine', 'Beaver Dam', 'Centennial Park', 'LeChee', 'Mescal', 'Congress', 'Grand Canyon Village', 'Claypool', 'Cactus Flats', 'Spring Valley', 'Donovan Estates', 'Tubac', 'Many Farms', 'Dilkon', 'Tsaile', 'Tombstone and Fredonia', 'Salome', 'Leupp', 'Golden Shores', 'Canyon Day', 'Komatke', 'Moenkopi', 'Joseph City', 'Wagon Wheel', 'Hotevilla-Bacavi', 'St. Michaels', 'Aguila', 'Peach Springs', 'Fort Valley', 'Casa Blanca', 'Arivaca Junction', 'Cameron', 'Arizona Village', 'Rainbow City', 'Ak-Chin Village', 'Shongopovi', 'Ganado', 'Houck', 'Mountainaire', 'Hondah', 'Six Shooter Canyon and Vicksburg', 'Bouse', 'Rancho Mesa Verde', 'Chilchinbito', 'Patagonia', 'Bluewater', 'Cactus Forest', 'Wilhoit', 'Willow Valley', 'Meadview', 'Sonoita', 'Whitecone', 'Ehrenberg', 'Naco', 'Round Valley', 'Pinon', 'Ash Fork', 'Gila Crossing', 'Dennehotso', 'Kykotsmovi Village and Maricopa Colony', 'Duncan', 'St. Johns CDP', 'Miracle Valley', 'Winslow West', 'Seven Mile', 'Tacna', 'Elephant Head', 'Munds Park', 'Round Rock', 'Strawberry', 'Teec Nos Pos', 'Sawmill', 'East Fork', 'McNary', 'Pimaco Two', 'El Prado Estates', 'Pinal', 'Yarnell', 'Queen Valley', 'Parker Strip', 'Gisela', 'Hayden', 'Burnside and Orange Grove Mobile Manor', 'Arivaca', 'Low Mountain', 'York', 'Littletown', 'Wittmann', 'Cedar Creek', 'San Jose', 'Tusayan', 'Rough Rock', 'Fort Thomas', 'Mesa del Caballo', 'Dudleyville', 'Shonto', 'Sanders', 'Tees Toh', 'Walnut Creek', 'Littlefield', 'Gadsden and Greasewood', 'La Paz Valley', 'Turkey Creek', 'Rock Point', 'Peeples Valley', 'Nelson', 'Seligman', 'Mesquite Creek', 'Nazlini', 'Lazy Y U', 'Wheatfields', 'Sacaton Flats Village and Jerome', 'Icehouse Canyon', 'Drysdale', 'Picacho', 'Solomon', 'Young', 'Bitter Springs', 'Cibola and Chuichu', 'Stanfield', 'Kino Springs', 'Lower Santan Village and Cane Beds', 'Brenda and Clay Springs', 'Upper Santan Village', 'Santa Rosa', 'Wellton Hills', 'Stotonic Village', 'Cornfields', 'Central', 'Tonto Village', 'Red Mesa', 'Wall Lane', 'Wenden', 'Pisinemo and Dateland', 'Winkelman', 'Wet Camp Village', 'Elfrida', 'Del Muerto', 'Bowie', 'Tonalea', 'Tolani Lake', 'Jeddito', 'Top-of-the-World', 'Clacks Canyon', 'Pinedale', 'Poston', 'South Komelik', 'Steamboat', 'Chloride and San Miguel', 'Tumacacori-Carmen', 'Indian Wells', 'Keams Canyon', 'East Globe', 'Padre Ranchitos', 'Palominas', 'Goodyear Village', 'So-Hi', 'White Hills', 'Beyerville', 'Klagetoh', 'Oljato-Monument Valley', 'Cottonwood', 'Oxbow Estates', 'Sunizona', 'Sun Valley', 'Carrizo', 'Cowlic and Summerhaven', 'Maish Vaya', 'Fort Apache', 'Valle and Deer Creek', 'Pinion Pines', 'Sacate Village', 'Red Rock', 'East Verde Estates and McNeal', 'Beaver Valley', 'Dripping Springs', 'Kaibab', 'Morristown', 'Sweet Water Village', 'Why', 'Antares', 'Concho', 'Seba Dalkai', 'Topawa and Haivana Nakya', 'Washington Park', 'Crystal Beach', 'Wikieup', 'San Simon', 'Woodruff', 'Wahak Hotrontk', 'Truxton and El Capitan', 'Ali Chuk', 'Kaka', 'Freedom Acres', 'Elgin', 'Rye', 'Ali Chukson and Sehili', 'Kohls Ranch and Whispering Pines', 'Amado', 'Hackberry', 'Gu Oidak', 'Arlington', 'Geronimo Estates', 'Ventana', 'Christopher Creek, Alpine, and Anegam', 'Hard Rock', 'Oak Springs and Wide Ruins', 'Utting', 'Martinez Lake', 'Katherine', 'Theba', 'Bryce', 'Tonopah', 'Ali Molina and Nolic', 'Rock House and Yucca', 'Roosevelt and Valentine', 'Nutrioso', 'Campo Bonito', 'Tat Momoli', 'Rillito', 'Pine Lake', 'Dragoon and Oatman', 'Flowing Springs', 'Wintersburg and Comobabi', 'Greer', 'Vernon', 'Franklin', 'Ak Chin', 'Jakes Corner', 'Haigler Creek', 'Buckshot', 'Crozier', 'Sunwest', 'Mojave Ranch Estates', 'Kohatk', 'Hunter Creek and Lupton', 'Topock', 'Charco', 'Ko Vaya', 'Alamo Lake']

    #### what to look for / fix
    # [X] space at end
    # [X] capitalization (all caps, all lowercase, 'CIty', etc)
    # [X] mispellings
    # [X] end in 'Az' or 'AZ' or ', AZ'
    # [X] abbreviations ('Phx')
    # !! all start with same letter, cuts down on how many cities to search

    # make copy of AZ cities to update
    new_AZ_cities = AZ_cities.copy()

    # for each city, find it's closest match using LS Distance
    # and replace it in the new cities array
    for city in range(0, AZ_cities.shape[0]):
        new_AZ_cities[city] = findClosest(AZ_cities[city], cities)

    # replace cities in df_AZ with cleaned one from new_AZ_cities
    before_and_after = {AZ_cities[i]: new_AZ_cities[i] for i in range(len(AZ_cities))}
    for before in before_and_after:
        df_AZ['city'] =  df_AZ['city'].replace(before, before_and_after[before])

    # print out the list of unique cleaned cities
    print(list(df_AZ['city'].unique()))
    # and its length
    print(len(list(df_AZ['city'].unique())))

main()
