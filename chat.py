import random
import json
import torch
import requests
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
import wikipedia

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"

#Function to convert kelvin to celsius
def kelvin_to_celsius(kelvin):
    celsius = kelvin - 273.15
    return round(celsius)

def weather_details(city):
    api_key = 'INSERT YOUR OWN API KEY HERE'
    country_code = 'MY'
    city_name = city
    search_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name},{country_code}&appid={api_key}'

    # Make the API call to search for the movie
    response2 = requests.get(search_url)

    if response2.status_code == 200:
        data = response2.json()
        if len(data) > 0:
            city = data['name']
            temp_celsius = kelvin_to_celsius(data['main']['temp'])
            formatted_celsius = f'{temp_celsius}°C'
            description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            formatted_humidity = f'{humidity}%'
            wind_speed = data['wind']['speed']
            formatted_wind = f'{wind_speed}m/s'

            city_details = {
                    'city': city,
                    'celsius': formatted_celsius,
                    'description': description,
                    'humidity': formatted_humidity,
                    'Wind Speed': formatted_wind }

            return city_details
        else:
            print(f'No results found for {city}')
    else:
        print(f'Failed to retrieve data for {city}')

    return None

def get_movie_details(title):
    api_key = 'INSERT YOUR OWN API KEY HERE'
    search_url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={title}'

    # Make the API call to search for the movie
    response = requests.get(search_url)

    if response.status_code == 200:
        data = response.json()
        results = data['results']
        if len(results) > 0:
            movie = results[0]
            title = movie['title']
            overview = movie['overview']
            release_date = movie['release_date']
            vote_average = movie['vote_average']
            vote_count = movie['vote_count']
            budget = movie['budget'] if 'budget' in movie else 'N/A'
            revenue = movie['revenue'] if 'revenue' in movie else 'N/A'
            popularity = movie['popularity']

            # Make a second API call to get the movie details
            details_url = f'https://api.themoviedb.org/3/movie/{movie["id"]}?api_key={api_key}&language=en-US&append_to_response=runtime'
            response = requests.get(details_url)
            if response.status_code == 200:
                details = response.json()
                production_countries = [country['name'] for country in details['production_countries']]
                production_companies = [company['name'] for company in details['production_companies']]
                genres = [genre['name'] for genre in details['genres']]
                runtime = details['runtime']

                movie_details = {
                    'title': title,
                    'overview': overview,
                    'release_date': release_date,
                    'vote_average': vote_average,
                    'vote_count': vote_count,
                    'runtime': runtime,
                    'budget': budget,
                    'revenue': revenue,
                    'popularity': popularity,
                    'production_countries': production_countries,
                    'production_companies': production_companies,
                    'genres': genres
                }

                return movie_details
            else:
                print(f'Failed to retrieve data for {title}')
        else:
            print(f'No results found for {title}')
    else:
        print(f'Failed to retrieve data for {title}')

    return None

def get_response(msg):
    if msg.startswith("!movie"):
        movie_title = msg[7:]  # Remove "!movie" prefix from the message
        movie_details = get_movie_details(movie_title)
        if movie_details:
            # Process and display the movie details in your chatbot's response
            response = f"Here are the details for the movie:<br><br>"
            response += f"Title: {movie_details['title']}<br><br>"
            response += f"Overview: {movie_details['overview']}<br><br>"
            response += f"Release Date: {movie_details['release_date']}<br>"
            response += f"Runtime: {movie_details['runtime']} minutes<br><br>"
            response += f"Budget: {movie_details['budget']}<br><br>"
            response += f"Revenue: {movie_details['revenue']}<br>" if movie_details['revenue'] != 'N/A' else "Revenue: N/A<br><br>"
            response += f"Production Companies: {', '.join(movie_details['production_companies'])}<br><br>"
            response += f"Genres: {', '.join(movie_details['genres'])}<br>"

            return response
        
    elif msg.startswith("!wiki"):
        search_query = msg[5:]  # Remove "wiki:" prefix from the message
        try:
            page = wikipedia.page(wikipedia.search(search_query)[0])
            return page.summary
        except wikipedia.exceptions.PageError:
            return "Sorry, I couldn't find any Wikipedia page matching your query."
        except wikipedia.exceptions.DisambiguationError as e:
            options = e.options[:5]  # Limit the number of options shown
            return f"Your query is ambiguous. Here are some options:\n\n{', '.join(options)}"
        
    elif msg.startswith("!weather"):
        search_city = msg[9:] # remove !weather
        weather = weather_details(search_city)
        if weather:
            response2 = f"Here are the weather details for {search_city}<br><br>"
            response2 += f"City: {weather['city']}<br><br>"
            response2 += f"Temperature: {weather['celsius']}<br><br>"
            response2 += f"Weather Description: {weather['description']}<br><br>"
            response2 += f"Humidity: {weather['humidity']}<br><br>"
            response2 += f"Wind Speed: {weather['Wind Speed']}<br><br>" 

        return response2
    elif msg.startswith("!info"):
        response = "Greetings! I'm a personal chatbot created by OngAJ to help answer questions about him. "
        response += "Refer below for ideas on what you can ask me :)<br><br>"
        response += "1) Get to know OngAJ by asking me about his background, education, work experiences, future plans, skills, hobbies, spoken languages, birthday, age.<br><br>"
        response += "2) If you're not interested to know more about OngAJ, I was built with some additional features that you might find interesting! Type !commands for more information."
        
        return response
    elif msg.startswith("!commands"):
        response = "Use the command !movie followed by a movie title to receive a summarized description of your movie. For example, !movie spiderman 3 <br><br>"
        response += "Use the command !wiki followed by a query to receive a summarized description of your topic. For example, !wiki tiger. <br><br>"
        response += "Use the command !weather followed by a city in malaysia to receive a weather report of your city. For example, you can try !weather petaling jaya."
        return response
    elif msg.startswith("!links"):
        response = "Here's all the relevant links you may find helpful!<br><br>"
        response += "<a href='https://github.com/ongaunjie1' style='color: blue;text-decoration: underline' target='_blank'>OngAJ's GitHub Profile</a><br><br>"
        response += "<a href='https://www.linkedin.com/in/ongaunjie/' style='color: blue;text-decoration: underline' target='_blank'>OngAJ's Linkedin Profile</a><br><br>"
        response += "<a href='https://drive.google.com/file/d/15BgQuUlHtsDVZKWghgU53hrOrkBryYmp/view' style='color: blue;text-decoration: underline' target='_blank'>OngAJ's Resume</a><br><br>"
        response += "You may also click on the social icons on the left-side of the website to navigate to these links as well"
        return response
    else:
        sentence = tokenize(msg) #this is for intents
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)

        output = model(X)
        _, predicted = torch.max(output, dim=1)

        tag = tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > 0.75:
            for intent in intents['intents']:
                if tag == intent["tag"]:
                    return random.choice(intent['responses']) #return random response from the intents.json

        return "I do not understand..."

if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)
