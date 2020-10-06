# ByteNet
ByteNet is a social networking site built with django and bootstrap. 

Project is live at : https://bytenet.pythonanywhere.com/


## Functionalities


Things you can do on ByteNet:-

1. Create account

2. Make friends by sending and accepting friend requests

3. Share images, music, youtube videos and much more with your friends

4. Like and Dislike the posts on your feed

5. Tag friends and be part of the conversation

6. Find users on the website

7. See what everyone is up to in your feed

8. Catch on with latest trends,news and memes.

and also, posts, here, are called "bytes" : )

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Feel free to open issues with appropriate tags.

## Running the Django app
1. Create a `virtualenv` for running the app.
    - Run `python3 -m venv myvenv` inside `bytenet` folder.
    - Run `source myvenv/bin/activate` to start virtual environment.
    - Run `pip3 install requirements.txt`.
2. Migrate the models.
    - Run `python3 manage.py makemigrations`.
    - Run `python3 manage.py migrate`.
3. Run the server.
    - Run `python3 manage.py runserver`
And that's it.
## secrets.py and credentials
        
- To run some functions you will need some credentials.
- Create a `python` file called `secrets.py` in `constants` directory.

###     imgur credentials

- Head over to https://apidocs.imgur.com/ and get the necessary credentials and add them to `constants/secrets.py`.
- You will need these 2 credentials: `IMGUR_CLIENT_ID` and `IMGUR_CLIENT_SECRET`.

###     link_preview credentials
            
- Head over to https://www.linkpreview.net/ and get the necessary credentials and add them to `constants/secrets.py`.
- You will need just one credentials: `LINK_PREVIEW_KEY`.

###     reddit credentials
            
- For running `god_script.py` you will have to get reddit credentials.
- Head over to https://www.reddit.com/dev/api/ and get these credentials `REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD, REDDIT_APP_NAME` and store it in `constants/secrets.py`. 