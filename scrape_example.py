"""Simple requests demo"""
import requests
import re
from datetime import datetime

request_url1 = 'https://peabody.jhu.edu/events/photo/page/1/'
request_url2 = 'https://peabody.jhu.edu/events/photo/page/2/'
request_url3 = 'https://peabody.jhu.edu/events/photo/page/3/'
request_url4 = 'https://baltshowplace.tumblr.com/'

def parse_event_datetime(event_date_text,event_time_text):
  if event_time_text:
    fulldatetext = event_date_text + ' ' + event_time_text
    if ':' in event_time_text:
      fulldatetime = datetime.strptime(fulldatetext, '%A, %B %d, %Y %I:%M%p')
    else:
      fulldatetime = datetime.strptime(fulldatetext, '%A, %B %d, %Y %I%p')
  else:
    fulldatetime = datetime.strptime(event_date_text, '%A, %B %d, %Y')
  return fulldatetime

def scrape_page_showspace(request_url):

  showspace_location_dict = {
    '<span style="color: #444444">Fadensonnen</span>':'3 W 23rd St',
    '1300 Bayard St':'1300 Bayard St',
    '1627 E Fort Ave':'1627 E Fort Ave',
    '1750 Union Ave':'1750 Union Ave',
    '1828 Webster St':'1828 Webster St',
    '1915 Maryland Avenue':'1915 Maryland Ave',
    '1919':'1919 E Fleet St',
    '200 St. Paul Place':'200 St. Paul Place',
    '2010 Clipper Park Rd Suite 105':'2010 Clipper Park Rd',
    '21 W. Mt Royal 5th Floor':'21 W Mt Royal Ave',
    '27 S Patterson Park':'27 S Patterson Park',
    '218 West Saratoga St':'218 W Saratoga St',
    '225 Holliday St':'225 Holliday St',
    '2410 Erdman Ave':'2410 Erdman Ave',
    '2640 Space':'2640 St Paul St',
    '2741 Guilford Ave.':'2741 Guilford Ave',
    '29th St &amp; Charles St':'2901 N Charles St',
    '2999 Boston St':'2999 Boston St',
    '32nd St &amp; Brentwood':'32nd St &amp; Brentwood',
    '32nd St &amp; Brentwood Ave':'32nd St &amp; Brentwood',
    '3000 Block of Abell Ave.':'3001 Abell Ave',
    '3001 East Dr.':'3001 East Dr.',
    '307 Northway':'307 Northway',
    '3300 Clipper Mill Rd':'3300 Clipper Mill Rd',
    '3311 Ailsa Ave':'3311 Ailsa Ave',
    '3301 Waterview Ave':'3301 Waterview Ave',
    '3355 Keswick':'3355 Keswick Rd',
    '4001 Harford Rd':'4001 Harford Rd',
    '431 Notre Dome Lane':'431 Notre Dame Lane',
    '4518 Raspe Ave':'4518 Raspe Ave',
    '5701 Smith Ave':'5701 Smith Ave',
    '6007 Pinehurst Rd':'6007 Pinehurst Rd',
    '6207 Blackburn Ln':'6207 Blackburn Ln',
    '709 N. Howard St.':'709 N Howard St',
    '8x10':'10 E Cross St',
    '810 W. 36th St':'810 W 36th St',
    'Address sent after ticket purchase on RA':'UNKNOWN',
    'Aliceanna Social Club':'1603 Aliceanna St',
    'American Legion Post 38 (3300 Dundalk Ave)':'3300 Dundalk Ave',
    'American Visionary Arts Museum':'800 Key Hwy',
    'An Die Musik':'409 N Charles St',
    'Angel’s Rock Bar':'10 Market Pl',
    'Angels Rock Bar':'10 Market Pl',
    'Area 405':'405 E Oliver St',
    'Baltimore City Hall':'100 Holliday St',
    'Baltimore Safe Haven':'2117 N Charles St',
    'Baltimore Science Fiction Society':'3310 E Baltimore St',
    'Baltimore Spirits Company':'1700 W 41st St',
    'Baltimore Theatre Project':'45 W Preston St',
    'Barcocina':'1629 Thames St',
    'Big Blue House (DM bands for address)':'UNKNOWN',
    'Black Cherry Puppet Theater':'1115 Hollins St',
    'Black Collar':'2100 Aisquith St',
    'Bliss Meadows (5105 Plainfield Avenue)':'5105 Plainfield Ave',
    'Bliss Meadows (5105 Plainfield Ave)':'5105 Plainfield Ave',
    'Bloom’s':'2 E Read St',
    'Bogus Gallery (1511 Guilford Ave)':'1511 Guilford Ave',
    'Bone Orchard (DM bands for address)':'UNKNOWN',
    'Book Thing':'3001 Vineyard Ln',
    'Bromo Arts District':'21 S Eutaw St',
    'BSC’s Cocktail Gallery':'1700 W 41st St',
    'BSO':'1212 Cathedral St',
    'CFG Arena':'201 W Baltimore St',
    'Canton Waterfront Park':'3001 Boston St',
    'Caroll Skatepark':'800 Bayard St',
    'Cat House (DM artists for address)':'UNKNOWN',
    'Cat House (DM bands for address)':'UNKNOWN',
    'Central Library (400 Cathedral St)':'400 Cathedral St',
    'Ceremony Coffee Harbor East':'1312 Point St',
    'Ceremony Coffee Harbor Point':'1312 Point St',
    'Chapel of Church of the Redeemer':'5603 N Charles St',
    'Charles St':'1 N Charles St',
    'Charles Theater':'1711 N Charles St',
    'Charm City Books':'426 W Franklin St',
    'Charm City Meadworks':'400 E Biddle St',
    'Charm City Skatepark':'4401 O\'Donnell St',
    'Checkerspot Brewing':'1421 Ridgely St',
    'Chilton St &amp; Hillen Road':'Chilton St & Hillen Road',
    'Church on the Square':'1025 S Potomac St',
    'Clifton Park':'2701 St Lo Dr',
    'Clovr Collective (2010 Clipper Park Road)':'2010 Clipper Park Road',
    'Club 603':'UNKNOWN',
    'Club Car':'12 W North Ave',
    'Club Car.':'12 W North Ave',
    'Club Carr':'12 W North Ave',
    'Comptoir Du Vin':'1729 Maryland Ave',
    'Creative Alliance':'3134 Eastern Ave',
    'Creative Alliance.':'3134 Eastern Ave',
    'Crown Back Bar':'1910 N Charles st',
    'Crown Pink Room':'1910 N Charles st',
    'Cult Classic Brewing':'1169 Shopping Center Rd',
    'Current Space':'421 N Howard St',
    'Cylburn Arboretum':'4915 Greenspring Ave',
    'Dangerously Delicious (810 36th St)':'810 36th St',
    'Dangerously Delicious Hampden (810 W. 36th St)':'810 36th St',
    'Design Distillery (1414 Key Hwy)':'1414 Key Hwy',
    'Digital Xscape (DM digitalxscape for address)':'UNKNOWN',
    'Digital Xscape (DM for Address)':'UNKNOWN',
    'DM artists for address':'UNKNOWN',
    'DM bands for address':'UNKNOWN',
    'DM beatitude.bmore for address':'UNKNOWN',
    'DM digitalxscape for address':'UNKNOWN',
    'DM Digital Xscape for address':'UNKNOWN',
    'DM inmysoulzine for address':'UNKNOWN',
    'DM itsjacqjill for address':'UNKNOWN',
    'Downtown':'1 N Charles St',
    'Druid Hill Park':'900 Druid Park Lake Dr',
    'El Bufalo':'2921 O\'Donnell St',
    'Ekiben Hampden':'911 W 36th St',
    'Ema’s Corner':'33 W North Ave',
    'Ema’s Corner (33 W North Ave)':'33 W North Ave',
    'Emmanuel Episcopal Church':'811 Cathedral St',
    'Enigma Bar':'1713 Eastern Ave',
    'Fadensonnen':'3 W 23rd St',
    'Frank’s Bay Tavern':'4507 Pennington Ave',
    'Good Neighbor Design Garage':'3827 Falls Rd',
    'Goucher College (Trustees Hall)':'1021 Dulaney Valley Rd, Towson, MD',
    'Goucher Glass Studio Trustees Hall':'1021 Dulaney Valley Rd, Towson, MD',
    'Guilford Hall Brewery':'1611 Guilford Ave',
    'Hargrove':'2225 Hargrove Ave',
    'Haus (DM wmbc_radio for address)':'UNKNOWN',
    'Herring Run':'3800 Belair Rd',
    'Hippodrome':'12 N Eutaw St',
    'Holy Frijoles':'908-912 W 36th St',
    'Holy Frijoles</strike>':'908-912 W 36th St',
    'Homewood Friends Meeting House':'3107 N Charles St',
    'Homewood Friends Meeting House (3107 N. Charles St.)':'3107 N Charles St',
    'House of Chiefs':'4603 York Rd',
    'House of Chiefs (4603 York Road)':'4603 York Rd',
    'House of Za (DM bands for address)':'UNKNOWN',
    'Idle Hour (201 E Fort Ave)':'201 E Fort Ave',
    'Idle Hour (201 E Fort Ave)':'201 E Fort Ave',
    'Iiinteruption Studios':'UNKNOWN',
    'Inner Harbor Amphitheater':'200 E Pratt St',
    'Inner Harbor Wine Village':'399 E Pratt St',
    'Kenwood Tavern':'800 S Kenwood Ave',
    'Keystone Korner':'1350 Lancaster St',
    'Koopatini Haus (DM bands for address)':'UNKNOWN',
    'Le Mondo':'406 N Howard St',
    'Lith Hall':'851 Hollins St',
    'Locals Only':'25 E Cross St',
    'Location TBA':'UNKNOWN',
    'Lost &amp; Found (1601 Ridgely St)':'1601 Ridgely St',
    'Lwnsphere (4518 Raspe Ave)':'4518 Raspe Ave',
    'Lwn Sphere (4518 Raspe Ave)':'4518 Raspe Ave',
    'M.A.P. Technologies':'322 W Baltimore St',
    'M&amp;T Bank Exchange':'401 W Fayette St',
    'Manor Mill':'2029 Monkton Rd',
    'Market Maven':'1630 Reisterstown Rd',
    'Maryland Safe Haven':'2117 N Charles St',
    'Maryland Science Center':'601 Light St',
    'Mercury Theater':'1823 N Charles St',
    'Mercury Theatre':'1823 N Charles St',
    'Metro':'1700 N Charles St',
    'MICA Meyerhoff Gallery':'1303 W Mount Royal Ave',
    'Mickey’s Joint':'5402 Harford Rd',
    'Micky’s Joint':'5402 Harford Rd',
    'Ministry of Brewing':'1900 E Lombard St',
    'Mobtown Ballroom':'30 W North Ave',
    'Mobtown Ballroom &amp; Club Car &amp; Royal Blue &amp; Night Owl':'30 W North Ave',
    'Mobtown Brewery':'4015 Foster Ave',
    'Monument City Brewing':'1 N Haven St',
    'Monument City Brewing</strike>':'1 N Haven St',
    'Morsebegers':'713 Frederick Rd',
    'Morsbergers':'713 Frederick Rd',
    'Mosaic':'34 Market Pl',
    'Motor House':'120 W North Ave',
    'Museum of Industry':'1415 Key Hwy',
    'National Aquarium':'501 E Pratt St',
    'Night Owl Gallery':'1735 Maryland Ave',
    'Normal’s':'425 E 31st St',
    'Normal’s Books':'425 E 31st St',
    'Normals':'425 E 31st St',
    'Normals Books':'425 E 31st St',
    'Old Major':'900 S Carey St',
    'Onle Vibez (3241 Belar Rd)':'3241 Belair Rd',
    'Openworks (1400 Greenmount Ave)':'1400 Greenmount Ave',
    'Orion Studios':'2903 Whittington Ave #C',
    'Ottobar':'2549 N Howard St',
    'OttobaR':'2549 N Howard St',
    'Ottobar Upstairs':'2549 N Howard St',
    'Outside (DM bands for address)':'UNKNOWN',
    'Parris Underground (497 Ritchie Highway Suite C)':'497 Ritchie Hwy',
    'Patterson Park':'Patterson Park',
    'Patterson Park Observatory':'Patterson Park',
    'Patterson Park Pagoda':'Patterson Park',
    'Peabody Heights':'401 E 30th St',
    'Peabody Heights Brewery':'401 E 30th St',
    'Peabody Heights Brewery</strike>':'401 E 30th St',
    'Peabody Heights Brewing':'401 E 30th St',
    'Peabody Maestro’s Cafe':'5 E Centre St',
    'Pearlstone Park':'199 W Preston St',
    'Phlote (300 W Pratt St)':'300 W Pratt St',
    'Phlote (300 W Pratt St 3rd floor)':'300 W Pratt St',
    'Pier Six':'731 Eastern Ave',
    'Power Plant':'34 Market Pl',
    'Powerplant':'34 Market Pl',
    'Powerplant Live':'34 Market Pl',
    'Pratt St &amp; Ellwood Ave':'3079 E Pratt St',
    'Rams Head':'20 Market Pl',
    'Rams Head<br>Usher. 8PM, $260 @ CFG Arena':'20 Market Pl',
    'Raw &amp; Refined':'2723 Lighthouse Point',
    'Raw &amp; Refined (2723 Lighthouse Point)':'2723 Lighthouse Point',
    'Recher':'512 York Rd',
    'Red Emma’s':'3128 Greenmount Ave',
    'Remington Ave':'Remington Ave',
    'Renaissance Harborplace Hotel':'202 E Pratt St',
    'Reverb':'2112 N Charles St',
    'Robert C. Marshall Park':'1182 Division St',
    'Rocket To Venus':'3360 Chestnut Ave',
    'Roland Water Tower':'4210 Roland Ave',
    'Roland Water Tower':'4210 Roland Ave',
    'Roosevelt Park (36th St &amp; Falls Rd)':'3601 Falls Rd',
    'Royal Blue':'1733 Maryland Ave',
    'Saunter Corner Bar':'1801 E Lombard St',
    'Shake n’ Bake':'1601 Pennsylvania Ave',
    'Shamrock Inn':'6044 Harford Rd',
    'Sisson Street Community Park':'2701 Sisson St',
    'Skate Park of Baltimore':'1201 W 36th St',
    'Skatepark of Baltimore':'1201 W 36th St',
    'Sky Tower (DM bands for address)':'UNKNOWN',
    'Soundstage':'124 Market Pl',
    'Soundstage<br>Karaoke. 8PM, $FREE @ Old Major':'124 Market Pl',
    'Southpaw (529 S Bond St)':'529 S Bond St',
    'St. Luke’s Church':'800 W 36th St',
    'St. Luke’s Church (800 W 36th St)':'800 W 36th St',
    'St. Mary’s Park':'601 N Paca St',
    'Station North':'1 W North Ave',
    'Stem &amp; Vine':'326 N Charles St',
    'Submersive HQ (3523 Buena Vista Ave)':'3523 Buena Vista Ave',
    'The Bluebird':'3602 Hickory Ave',
    'The Bone Orchard (DM bands for address)':'UNKNOWN',
    'The Book Thing':'3001 Vineyard Ln',
    'The Can Company':'2400 Boston St',
    'The Cat’s House (DM bands for address)':'UNKNOWN',
    'The Cave (DM bands for address)':'UNKNOWN',
    'The Cigarette Jar (DM bands for address)':'UNKNOWN',
    'The Compound':'2239 Kirk Ave',
    'The Depot':'1728 N Charles St',
    'The Empanada Lady':'10 South St',
    'The Forest (DM ___by_my_reanimated_corpse for address)':'UNKNOWN',
    'The Forest (DM bands for address)':'UNKNOWN',
    'The Forest (DM bmorezinefest for address)':'UNKNOWN',
    'The Hargrove (2223 Hargrove St)':'2223 Hargrove St',
    'The Hargrove (2225 Hargrove Aly)':'2225 Hargrove St',
    'The Hargrove':'2225 Hargrove St',
    'The Hargrove (DM artists for address)':'39.3150763,-76.6145339',
    'The H.O.L.E. (DM bmorezinefest for address)':'UNKNOWN',
    'The Hole (DM bands below for address)':'UNKNOWN',
    'The Hole (DM bands for address)':'UNKNOWN',
    'The Hole (DM bmorezinefest for address)':'UNKNOWN',
    'The Hole Severna Park (DM bands for address)':'UNKNOWN',
    'The Lyric':'140 W Mt Royal Ave',
    'The Lyric</strike>':'140 W Mt Royal Ave',
    'The Manor':'924 N Charles St',
    'The Meyerhoff':'1212 Cathedral St',
    'The Ottobar':'2549 N Howard St',
    'The Recher':'512 York Rd',
    'The Shamrock Inn':'6044 Harford Rd',
    'The Skatepark (DM bands for address)':'UNKNOWN',
    'The Undercroft':'2629 Huntington Ave',
    'The Vortex CAA Park':'202 Ingleside Ave',
    'The Vortex (CAA Park)':'202 Ingleside Ave',
    'The Vortex at CAA Park':'202 Ingleside Ave',
    'The Voxel':'9 W 25th St',
    'The Watermelon Room (DM bands for address)':'UNKNOWN',
    'The Wiggle Room (3000 Falls Rd)':'3000 Falls Rd',
    'The Wine Collective':'1700 W 41st St',
    'The Wren':'1712 Aliceanna St',
    'Thee Portal (DM artists for address)':'UNKNOWN',
    'Towson Planetarium':'8000 York Rd',
    'True Vine':'1827 N Charles St',
    'Union Craft Brewing':'1700 W 41st St',
    'Uranus (DM bands for address)':'UNKNOWN',
    'Village Learning Place (2521 St. Paul St)':'2521 St. Paul St',
    'Warehouse (tix on Resident Advisor)':'UNKNOWN',
    'Warehouse Cinema':'727 W 40th St',
    'Warehouse Cinemas':'727 W 40th St',
    'Warehouse Cinema Rotunda':'727 W 40th St',
    'Watermelon Room (DM bands for address)':'UNKNOWN',
    'Waverly Brewing':'1625 Union Ave',
    'Waverly Brewing Co.':'1625 Union Ave',
    'Waverly Brewing Company':'1625 Union Ave',
    'Waverly Main St':'418 E 32nd St',
    'Waverly United Methodist':'644 E 33rd St',
    'Wax Atlas':'5523 Harford Rd',
    'Weiss Imports &amp; Domestics (1160 Homestead St)':'1160 Homestead St',
    'Wiggle Room (3000 Falls Rd)':'3000 Falls Rd',
    'Wiggle Room (DM bands for address)':'3000 Falls Rd',
    'Wine Collective':'1700 W 41st St',
    'Wyman Park Dell':'2929 N Charles St',
    'Ye Olde Emerald Tavern':'8300 Harford Rd',
    'York Rd &amp; Woodbourne Ave':'5401 York Rd',
    'Zen West':'5916 York Rd',
    'Zika Farm':'UNKNOWN',
    'Zika Farm (DM artists for address)':'UNKNOWN',
    'Zika Farm (Address shown w/ ticket purchase)':'UNKNOWN',
    'Zion Lutheran Church (400 E Lexington St)':'400 E Lexington St',
    'Zissimos':'400 E Lexington St',
    'Zissimo’s':'400 E Lexington St',
    'Zo Gallery (3510 Ash St)':'3510 Ash St',
  }
  showspace_location_coords = {
    '<span style="color: #444444">Fadensonnen</span>':'39.3015459,-76.616743',
    '1300 Bayard St':'39.2783747,-76.6358208',
    '1627 E Fort Ave':'39.2680623,-76.5917014',
    '1750 Union Ave':'39.3332615,-76.643971',
    '1828 Webster St':'39.2689128,-76.60427',
    '1915 Maryland Avenue':'39.3116095,-76.6174162',
    '1919':'39.2843472,-76.6018247',
    '200 St. Paul Place':'39.2914004,-76.6141673',
    '2010 Clipper Park Rd Suite 105':'39.3319754,-76.6456497',
    '21 W. Mt Royal 5th Floor':'39.3051217,-76.6171648',
    '27 S Patterson Park':'39.2929679,-76.5743555',
    '218 West Saratoga St':'39.2931635,-76.6187973',
    '225 Holliday St':'39.291864,-76.610052',
    '2410 Erdman Ave':'39.3252975,-76.5790731',
    '2640 Space':'39.3204511,-76.6159521',
    '2741 Guilford Ave.':'39.3219395,-76.6128369',
    '29th St &amp; Charles St':'39.323355,-76.616934',
    '2999 Boston St':'39.2776319,-76.5738217',
    '3000 Block of Abell Ave.':'39.3248098,-76.611706',
    '3001 East Dr.':'39.3209325,-76.6345425',
    '307 Northway':'39.3427942,-76.6114545',
    '32nd St &amp; Brentwood':'39.303726,-76.609288',
    '32nd St &amp; Brentwood Ave':'39.303726,-76.609288',
    '3300 Clipper Mill Rd':'39.3274597,-76.6385458',
    '3301 Waterview Ave':'39.2550105,-76.6223111',
    '3311 Ailsa Ave':'39.3440789,-76.5618692',
    '3355 Keswick':'39.328491,-76.6276369',
    '4001 Harford Rd':'39.335662,-76.5746326',
    '431 Notre Dome Lane':'39.3512971,-76.6115692',
    '4518 Raspe Ave':'39.3488426,-76.5278754',
    '5701 Smith Ave':'39.3684573,-76.6521711',
    '6007 Pinehurst Rd':'39.3658043,-76.6149956',
    '6207 Blackburn Ln':'39.3699218,-76.6138352',
    '709 N. Howard St.':'39.2980067,-76.6197818',
    '8x10':'39.2770313,-76.6138622',
    '810 W. 36th St':'39.3313957,-76.6299642',
    'Address sent after ticket purchase on RA':'UNKNOWN',
    'Aliceanna Social Club':'39.2834054,-76.5949788',
    'American Legion Post 38 (3300 Dundalk Ave)':'39.2519889,-76.5221377',
    'American Visionary Arts Museum':'39.2803985,-76.6068932',
    'An Die Musik':'39.2945238,-76.6151418',
    'Angel’s Rock Bar':'39.2896777,-76.6072656',
    'Angels Rock Bar':'39.2896777,-76.6072656',
    'Area 405':'39.3065032,-76.6101781',
    'Baltimore City Hall':'39.2908833,-76.6107116',
    'Baltimore Safe Haven':'39.3138024,-76.616473',
    'Baltimore Science Fiction Society':'39.2926035,-76.5704674',
    'Baltimore Spirits Company':'39.3358424,-76.6443726',
    'Baltimore Theatre Project':'39.3042745,-76.6182366',
    'Barcocina':'39.2811117,-76.5944726',
    'Big Blue House (DM bands for address)':'UNKNOWN',
    'Black Cherry Puppet Theater':'39.2872152,-76.635728',
    'Black Collar':'39.3137343,-76.6022154',
    'Bliss Meadows (5105 Plainfield Avenue)':'39.3328412,-76.5495014',
    'Bliss Meadows (5105 Plainfield Ave)':'39.3328412,-76.5495014',
    'Bloom’s':'39.2998179,-76.6154716',
    'Bogus Gallery (1511 Guilford Ave)':'39.3070209,-76.6120693',
    'Bone Orchard (DM bands for address)':'UNKNOWN',
    'Book Thing':'39.3251591,-76.6101512',
    'Bromo Arts District':'39.2876669,-76.6206228',
    'BSC’s Cocktail Gallery':'39.3358424,-76.6443726',
    'BSO':'39.303876,-76.6189886',
    'CFG Arena':'39.2886044,-76.6187088',
    'Canton Waterfront Park':'39.276827,-76.5699968',
    'Caroll Skatepark':'39.281557,-76.639436',
    'Cat House (DM artists for address)':'UNKNOWN',
    'Cat House (DM bands for address)':'UNKNOWN',
    'Central Library (400 Cathedral St)':'39.2945237,-76.6173559',
    'Ceremony Coffee Harbor East':'39.2809255,-76.5984532',
    'Ceremony Coffee Harbor Point':'39.2809255,-76.5984532',
    'Chapel of Church of the Redeemer':'39.3652627,-76.6240753',
    'Charles St':'39.2901346,-76.6148319',
    'Charles Theater':'39.3093254,-76.6159938',
    'Charm City Books':'39.29498,-76.6225029',
    'Charm City Meadworks':'39.3040247,-76.6104762',
    'Charm City Skatepark':'39.2806041,-76.5587337',
    'Checkerspot Brewing':'39.2908816,-76.610759',
    'Chilton St &amp; Hillen Road':'39.3277025,-76.5897824',
    'Church on the Square':'39.2802511,-76.5737227',
    'Clifton Park':'39.320833, -76.582778',
    'Clovr Collective (2010 Clipper Park Road)':'39.3319754,-76.6456497',
    'Club 603':'UNKNOWN',
    'Club Car':'39.3113936,-76.6170449`',
    'Club Car.':'39.3113936,-76.6170449`',
    'Club Carr':'39.3113936,-76.6170449`',
    'Comptoir Du Vin':'39.3015476,-76.6167263',
    'Creative Alliance':'39.2867649,-76.5717943',
    'Creative Alliance.':'39.2867649,-76.5717943',
    'Crown Back Bar':'39.3117857,-76.6168609',
    'Crown Pink Room':'39.3117857,-76.6168609',
    'Cult Classic Brewing':'39.091831,-76.779125',
    'Current Space':'39.2947221,-76.6193838',
    'Cylburn Arboretum':'39.3531897,-76.6541946',
    'Dangerously Delicious (810 36th St)':'39.3313957,-76.6299642',
    'Dangerously Delicious Hampden (810 W. 36th St)':'39.3313957,-76.6299642',
    'Design Distillery (1414 Key Hwy)':'39.2730828,-76.6021748',
    'Digital Xscape (DM digitalxscape for address)':'UNKNOWN',
    'Digital Xscape (DM for Address)':'UNKNOWN',
    'DM artists for address':'UNKNOWN',
    'DM bands for address':'UNKNOWN',
    'DM beatitude.bmore for address':'UNKNOWN',
    'DM digitalxscape for address':'UNKNOWN',
    'DM Digital Xscape for address':'UNKNOWN',
    'DM inmysoulzine for address':'UNKNOWN',
    'DM itsjacqjill for address':'UNKNOWN',
    'Downtown':'39.2901346,-76.6148319',
    'Druid Hill Park':'39.317045,-76.636339',
    'El Bufalo':'39.2798903,-76.5745794',
    'Ekiben Hampden':'39.3308495,-76.6317673',
    'Ema’s Corner':'39.310794,-76.6177434',
    'Ema’s Corner (33 W North Ave)':'39.310794,-76.6177434',
    'Emmanuel Episcopal Church':'39.2987356,-76.6170687',
    'Enigma Bar':'39.2854717,-76.592576',
    'Fadensonnen':'39.3015459,-76.616743',
    'Frank’s Bay Tavern':'39.2250492,-76.5881778',
    'Good Neighbor Design Garage':'39.3345962,-76.6357922',
    'Goucher College (Trustees Hall)':'39.4087096,-76.5956544',
    'Goucher Glass Studio Trustees Hall':'39.4087096,-76.5956544',
    'Guilford Hall Brewery':'39.3084005,-76.612048',
    'Hargrove':'39.29038,-76.61219',
    'Haus (DM wmbc_radio for address)':'UNKNOWN',
    'Herring Run':'39.32536,-76.568997',
    'Hippodrome':'39.2894402,-76.6210986',
    'Holy Frijoles':'39.3312491,-76.6314478',
    'Holy Frijoles</strike>':'39.3312491,-76.6314478',
    'Homewood Friends Meeting House':'39.3263695,-76.6170207',
    'Homewood Friends Meeting House (3107 N. Charles St.)':'39.3263695,-76.6170207',
    'House of Chiefs':'39.3443441,-76.6092286',
    'House of Chiefs (4603 York Road)':'39.3443441,-76.6092286',
    'House of Za (DM bands for address)':'UNKNOWN',
    'Idle Hour (201 E Fort Ave)':'39.2726198,-76.6098886',
    'Iiinteruption Studios':'UNKNOWN',
    'Inner Harbor Amphitheater':'39.2873581,-76.6114433',
    'Inner Harbor Wine Village':'39.2864464,-76.6102909',
    'Kenwood Tavern':'39.2830522,-76.5772611',
    'Keystone Korner':'39.2824611,-76.5979203',
    'Koopatini Haus (DM bands for address)':'UNKNOWN',
    'Le Mondo':'39.2941263,-76.6198852',
    'Lith Hall':'39.2877881,-76.6303368',
    'Locals Only':'39.2765253,-76.6133565',
    'Location TBA':'UNKNOWN',
    'Lost &amp; Found (1601 Ridgely St)':'39.2737205,-76.6299152',
    'Lwnsphere (4518 Raspe Ave)':'39.3488426,-76.5278754',
    'Lwn Sphere (4518 Raspe Ave)':'39.3488426,-76.5278754',
    'M.A.P. Technologies':'39.2894465,-76.6204915',
    'M&amp;T Bank Exchange':'39.290314,-76.6212',
    'Manor Mill':'39.5762544,-76.6101941',
    'Market Maven':'39.3789693,-76.7288117',
    'Maryland Safe Haven':'39.3138024,-76.616473',
    'Maryland Science Center':'39.2815216,-76.6121715',
    'Mercury Theater':'39.3105486,-76.6162619',
    'Mercury Theatre':'39.3105486,-76.6162619',
    'Metro':'39.3089146,-76.6167916',
    'MICA Meyerhoff Gallery':'39.30873,-76.6210491',
    'Mickey’s Joint':'39.3514225,-76.5624988',
    'Micky’s Joint':'39.3514225,-76.5624988',
    'Ministry of Brewing':'39.2909054,-76.5901596',
    'Mobtown Ballroom':'39.3113947,-76.6177064',
    'Mobtown Ballroom &amp; Club Car &amp; Royal Blue &amp; Night Owl':'39.3113947,-76.6177064',
    'Mobtown Brewery':'39.2843704,-76.5625121',
    'Monument City Brewing':'39.2929307,-76.5624118',
    'Monument City Brewing</strike>':'39.2929307,-76.5624118',
    'Morsebegers':'39.2717408,-76.7318923',
    'Morsbergers':'39.2717408,-76.7318923',
    'Mosaic':'39.2895897,-76.6072583',
    'Motor House':'39.3113403,-76.6189024',
    'Museum of Industry':'39.2737223,-76.6021352',
    'National Aquarium':'39.2847578,-76.60769',
    'Night Owl Gallery':'39.3096273,-76.6176346',
    'Normal’s':'39.3259512,-76.609908',
    'Normal’s Books':'39.3259512,-76.609908',
    'Normals':'39.3259512,-76.609908',
    'Normals Books':'39.3259512,-76.609908',
    'Old Major':'39.2819356,-76.6373744',
    'Onle Vibez (3241 Belar Rd)':'39.3212898,-76.5736983',
    'Openworks (1400 Greenmount Ave)':'39.3060824,-76.608924',
    'Orion Studios':'39.2597122,-76.6549785',
    'Ottobar':'39.3188574,-76.6196694',
    'OttobaR':'39.3188574,-76.6196694',
    'Ottobar Upstairs':'39.3188574,-76.6196694',
    'Outside (DM bands for address)':'UNKNOWN',
    'Parris Underground (497 Ritchie Highway Suite C)':'39.2346832,-76.6119605',
    'Patterson Park':'39.2889335,-76.5788048',
    'Patterson Park Observatory':'39.2889335,-76.5788048',
    'Patterson Park Pagoda':'39.2889335,-76.5788048',
    'Peabody Heights':'39.3242354,-76.6104126',
    'Peabody Heights Brewery':'39.3242354,-76.6104126',
    'Peabody Heights Brewery</strike>':'39.3242354,-76.6104126',
    'Peabody Heights Brewing':'39.3242354,-76.6104126',
    'Peabody Maestro’s Cafe':'39.2962108,-76.6150451',
    'Pearlstone Park':'39.3043142,-76.6195229',
    'Phlote (300 W Pratt St)':'39.2866853,-76.6196986',
    'Phlote (300 W Pratt St 3rd floor)':'39.2866853,-76.6196986',
    'Pier Six':'39.283608,-76.6042422',
    'Power Plant':'39.2895897,-76.6072583',
    'Powerplant':'39.2895897,-76.6072583',
    'Powerplant Live':'39.2895897,-76.6072583',
    'Pratt St &amp; Ellwood Ave':'39.2899791,-76.5734417',
    'Rams Head':'39.2892619,-76.6071918',
    'Rams Head<br>Usher. 8PM, $260 @ CFG Arena':'39.2892619,-76.6071918',
    'Raw &amp; Refined':'39.2774398,-76.5777849',
    'Raw &amp; Refined (2723 Lighthouse Point)':'39.2774398,-76.5777849',
    'Recher':'39.4009454,-76.6021005',
    'Red Emma’s':'39.3269965,-76.6099978',
    'Remington Ave':'39.3233126,-76.6234234',
    'Renaissance Harborplace Hotel':'39.286554,-76.6109903',
    'Reverb':'39.313714,-76.6171249',
    'Robert C. Marshall Park':'39.3086443,-76.6388888',
    'Rocket To Venus':'39.3285598,-76.6294581',
    'Roland Water Tower':'39.3412196,-76.6349848',
    'Roosevelt Park (36th St &amp; Falls Rd)':'39.3313227,-76.6346173',
    'Royal Blue':'39.3095848,-76.6176354',
    'Saunter Corner Bar':'39.2903041,-76.5915473',
    'Shake n’ Bake':'39.3032633,-76.633751',
    'Shamrock Inn':'39.3583692,-76.5565543',
    'Sisson Street Community Park':'39.3188318,-76.6245288',
    'Skate Park of Baltimore':'39.330643,-76.635734',
    'Skatepark of Baltimore':'39.330643,-76.635734',
    'Sky Tower (DM bands for address)':'UNKNOWN',
    'Soundstage':'39.2875658,-76.6074329',
    'Soundstage<br>Karaoke. 8PM, $FREE @ Old Major':'39.2875658,-76.6074329',
    'Southpaw (529 S Bond St)':'39.2846221,-76.5950825',
    'St. Luke’s Church':'39.331478,-76.6295992',
    'St. Luke’s Church (800 W 36th St)':'39.331478,-76.6295992',
    'St. Mary’s Park':'39.2958078,-76.6224647',
    'Station North':'39.3107411,-76.6166913',
    'Stem &amp; Vine':'39.2932699,-76.6155328',
    'Submersive HQ (3523 Buena Vista Ave)':'39.3291366,-76.6381614',
    'The Bluebird':'3602 Hickory Ave',
    'The Bone Orchard (DM bands for address)':'UNKNOWN',
    'The Book Thing':'39.3251591,-76.6101512',
    'The Can Company':'39.2817479,-76.5816562',
    'The Cat’s House (DM bands for address)':'UNKNOWN',
    'The Cave (DM bands for address)':'UNKNOWN',
    'The Cigarette Jar (DM bands for address)':'UNKNOWN',
    'The Compound':'39.3151509,-76.6049917',
    'The Depot':'39.3096068,-76.6167329',
    'The Empanada Lady':'39.2892322,-76.6112179',
    'The Forest (DM ___by_my_reanimated_corpse for address)':'UNKNOWN',
    'The Forest (DM bands for address)':'UNKNOWN',
    'The Forest (DM bmorezinefest for address)':'UNKNOWN',
    'The Hargrove (2223 Hargrove St)':'39.3150763,-76.6145339',
    'The Hargrove (2225 Hargrove Aly)':'39.3150763,-76.6145339',
    'The Hargrove':'39.3150763,-76.6145339',
    'The Hargrove (DM artists for address)':'39.3150763,-76.6145339',
    'The H.O.L.E. (DM bmorezinefest for address)':'UNKNOWN',
    'The Hole (DM bands below for address)':'UNKNOWN',
    'The Hole (DM bands for address)':'UNKNOWN',
    'The Hole (DM bmorezinefest for address)':'UNKNOWN',
    'The Hole Severna Park (DM bands for address)':'UNKNOWN',
    'The Lyric':'39.305976,-76.6182009',
    'The Lyric</strike>':'39.305976,-76.6182009',
    'The Manor':'39.3004532,-76.6162265',
    'The Meyerhoff':'39.303876,-76.6189886',
    'The Ottobar':'39.3188574,-76.6196694',
    'The Recher':'39.4009454,-76.6021005',
    'The Shamrock Inn':'39.3583692,-76.5565543',
    'The Skatepark (DM bands for address)':'UNKNOWN',
    'The Undercroft':'39.4995455,-76.6430605',
    'The Vortex CAA Park':'39.29038,-76.61219',
    'The Vortex (CAA Park)':'39.29038,-76.61219',
    'The Vortex at CAA Park':'39.29038,-76.61219',
    'The Voxel':'39.3175043,-76.6175292',
    'The Watermelon Room (DM bands for address)':'UNKNOWN',
    'The Wiggle Room (3000 Falls Rd)':'39.3230125,-76.6305904',
    'The Wine Collective':'39.3358424,-76.6443726',
    'The Wren':'39.2837617,-76.5925855',
    'Thee Portal (DM artists for address)':'UNKNOWN',
    'Towson Planetarium':'39.3869768,-76.6185804',
    'True Vine':'39.3105745,-76.6164326',
    'Union Craft Brewing':'39.3358424,-76.6443726',
    'Uranus (DM bands for address)':'UNKNOWN',
    'Village Learning Place (2521 St. Paul St)':'39.3186131,-76.6151688',
    'Warehouse (tix on Resident Advisor)':'UNKNOWN',
    'Warehouse Cinema':'39.3351418,-76.6298625',
    'Warehouse Cinemas':'39.3351418,-76.6298625',
    'Warehouse Cinema Rotunda':'39.3351418,-76.6298625',
    'Watermelon Room (DM bands for address)':'UNKNOWN',
    'Waverly Brewing':'39.3318378,-76.6415299',
    'Waverly Brewing Co.':'39.3318378,-76.6415299',
    'Waverly Brewing Company':'39.3318378,-76.6415299',
    'Waverly Main St':'39.3272588,-76.6100064',
    'Waverly United Methodist':'39.3287727,-76.60665',
    'Wax Atlas':'39.3525967,-76.5609185',
    'Weiss Imports &amp; Domestics (1160 Homestead St)':'39.3246781,-76.6011816',
    'Wiggle Room (3000 Falls Rd)':'39.3230125,-76.6305904',
    'Wiggle Room (DM bands for address)':'39.3230125,-76.6305904',
    'Wine Collective':'39.3358424,-76.6443726',
    'Wyman Park Dell':'39.324025,-76.6170002',
    'Ye Olde Emerald Tavern':'39.3791712,-76.5386118',
    'York Rd &amp; Woodbourne Ave':'39.3556559,-76.6096683',
    'Zen West':'39.364333,-76.610107',
    'Zika Farm':'UNKNOWN',
    'Zika Farm (DM artists for address)':'UNKNOWN',
    'Zika Farm (Address shown w/ ticket purchase)':'UNKNOWN',
    'Zion Lutheran Church (400 E Lexington St)':'39.291361,-76.61015',
    'Zissimos':'39.3309235,-76.6334081',
    'Zissimo’s':'39.3309235,-76.6334081',
    'Zo Gallery (3510 Ash St)':'39.3295124,-76.6401209',
  }
  location_set = set()
  firstpage = requests.get(request_url).text

  firstpage_single_line = ' '.join(firstpage.splitlines())

  firstpagelines = firstpage.splitlines()

# find and report
  list_of_matching_months = re.findall(r"(\s*<section\s+class=\"post\">.*?</div>)",firstpage_single_line)
  first_matching_month = list_of_matching_months[11]

  for thismonth in [first_matching_month]:
    list_of_links = re.findall(r"href=\"(.*?)\"",thismonth)
    single_link = re.search(r"href=\"(.*?)\"",thismonth)
    thismonth_url = single_link.group(1)
    print(thismonth_url)
    # clicking through to current month's results
    thismonth_result = requests.get(thismonth_url).text
    list_of_matching_strings = re.findall(r"(\s*</figure>\s*</div>\s*</div>\s*<p>.*?<section\s+class=\"inline-meta post-extra\">)",firstpage_single_line)

    thismonth_result_single_line = ' '.join(thismonth_result.splitlines())
    daylist = re.split(r"<p><br></p>",thismonth_result_single_line)
    for thisday in daylist:
      event_date_match = re.search(r"<h2>(.*?)</h2>",thisday)
      if event_date_match:
        event_date_text = event_date_match.group(1)
        list_of_events = re.findall(r"(<p>\s*\w.*?</p>)",thisday)
        for event in list_of_events:
          print('HERE IS AN EVENT')
          event_title_match = re.search(r"<p>(.*?)</p>",event)
          event_title_text = event_title_match.group(1)
          print(event_title_text)

          event_url_match = 'FIXME'
          event_url_text = thismonth_url
          print(event_url_text)

          print(event_date_text)

          event_time_match = re.search(r"<p>.*?\.\s+(\d+\D*(?:AM|PM))\s*[,.@&-]",event)
          if event_time_match:
            event_time_text = event_time_match.group(1)
            print(event_time_text)
            event_time_text = re.sub(r"\b15PM","5PM",event_time_text)
            event_time_text = re.sub(r"\b20PM","8PM",event_time_text)
            event_time_text = re.sub(r"\b3PMPM","3PM",event_time_text)
            print(event_time_text)
            fulldatetime = parse_event_datetime(event_date_text,event_time_text)
            print(fulldatetime)

          event_location_match = re.search(r"@\s+(.*?)\s*</p>",event)
          if event_location_match:
            event_location_text = event_location_match.group(1)
            if event_location_text:
              print(event_location_text)
              location_set.add(event_location_text)

          event_street_address_text = "ERROR"
          if event_location_text:
            event_street_address_text = showspace_location_dict[event_location_text]
            print(event_street_address_text)

          event_cost_match = re.search(r"<p>.*?\.\s+\w.*?(?:AM|PM)\s*[,.@&-]\s+(.*?)\s+@",event)
          if event_cost_match:
            event_cost_text = event_cost_match.group(1)
            print(event_cost_text)
          else:
            print("DUNNO")

          event_description_match = re.search(r"<div\s+class=\"tribe-events-single-event-description[^>]*>\s*(.*?)</div>",thismonth_result_single_line)
          if event_description_match:
            event_description_text = event_description_match.group(1)
            print(event_description_text)
          else:
            print("NONE")
#  print(location_set)
#  location_list = list(location_set)
#  location_list.sort()
#  print(location_list)

def scrape_page_peabody(request_url):
  result = requests.get(request_url).text

  result_single_line = ' '.join(result.splitlines())

  resultlines = result.splitlines()

  # find and report
  list_of_matching_strings = re.findall(r"(<article.*?</article>)",result_single_line)

  for result in list_of_matching_strings:
    list_of_links = re.findall(r"href=\"(.*?)\"",result)
    single_link = re.search(r"href=\"(.*?)\"",result)
    subsite_url = single_link.group(1)
    subsite_result = requests.get(subsite_url).text
    print()
    print("*****************************************************")
    print()
    #print(subsite_result)
    subsite_result_single_line = ' '.join(subsite_result.splitlines())
    event_title_match = re.search(r"<h1\s+class=\"tribe-events-single-event-title[^>]*>(.*?)</h1>",subsite_result_single_line)
    event_title_text = event_title_match.group(1)
    print(event_title_text)

    event_url_match = 'FIXME'
    event_url_text = subsite_url
    print(event_url_text)

    event_date_match = re.search(r"<div\s+class=\"tse-date-details\">\s*(.*?)</div>",subsite_result_single_line)
    event_date_text = event_date_match.group(1)
    event_date_text = re.sub(r"\s+"," ",event_date_text)
    print(event_date_text)

    event_time_match = re.search(r"<div\s+class=\"tribe-events-abbr\s+tribe-events-start-time[^>]*>\s*(.*?)</div>",subsite_result_single_line)
    event_time_text = event_time_match.group(1)
    print(event_time_text)

    event_location_match = re.search(r"<div\s+class=\"tribe-venue\">\s*(.*?)</div>",subsite_result_single_line)
    event_location_text = event_location_match.group(1)
    print(event_location_text)

    event_cost_match = re.search(r"<div\s+class=\"tribe-events-event-cost\">\s*(.*?)</div>",subsite_result_single_line)
    event_cost_text = event_cost_match.group(1)
    print(event_cost_text)

    #event_description_match = re.search(r"<div\s+class=\"tribe-events-single-event-description[^>]*>\s*(.*?)</div>",subsite_result_single_line)
    #event_description_text = event_description_match.group(1)
    #print(event_description_text)

#scrape_page_peabody(request_url1)
#scrape_page_peabody(request_url2)
#scrape_page_peabody(request_url3)
scrape_page_showspace(request_url4)
