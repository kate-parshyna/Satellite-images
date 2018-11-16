# from azure.cognitiveservices.vision.customvision.prediction import prediction_endpoint
#
# # Replace with a valid key
# #training_key = "<your training key>"
# prediction_key = "d068af02c24b42b498f049e8dcad6a7a"
#
# predictor = prediction_endpoint.PredictionEndpoint(prediction_key)
#
# test_data = 'output/aerialImage_target_image.jpeg'
#
# project = 'farmhouse'
#
# results = predictor.predict_image_url(project_id=project, test_data=test_data)
#
# # Alternatively, if the images were on disk in a folder called Images alongside the sample.py, then
# # they can be added by using the following.
# #
# # Open the sample image and get back the prediction results.
# # with open("Images\\test\\test_image.jpg", mode="rb") as test_data:
# #     results = predictor.predict_image(project.id, test_data, iteration.id)
#
# # Display the results.
# for prediction in results.predictions:
#     print ("\t" + prediction.tag_name + ": {0:.2f}%".format(prediction.probability * 100))


from azure.cognitiveservices.vision.customvision.prediction import prediction_endpoint

project = 'f3c7ba04-ee4e-4b42-a4f4-fd116b1788c1'
prediction_key = 'd068af02c24b42b498f049e8dcad6a7a'
base_image_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-CustomVision-Windows/master/Samples/'


predictor = prediction_endpoint.PredictionEndpoint(prediction_key)

#with open("test.jpg", mode="rb") as test_data:
results = predictor.predict_image(project_id=project, image_data=base_image_url + "Images/Hemlock/hemlock_2.jpg", iteration_id=4)

for prediction in results.predictions:
    print ("\t" + prediction.tag_name + ": {0:.2f}%".format(prediction.probability * 100), prediction.bounding_box.left, prediction.bounding_box.top, prediction.bounding_box.width, prediction.bounding_box.height)