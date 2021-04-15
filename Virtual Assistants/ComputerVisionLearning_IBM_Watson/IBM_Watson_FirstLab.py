#pip install --upgrade ibm-watson opencv-python    --> install it in order to work with this file

import cv2
import urllib.request
from matplotlib import pyplot as plt
from pylab import rcParams
from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
from pandas.io.json import json_normalize


# Paste your API key for IBM Watson Visual Recognition below:
my_apikey = 'JiFBdOBY-EE_rukAZCmoZ7kNt65sDNzq0R8qYOtQSmyw'
authenticator = IAMAuthenticator(my_apikey)


def getdf_visrec(url, apikey=my_apikey):
    json_result = visrec.classify(url=url,
                                  threshold='0.6',
                                  classifier_ids='default').get_result()

    json_classes = json_result['images'][0]['classifiers'][0]['classes']

    df = json_normalize(json_classes).sort_values('score', ascending=False).reset_index(drop=True)

    return df


def plt_image(image_url, size=(10, 8)):
    # Downloads an image from a URL, and displays it in the notebook
    urllib.request.urlretrieve(image_url, "image.jpg")  # downloads file as "image.jpg"
    image = cv2.imread("image.jpg")

    # If image is in color, then correct color coding from BGR to RGB
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    rcParams['figure.figsize'] = size[0], size[1]  # set image display size

    plt.axis("off")
    plt.imshow(image, cmap="Greys_r")
    plt.show()


visrec = VisualRecognitionV3('2018-03-19',
                             authenticator=authenticator)

# threshold is set to 0.6, that means only classes that has a confidence score of 0.6 or greater will be shown
# classes = visrec.classify(url=image_url,
#                           threshold='0.6',
#                           classifier_ids='default').get_result()

# plt_image(image_url)
# print(json.dumps(classes, indent=2))

# url = 'http://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/CV0101/Images/76011_MAIN._AC_SS190_V1446845310_.jpg'
# plt_image(url)
# getdf_visrec(url)

url = 'http://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/CV0101/Images/2880px-Kyrenia_01-2017_img04_view_from_castle_bastion.jpg'
plt_image(url)
getdf_visrec(url)