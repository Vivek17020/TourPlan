import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import folium_static

HERE_API_KEY = "8hZQjseNSzHPrBqes_m-_kKdKFO0sXnYxVh9EhPFzNg"

logo_url = "tour.png"

def geocode(address):
    base_url = "https://geocode.search.hereapi.com/v1/geocode"
    params = {"q": address, "apiKey": HERE_API_KEY}
    response = requests.get(base_url, params=params)
    data = response.json()
    if data.get("items"):
        location = data["items"][0]["position"]
        return location
    return None

def calculate_route(start, end):
    base_url = "https://route.ls.hereapi.com/routing/7.2/calculateroute.json"
    params = {
        "waypoint0": f"{start['lat']},{start['lng']}",
        "waypoint1": f"{end['lat']},{end['lng']}",
        "mode": "fastest;car",
        "apiKey": HERE_API_KEY,
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data

def get_city_tours(city):
    city_tours = {
        "Paris": ["Eiffel Tower Tour", "Louvre Museum Tour"],
        "New York": ["Statue of Liberty Tour", "Central Park Tour"],
        "Mumbai": ["Gateway of India Tour", "Marine Drive Tour", "Elephanta Caves Tour"],
        "Italy": ["Colosseum in Rome Tour", "St. Mark's Square in Venice Tour", "Florence Cathedral (Duomo) Tour"]
    }
    return city_tours.get(city, [])


def get_tour_description(tour):
    tour_descriptions = {
        "Eiffel Tower Tour": "Explore the iconic Eiffel Tower in Paris, where wrought-iron craftsmanship meets panoramic views. Ascend to breathtaking heights and immerse yourself in the romantic ambiance of the City of Lights.",
        "Louvre Museum Tour": "Discover the world's largest art museum in Paris, the Louvre. Home to thousands of masterpieces, including the Mona Lisa, this cultural journey promises an enriching experience through the realms of art and history.",
        "Statue of Liberty Tour": "Visit the symbol of freedom in the USA with the Statue of Liberty Tour. Explore Liberty Island, marvel at the statue's grandeur, and learn about its profound significance in American history.",
        "Central Park Tour": "Explore the iconic park in the heart of Manhattan with the Central Park Tour. Stroll through picturesque landscapes, iconic landmarks, and vibrant greenery, experiencing the tranquility within the bustling metropolis.",
        "Gateway of India Tour": "Immerse yourself in the historic charm of Mumbai with the Gateway of India Tour. This architectural marvel by the Arabian Sea narrates tales of colonial-era splendor, serving as a timeless symbol of India's cultural heritage.",
        "Marine Drive Tour": "Experience the scenic Marine Drive in Mumbai.Experience the scenic Marine Drive in Mumbai, a captivating seaside promenade. Enjoy the mesmerizing views of the Arabian Sea, city skyline, and glittering lights, making it a perfect destination for a leisurely stroll.",
        "Colosseum in Rome Tour": "Discover the ancient Colosseum in Rome, where gladiatorial contests unfolded amidst architectural marvels. Step back in time to witness the grandeur of Roman engineering and the historical significance of this iconic amphitheater.",
        "St. Mark's Square in Venice Tour": "Immerse yourself in the historic charm of St. Mark's Square in Venice. Admire the architectural wonders, including St. Mark's Basilica and the Campanile, as you wander through this enchanting piazza surrounded by Venetian beauty.",
        "Florence Cathedral (Duomo) Tour": "Visit the iconic Florence Cathedral in Florence, a masterpiece of Renaissance architecture. Marvel at the intricate details of the Duomo, baptistery, and campanile, as you delve into the artistic and religious heritage of this enchanting Italian city."
    }
    return tour_descriptions.get(tour, "")

def get_tour_location(tour):
    tour_locations = {
        "Eiffel Tower Tour": geocode("Paris, France"),
        "Louvre Museum Tour": geocode("Paris, France"),
        "Statue of Liberty Tour": geocode("New York, USA"),
        "Central Park Tour": geocode("New York, USA"),
        "Gateway of India Tour": geocode("Mumbai, India"),
        "Marine Drive Tour": geocode("Mumbai, India"),
        "Elephanta Caves Tour": geocode("Mumbai, India"),
        "Colosseum in Rome Tour": geocode("Rome, Italy"),
        "St. Mark's Square in Venice Tour": geocode("Venice, Italy"),
        "Florence Cathedral (Duomo) Tour": geocode("Florence, Italy")
    }
    return tour_locations.get(tour, None)

def display_selected_tour_info(selected_tour, city_coordinates):
    st.subheader(f"{selected_tour} - Tour Information")
    st.write("Description:", get_tour_description(selected_tour))

    # Display map with the location of the selected tour
    tour_location = get_tour_location(selected_tour)
    if tour_location:
        st.map(pd.DataFrame({"LAT": [tour_location["lat"]], "LON": [tour_location["lng"]]}), zoom=15)
    else:
        st.warning("Location not available for the selected tour.")

def get_historical_info_with_images(city):
    historical_info = {
        "Paris": [
            {"title": "Notre-Dame Cathedral", "info": "🏰 Historic Gothic cathedral, a masterpiece of medieval architecture. Discover its rich history and intricate design.", "image_url": "Notre-Dame-Cathedral.jpg", "animation_url": None, "tooltip": "Click to learn more"},
            {"title": "Versailles Palace", "info": "👑 Opulent royal palace with stunning gardens. Immerse yourself in the splendor of French royalty at Versailles.", "image_url": "https://media-manager.starsinsider.com/gallery/1080/na_615706509010e.jpg"}
        ],
        "New York": [
            {"title": "Ellis Island", "info": "🗺️ Immigration museum, witness the gateway to America's immigrant past. Explore the compelling stories of those who arrived seeking a new life.", "image_url": "https://i.redd.it/8iibeqzc8dz41.jpg"},
            {"title": "Empire State Building", "info": "🏙️ Iconic skyscraper, a symbol of the New York skyline. Soar to the top for panoramic views of the city that never sleeps.", "image_url": "https://images.fineartamerica.com/images-medium-large-5/iconic-new-york-city-flatiron-building-mark-e-tisdale.jpg"}
        ],
        "Mumbai": [
            {"title": "Gateway of India", "info": "⛩️ Historic monument and tourist attraction. Marvel at the grand arch overlooking the Arabian Sea, a landmark of Mumbai.", "image_url": "https://www.lasociedadgeografica.com/blog/uploads/2020/08/media-india-group-the-gateway-of-india-scaled.jpg"},
            {"title": "Marine Drive", "info": "🌅 Scenic promenade along the Arabian Sea. Enjoy breathtaking sunsets and the rhythmic charm of the 'Queen's Necklace.'", "image_url": "https://www.adotrip.com/public/images/areas/5c53e68d4a6a3-Marine%20Drive%20Sight%20Seeing%20Tour.jpg"},
            {"title": "Elephanta Caves", "info": "🗿 Ancient rock-cut caves on Elephanta Island. Explore the UNESCO site with remarkable sculptures and a glimpse into India's past.", "image_url": "https://tse3.mm.bing.net/th?id=OIP.vITGx8tnRwFTP8ik_aTzrgAAAA&pid=Api&P=0&h=450"}  # Adjusted image size
        ],
        "Italy": [
            {"title": "Colosseum in Rome", "info": "🏛️ Discover the ancient Colosseum, an iconic amphitheater. Immerse yourself in the spectacles of gladiatorial contests and Roman history.", "image_url": "http://traveldigg.com/wp-content/uploads/2016/05/Colosseum-Photography.jpg"},
            {"title": "St. Mark's Square in Venice", "info": "🏰 Explore the historic St. Mark's Square. Admire the grandeur of St. Mark's Basilica and the Campanile in this enchanting Venetian piazza.", "image_url": "https://d6qyz3em3b312.cloudfront.net/upload/images/media/2019/10/11/shutterstock_667311706.2048x1024.jpg"},
            {"title": "Florence Cathedral (Duomo)", "info": "⛪ Visit the iconic Florence Cathedral. Marvel at the Duomo's architectural beauty, a masterpiece of Renaissance design.", "image_url": "https://images-e-venise.global.ssl.fastly.net/pics/musees-florence/tour-arnolfo/palazzo-vecchio-tour-arnolfo-vue-aerienne-duomo-campanile-giotto-florence-italie-14.jpg"}
        ]
    }
    return historical_info.get(city, [])




st.sidebar.image(logo_url, width=200)
# Sidebar
st.sidebar.title("Lets Travel Together")
selected_city = st.sidebar.selectbox("Select a city/Country:", ["Paris", "New York","Mumbai", "Italy"])

# Get coordinates for the selected city
city_coordinates = geocode(selected_city + ", Country")

# Main content area
st.title(f"🗺️ Tourism and City Exploration App - {selected_city}")

# Guided Tours Section
st.header("🚶‍♂️ Guided Tours 🚶‍♀️")

city_tours = get_city_tours(selected_city)

# Dropdown for selecting a specific tour
selected_tour = st.selectbox("Select a tour:", city_tours if city_tours else [])
if selected_tour:
    display_selected_tour_info(selected_tour, city_coordinates)
else:
    st.write("No tours available for the selected city.")

# Historical Information Section
st.header("Historical Information")

historical_info_data = get_historical_info_with_images(selected_city)
if historical_info_data:
    for info in historical_info_data:
        st.subheader(info["title"])
        st.write("Information:", info["info"])
        st.image(info["image_url"], caption='Image', use_column_width=True)
else:
    st.write("No historical information available for the selected city.")

# Interactive Map Section
st.title("Route Planning ")

# Check if the selected city is Paris or New York
# Check if the selected city is Paris
if selected_city == "Paris":
    # Define the coordinates for tourist attractions in Paris
    eiffel_tower_location = {"lat": 48.8588, "lng": 2.2944}  # Eiffel Tower
    louvre_museum_location = {"lat": 48.8606, "lng": 2.3376}  # Louvre Museum
    notre_dame_location = {"lat": 48.8530, "lng": 2.3499}  # Notre-Dame Cathedral

    # Display the map for Paris
    m_paris = folium.Map(location=(eiffel_tower_location["lat"], eiffel_tower_location["lng"]), zoom_start=14)

    # Add tourist attraction markers for Paris
    folium.Marker(location=(eiffel_tower_location["lat"], eiffel_tower_location["lng"]), popup="Eiffel Tower").add_to(m_paris)
    folium.Marker(location=(louvre_museum_location["lat"], louvre_museum_location["lng"]), popup="Louvre Museum").add_to(m_paris)
    folium.Marker(location=(notre_dame_location["lat"], notre_dame_location["lng"]), popup="Notre-Dame Cathedral").add_to(m_paris)

    # Add connections between tourist attractions in Paris
    route_coordinates_eiffel_to_louvre = [
        (eiffel_tower_location["lat"], eiffel_tower_location["lng"]),
        (louvre_museum_location["lat"], louvre_museum_location["lng"]),
    ]

    route_coordinates_louvre_to_notre_dame = [
        (louvre_museum_location["lat"], louvre_museum_location["lng"]),
        (notre_dame_location["lat"], notre_dame_location["lng"]),
    ]

    route_coordinates_eiffel_to_notre_dame = [
        (eiffel_tower_location["lat"], eiffel_tower_location["lng"]),
        (notre_dame_location["lat"], notre_dame_location["lng"]),
    ]

    # Add route polyline from Eiffel Tower to Louvre Museum (red color)
    folium.PolyLine(locations=route_coordinates_eiffel_to_louvre, color="red", weight=5, opacity=0.7).add_to(m_paris)

    # Add route polyline from Louvre Museum to Notre-Dame Cathedral (blue color)
    folium.PolyLine(locations=route_coordinates_louvre_to_notre_dame, color="blue", weight=5, opacity=0.7).add_to(m_paris)

    # Add route polyline from Eiffel Tower to Notre-Dame Cathedral (red color)
    folium.PolyLine(locations=route_coordinates_eiffel_to_notre_dame, color="red", weight=5, opacity=0.7).add_to(m_paris)

    # Display the map for Paris
    folium_static(m_paris)


# Check if the selected city is New York
elif selected_city == "New York":
    # Define the coordinates for tourist attractions in New York
    statue_of_liberty_location = {"lat": 40.6892, "lng": -74.0445}  # Statue of Liberty
    central_park_location = {"lat": 40.7851, "lng": -73.9683}  # Central Park
    empire_state_building_location = {"lat": 40.7488, "lng": -73.9857}  # Empire State Building

    # Display the map for New York
    m_ny = folium.Map(location=(statue_of_liberty_location["lat"], statue_of_liberty_location["lng"]), zoom_start=14)

    # Add tourist attraction markers for New York
    folium.Marker(location=(statue_of_liberty_location["lat"], statue_of_liberty_location["lng"]), popup="Statue of Liberty").add_to(m_ny)
    folium.Marker(location=(central_park_location["lat"], central_park_location["lng"]), popup="Central Park").add_to(m_ny)
    folium.Marker(location=(empire_state_building_location["lat"], empire_state_building_location["lng"]), popup="Empire State Building").add_to(m_ny)

    # Add connections between tourist attractions in New York
    route_coordinates_statue_of_liberty_to_central_park = [
        (statue_of_liberty_location["lat"], statue_of_liberty_location["lng"]),
        (central_park_location["lat"], central_park_location["lng"]),
    ]

    route_coordinates_central_park_to_empire_state_building = [
        (central_park_location["lat"], central_park_location["lng"]),
        (empire_state_building_location["lat"], empire_state_building_location["lng"]),
    ]

    route_coordinates_statue_of_liberty_to_empire_state_building = [
        (statue_of_liberty_location["lat"], statue_of_liberty_location["lng"]),
        (empire_state_building_location["lat"], empire_state_building_location["lng"]),
    ]

    # Add route polyline from Statue of Liberty to Central Park (red color)
    folium.PolyLine(locations=route_coordinates_statue_of_liberty_to_central_park, color="red", weight=5, opacity=0.7).add_to(m_ny)

    # Add route polyline from Central Park to Empire State Building (blue color)
    folium.PolyLine(locations=route_coordinates_central_park_to_empire_state_building, color="blue", weight=5, opacity=0.7).add_to(m_ny)

    # Add route polyline from Statue of Liberty to Empire State Building (red color)
    folium.PolyLine(locations=route_coordinates_statue_of_liberty_to_empire_state_building, color="red", weight=5, opacity=0.7).add_to(m_ny)

    # Display the map for New York
    folium_static(m_ny)

elif selected_city == "Mumbai":
    # Define the coordinates for tourist attractions in Mumbai, India
    gateway_of_india_location = {"lat": 18.9217, "lng": 72.8342}  # Gateway of India
    marine_drive_location = {"lat": 18.9433, "lng": 72.8245}  # Marine Drive
    elephanta_caves_location = {"lat": 18.9647, "lng": 72.9310}  # Elephanta Caves

    # Display the map for Mumbai, India
    m_mumbai = folium.Map(location=(gateway_of_india_location["lat"], gateway_of_india_location["lng"]), zoom_start=14)

    # Add tourist attraction markers for Mumbai, India
    folium.Marker(location=(gateway_of_india_location["lat"], gateway_of_india_location["lng"]), popup="Gateway of India").add_to(m_mumbai)
    folium.Marker(location=(marine_drive_location["lat"], marine_drive_location["lng"]), popup="Marine Drive").add_to(m_mumbai)
    folium.Marker(location=(elephanta_caves_location["lat"], elephanta_caves_location["lng"]), popup="Elephanta Caves").add_to(m_mumbai)

    # Add connections between tourist attractions in Mumbai, India
    route_coordinates_gateway_to_marine_drive = [
        (gateway_of_india_location["lat"], gateway_of_india_location["lng"]),
        (marine_drive_location["lat"], marine_drive_location["lng"]),
    ]

    route_coordinates_marine_drive_to_elephanta_caves = [
        (marine_drive_location["lat"], marine_drive_location["lng"]),
        (elephanta_caves_location["lat"], elephanta_caves_location["lng"]),
    ]

    route_coordinates_gateway_to_elephanta_caves = [
        (gateway_of_india_location["lat"], gateway_of_india_location["lng"]),
        (elephanta_caves_location["lat"], elephanta_caves_location["lng"]),
    ]

    # Add route polyline from Gateway of India to Marine Drive (red color)
    folium.PolyLine(locations=route_coordinates_gateway_to_marine_drive, color="red", weight=5, opacity=0.7).add_to(m_mumbai)

    # Add route polyline from Marine Drive to Elephanta Caves (blue color)
    folium.PolyLine(locations=route_coordinates_marine_drive_to_elephanta_caves, color="blue", weight=5, opacity=0.7).add_to(m_mumbai)

    # Add route polyline from Gateway of India to Elephanta Caves (red color)
    folium.PolyLine(locations=route_coordinates_gateway_to_elephanta_caves, color="red", weight=5, opacity=0.7).add_to(m_mumbai)

    # Display the map for Mumbai, India
    folium_static(m_mumbai)

elif selected_city == "Italy":
    # Define the coordinates for tourist attractions in Italy
    rome_colosseum_location = {"lat": 41.8902, "lng": 12.4924}  # Colosseum in Rome
    venice_st_mark_location = {"lat": 45.4345, "lng": 12.3390}  # St. Mark's Square in Venice
    florence_duomo_location = {"lat": 43.7733, "lng": 11.2558}  # Florence Cathedral (Duomo)

    # Display the map for Italy
    m_italy = folium.Map(location=(rome_colosseum_location["lat"], rome_colosseum_location["lng"]), zoom_start=14)

    # Add tourist attraction markers for Italy
    folium.Marker(location=(rome_colosseum_location["lat"], rome_colosseum_location["lng"]), popup="Colosseum in Rome").add_to(m_italy)
    folium.Marker(location=(venice_st_mark_location["lat"], venice_st_mark_location["lng"]), popup="St. Mark's Square in Venice").add_to(m_italy)
    folium.Marker(location=(florence_duomo_location["lat"], florence_duomo_location["lng"]), popup="Florence Cathedral (Duomo)").add_to(m_italy)

    # Add connections between tourist attractions in Italy
    route_coordinates_rome_to_venice = [
        (rome_colosseum_location["lat"], rome_colosseum_location["lng"]),
        (venice_st_mark_location["lat"], venice_st_mark_location["lng"]),
    ]

    route_coordinates_venice_to_florence = [
        (venice_st_mark_location["lat"], venice_st_mark_location["lng"]),
        (florence_duomo_location["lat"], florence_duomo_location["lng"]),
    ]

    route_coordinates_rome_to_florence = [
        (rome_colosseum_location["lat"], rome_colosseum_location["lng"]),
        (florence_duomo_location["lat"], florence_duomo_location["lng"]),
    ]

    # Add route polyline from Rome to Venice (red color)
    folium.PolyLine(locations=route_coordinates_rome_to_venice, color="red", weight=5, opacity=0.7).add_to(m_italy)

    # Add route polyline from Venice to Florence (blue color)
    folium.PolyLine(locations=route_coordinates_venice_to_florence, color="blue", weight=5, opacity=0.7).add_to(m_italy)

    # Add route polyline from Rome to Florence (red color)
    folium.PolyLine(locations=route_coordinates_rome_to_florence, color="red", weight=5, opacity=0.7).add_to(m_italy)

    # Display the map for Italy
    folium_static(m_italy)