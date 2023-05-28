import json
import re
import requests
from PIL import Image
from io import BytesIO
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Define the path to your JSON file
json_file_path = r'C:\Users\Igor\OneDrive\Рабочий стол\json\films_2.0.json'

# Define the command to start the bot
def start(update: Update, context: CallbackContext) -> None:
    reply_markup = ReplyKeyboardMarkup([['Комедия', 'Ужасы', 'Фильм-нуар'],
                                        ['Боевик', 'Фантастика', 'Триллер'],
                                        ['Мультфильм', 'Аниме', 'Драма']],
                                       resize_keyboard=True)
    update.message.reply_text('Добро пожаловатьв movi_bot выберите категорию фильмов которые хотели посмотреть:', reply_markup=reply_markup)

# Define the function to handle user messages
def handle_message(update: Update, context: CallbackContext) -> None:
    user_data = context.user_data
    category = update.message.text.lower()

    if category == 'next movie':
        send_next_movie(update, context)
    elif category == 'watched':
        mark_movie_watched(update, context)
    elif category == 'back to categories':
        start(update, context)
    else:
        user_data['category'] = category
        user_data['movies'] = fetch_movies_by_category(category)
        user_data['current_movie_index'] = 0

        if user_data['movies']:
            send_movie(update, context)
        else:
            update.message.reply_text('Нет фильмов по данной категории.')

# Send a movie from the current movie index
def send_movie(update: Update, context: CallbackContext):
    user_data = context.user_data
    movie = user_data['movies'][user_data['current_movie_index']]

    # Check if the movie has been watched
    if movie.get('watched'):
        update.message.reply_text('Ок')
        return

    # Download and resize the image
    img_url = movie['img']
    resized_img = resize_image(img_url, (300, 450))

    # Send the resized image along with movie details
    update.message.reply_photo(photo=resized_img, caption=f"Title: {movie['name']}\nDescription: {movie['first']}",
                               reply_markup=ReplyKeyboardMarkup([['Next Movie', 'Watched', 'Back to Categories']],
                                                              resize_keyboard=True))

# Send the next movie from the current movie index
def send_next_movie(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_data['current_movie_index'] += 1

    if user_data['current_movie_index'] < len(user_data['movies']):
        send_movie(update, context)
    else:
        update.message.reply_text('Нет фильмов по данной категории.')

# Mark the current movie as watched
def mark_movie_watched(update: Update, context: CallbackContext):
    user_data = context.user_data
    current_movie = user_data['movies'][user_data['current_movie_index']]

    # Check if the movie has already been marked as watched
    if current_movie.get('watched'):
        update.message.reply_text('Ок')
        return

    current_movie['watched'] = True
    update.message.reply_text('Запомним')

# Fetch movies by category from the JSON file
def fetch_movies_by_category(category):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    movies = [data[movie_id] for movie_id in data if category.lower() in extract_categories(data[movie_id]['first'].lower())]
    return movies

# Extract categories from movie details
def extract_categories(text):
    return re.findall(r'\b\w+\b', text)

# Resize an image from a given URL to the specified dimensions
def resize_image(url, size):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = img.resize(size)
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    return img_byte_arr

# Create the Updater and pass in the bot token
updater = Updater('6186582985:AAFTPVxM_0-YWvpYpOidhzhprTytiNHSqg0', use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Register the command handler
dispatcher.add_handler(CommandHandler('start', start))

# Register the message handler
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Start the bot
updater.start_polling()
