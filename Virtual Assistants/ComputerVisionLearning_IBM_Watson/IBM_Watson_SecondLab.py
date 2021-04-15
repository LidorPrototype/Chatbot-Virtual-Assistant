# pip install --upgrade ibm-watson --> install it to use this file
from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import urllib.request
import json
from pandas.io.json import json_normalize


# Paste your API key for IBM Watson Visual Recognition below:
my_apikey = 'JiFBdOBY-EE_rukAZCmoZ7kNt65sDNzq0R8qYOtQSmyw'

authenticator = IAMAuthenticator(my_apikey)

visrec = VisualRecognitionV3('2018-03-19',
                             authenticator=authenticator)

# Downloading Beagle dataset
urllib.request.urlretrieve(
    "http://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/CV0101/Dataset/Beagle.zip",
    "beagle.zip")

# Downloading Husky dataset
urllib.request.urlretrieve(
    "http://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/CV0101/Dataset/Husky.zip",
    "husky.zip")

# Downloading Golden Retriever dataset
urllib.request.urlretrieve(
    "http://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/CV0101/Dataset/GoldenRetriever.zip",
    "goldenretriever.zip")  # note that we should remove any hyphens from the zip file name

with open('beagle.zip', 'rb') as beagle, \
        open('goldenretriever.zip', 'rb') as gretriever, \
        open('husky.zip', 'rb') as husky:
    response = visrec.create_classifier(name="dogbreedclassifier",
                                        positive_examples={'beagle': beagle, \
                                                           'goldenretriever': gretriever, \
                                                           'husky': husky})
print(json.dumps(response.get_result(), indent=2))

# lets grab the classifier id
classifier_id = response.get_result()["classifier_id"]
classifier_id

Status = visrec.get_classifier(classifier_id=classifier_id, verbose=True).get_result()['status']
if Status == 'training':
    print("Please, Wait to complete training.......")
else:
    print("Good to go ")

visrec.list_classifiers(verbose=True).get_result()


def getdf_visrec(url, classifier_ids, apikey=my_apikey):
    json_result = visrec.classify(url=url,
                                  threshold='0.6',
                                  classifier_ids=classifier_id).get_result()

    json_classes = json_result['images'][0]['classifiers'][0]['classes']

    df = json_normalize(json_classes).sort_values('score', ascending=False).reset_index(drop=True)

    return df

# GIVES ERRORS YET -->
# getdf_visrec(url = 'https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/CV0101/Dataset/GoldenRetriever1_stacked.jpg',
#             classifier_ids=classifier_id)
#
# getdf_visrec(url = 'http://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/CV0101/Dataset/cat-2083492_960_720.jpg',
#             classifier_ids=classifier_id)
#<--


classifiers = visrec.list_classifiers(verbose=True).get_result()['classifiers']
print(json.dumps(classifiers, indent=2))