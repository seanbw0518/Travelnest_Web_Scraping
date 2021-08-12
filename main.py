from selenium import webdriver

# driver running Chrome 92, so Chrome 92 must be installed
driver = webdriver.Chrome('chromedriver.exe')

URLS = ["https://www.airbnb.co.uk/rooms/33571268", "https://www.airbnb.co.uk/rooms/33090114",
        "https://www.airbnb.co.uk/rooms/50633275"]


def get_property_info(url):
    property_info = {"property_name": None, "property_type": None, "bedrooms": None, "bathrooms": None,
                     "amenities": [], "missing_amenities": []}

    driver.get(url)

    # maximising window because the classes change depending on the window size, I found the relevant classes full-screen.
    driver.maximize_window()

    # wait to load all content, may need to wait longer if slower internet connection
    driver.implicitly_wait(1)

    # getting property name
    property_names = driver.find_elements_by_class_name("_fecoyn4")
    # if there is no class that corresponds with the property name, return error message, as it does not exist
    if not property_names:
        return "Property not available."
    else:
        property_info["property_name"] = property_names[0].text

    # getting property type
    property_types = driver.find_elements_by_class_name("_1qsawv5")
    property_info["property_type"] = property_types[0].text

    # getting number of bedrooms
    bedrooms_and_bathrooms = driver.find_elements_by_class_name("_tqmy57")[0].find_elements_by_tag_name("span")
    bedrooms = bedrooms_and_bathrooms[3].text[0]
    bathrooms = bedrooms_and_bathrooms[9].text[0]

    property_info["bedrooms"] = int(bedrooms)
    property_info["bathrooms"] = int(bathrooms)

    # getting amenities list (& missing amenities)
    amenities_button = driver.find_element_by_partial_link_text("amenities")
    # scroll to and click on button
    driver.execute_script("arguments[0].scrollIntoView();", amenities_button)
    driver.execute_script("arguments[0].click();", amenities_button)

    driver.implicitly_wait(1)

    amenities = driver.find_elements_by_class_name("_gw4xx4")
    for i in range(len(amenities)):
        if "Unavailable:" not in amenities[i].text:
            property_info["amenities"].append(amenities[i].text)
        else:
            missing_amenity = amenities[i].text.split("\n")
            property_info["missing_amenities"].append(missing_amenity[1])

    return property_info


for url in URLS:
    print("Info for " + url + ":\n  " + str(get_property_info(url)))
