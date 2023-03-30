import telegram
import requests
import instaloader
import os

# Initialize Telegram bot with token
bot = telegram.Bot("5687597141:AAFRNwvC7QTYpca0ih1B9n7zRQVPPH7WntQ")

# Initialize Instaloader
L = instaloader.Instaloader()

# Define a function to download and send media to Telegram
def download_and_send_media(post, chat_id):
    # Download the media file
    L.download_post(post, target=f"{post.owner_username}_{post.shortcode}")
    # Send the media file to Telegram
    with open(f"{post.owner_username}_{post.shortcode}/{post.date_utc}_{post.shortcode}.mp4", "rb") as f:
        bot.send_video(chat_id=chat_id, video=f)
    # Delete the media file
    os.remove(f"{post.owner_username}_{post.shortcode}/{post.date_utc}_{post.shortcode}.mp4")

# Define a function to handle incoming messages
def handle_message(update, context):
    # Get the chat ID
    chat_id = update.message.chat_id
    # Get the Instagram post URL
    post_url = update.message.text
    # Load the post
    post = instaloader.Post.from_shortcode(L.context, post_url.split("/")[-1])
    # Check if the post is a picture or a video
    if post.is_video:
        # If the post is a video, download and send the video
        download_and_send_media(post, chat_id)
    else:
        # If the post is a picture, download and send the picture
        L.download_pic(post, target=f"{post.owner_username}_{post.shortcode}")
        with open(f"{post.owner_username}_{post.shortcode}/{post.date_utc}_{post.shortcode}.jpg", "rb") as f:
            bot.send_photo(chat_id=chat_id, photo=f)
        os.remove(f"{post.owner_username}_{post.shortcode}/{post.date_utc}_{post.shortcode}.jpg")

# Start the Telegram bot and add the message handler
updater = telegram.ext.Updater("5687597141:AAFRNwvC7QTYpca0ih1B9n7zRQVPPH7WntQ", use_context=True)
updater.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))
updater.start_polling()
updater.idle()
