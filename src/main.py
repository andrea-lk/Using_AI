import json
from notopenai import NotOpenAI
import os
from graphics import Canvas

# go to cs106a.stanford.edu/notopenai and get your free api key
CLIENT = NotOpenAI(api_key="*enter_your_key*")
STORY_NAME = "original_big"
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500

def print_scene(scene):
    #print text of the scene
    print(scene["text"])
    # loop over all choices
    #keep track of each scene choice
    i = 0
    for choice in scene["choices"]:
        i += 1 #keep track of how many choices
        print(str(i) + ". " + str(choice["text"]))

def get_valid_choice(scene):
    #ask user
    user_choice = (input("What do you choose? "))
    while True:
        #check if it's a number
        if user_choice.isdigit():
            user_choice = int(user_choice)
            #check if it's in the valid range
            if (user_choice <= len(scene["choices"]) and user_choice > 0):
                #return correct choice, loop ends here
                return user_choice


        user_choice = (input("Please enter a valid choice: "))

def generate_scene(story_data, current_scene_key):

    print("Suspenseful music plays as the story continues...")
    prompt = ("Return the next scene of a story for key " + str(current_scene_key) +
              "An example scene should be formatted in json like this:" + str(story_data["scenes"]["start"]) +
              "The main plot line of the story is" + str(story_data["plot"]))
    chat_completion = CLIENT.chat.completions.create(
        messages =[{
            "role": "user",
            "content": prompt,
        }],
        model="gpt-3.5-turbo",  # the GPT model to use
        response_format={"type": "json_object"}  # we want our response in json format,
    )
    # get the content of the response
    response_str = chat_completion.choices[0].message.content
    # turn the string into a dictionary using loads
    new_scene_data = json.loads(response_str)

    return new_scene_data

def create_image(current_scene_key, canvas_image):
    path = "img/" + current_scene_key + ".jpg"
    black_path = "img/black_image.png"

    #if we have a valid path
    if os.path.exists(path):

        canvas_image.create_image_with_size(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, path)
        canvas_image.update()

    else:
        #get black screen shot image
        canvas_image.create_image_with_size(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, black_path)

        canvas_image.update()

def main():
    print("Infinite Story")
    story_data = json.load(open('data/original_big.json'))
    canvas_image = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT, "Infinite Story")


    #set first scene
    current_scene_key = "start"
    #show the start scene's image
    create_image(current_scene_key, canvas_image)
    scene = story_data["scenes"]
    end_loop = False

    #while it's a valid scene
    while end_loop is False:
        if current_scene_key in scene:
            #asign block of scene data to the current scene
            scene_data = scene[current_scene_key]
            print(" ")
            print_scene(scene_data)
            valid_choice = get_valid_choice(scene_data)
            current_scene_key = (scene_data["choices"][valid_choice - 1]["scene_key"])
            create_image(current_scene_key, canvas_image)


        else:
            new_scene_data = generate_scene(story_data, current_scene_key)
            scene[current_scene_key] = new_scene_data


if __name__ == "__main__":
    main()
