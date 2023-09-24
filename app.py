import requests
import json

def get_african_countries():
    # Fetch the list of all countries from the REST Countries API
    response = requests.get("https://restcountries.com/v3.1/all")
    
    if response.status_code == 200:
        countries_data = response.json()
        african_countries = []

        # Filter countries that are in Africa and extract relevant information
        for country in countries_data:
            if "region" in country and country["region"] == "Africa":
                country_info = {
                    "name": country.get("name", {}).get("common", ""),
                    "capital": country.get("capital", [])[0],
                    "currency": country.get("currencies", {}).get("USD", {}).get("name", ""),
                    "regions": country.get("region", []),
                }
                african_countries.append(country_info)

        return african_countries
    else:
        print("Failed to fetch data from the REST Countries API.")
        return []

def get_cities_for_country(country_name):
    # Fetch city data for a specific country using the GeoNames API
    base_url = "http://api.geonames.org/searchJSON"
    params = {
        "q": country_name,
        "country": country_name,
        "featureClass": "P",
        "maxRows": 10,  
        "username": "degraft",
        #getting cities failed!
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        city_data = response.json()
        return city_data.get("geonames", [])
    else:
        print(f"Failed to fetch city data for {country_name} from GeoNames API.")
        return []

def main():
    african_countries = get_african_countries()

    if african_countries:
        for country in african_countries:
            country_name = country["name"]
            cities = get_cities_for_country(country_name)
            country["cities"] = cities

        # Save the African countries data (including cities) to a JSON file
        with open("african_countries_with_cities.json", "w", encoding="utf-8") as json_file:
            json.dump(african_countries, json_file, ensure_ascii=False, indent=4)
        
        print("African countries data (including cities) has been saved to 'african_countries_with_cities.json'.")
    else:
        print("No African countries data found.")

if __name__ == "__main__":
    main()
