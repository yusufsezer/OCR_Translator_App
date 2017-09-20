import collections
from google.cloud import vision
from google.cloud import translate

WordBox = collections.namedtuple('WordBox', ['word', 'geometry'])


class ImageTranslator:
    """Handles requests to the Google Cloud Vision and Translate APIs

    :type target_language: str
    :param target_language: the target language to which text will be translated. If not passed, defaults to 'en',
                            resulting in translations into English.
    """

    __vision_client = vision.Client()
    __translate_client = translate.Client()

    def __init__(self, target_language='en'):
        self.__target_language = target_language

    def set_target_language(self, target_language):
        """Set the target language for translation requests sent to Google's Cloud Translate API

        :type target_language: str
        :param two letter language code for the target language

        :rtype None
        """
        self.__target_language = target_language

    def translate_image_text(self, image_data):
        """Detect and translate each word in the image, and construct a list of WordBox namedtuples.

        :type image_data: bytes
        :param image_data: pointer to the image data to extract/translate text from

        :rtype: list
        :returns: a list of WordBox namedtuples. Each WordBox encapsulates a word's translation and the vertices of its
                  bounding polygon
        """

        img_to_translate = ImageTranslator.__vision_client.image(content=image_data)
        text_to_translate = img_to_translate.detect_text()

        word_boxes = []
        for word_data in text_to_translate[1:]:
            translated_word = ImageTranslator.__translate_client.translate(word_data.description,
                                                                           target_language=self.__target_language)
            boundary_vertices = word_data.bounds.vertices
            box = []
            for vertex in boundary_vertices:
                box.append((vertex.x_coordinate, vertex.y_coordinate))
            word_boxes.append(WordBox(word=translated_word['translatedText'], geometry=box))

        return word_boxes
