# OCR Translator App
Technologies used: Google's Cloud Vision and Translate APIs, PyQt, OpenCV, Python

This app translates text contained in images into different languages, and overlays the results onto the original image. The app could be used in foreign language classrooms where students find themselves having to translate many words and phrases in reading assignments. This app could save time by overlaying translations onto images of the assignment, allowing students to translate unknown words or phrases seamlessly. This application could also be used to translate legal documents/forms for non-native speakers. A mobile version could be used to translate street signs, flyers and documents when traveling abroad.

# Using the App

Note, you must have a Google Cloud Developer account and project configured on your machine with Google Cloud Translate and Vision APIs enabled. This is because I have NOT provided the API keys associated with my account/project configuration to prevent charges from being billed to my account. 

Launch the application by running app_driver.py.

![Alt text](images/launch.PNG?raw=true "Application immediately after launch.")


Either select an existing image or take a new image using the buttons.

![Alt text](images/loadimage.PNG?raw=true "Application immediately after launch.")


Select a language using the combo box, and click the "Translate Text in Image" button.

![Alt text](images/runtranslation.PNG?raw=true "Application immediately after launch.")


Simply hover over each word with your cursor to reveal the translation!

![Alt text](images/hover.png?raw=true "Application immediately after launch.")
