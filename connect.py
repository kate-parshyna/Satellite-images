import requests
import json
import cv2

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


headers = {
    'Prediction-Key': 'd068af02c24b42b498f049e8dcad6a7a',
    'Content-Type': 'application/octet-stream'
}

def get_detect(path):
    with open(path, 'rb') as file:
        body = file.read()

    r = requests.post(
        'https://southcentralus.api.cognitive.microsoft.com/customvision/v2.0/Prediction/f3c7ba04-ee4e-4b42-a4f4-fd116b1788c1/image',
        headers=headers, data=body)
    r = json.loads(r.text)
    #print(r)
    img = cv2.imread(path)
    height, width, channels = img.shape
    centres = []
    for i in r['predictions']:
        # print(i.get('boundingBox'))
        probability = i.get('probability')
        if probability > 0.1:
            point1_x = i.get('boundingBox')['left']
            point1_y = i.get('boundingBox')['top']
            point2_x = i.get('boundingBox')['left'] + i.get('boundingBox')['width']
            point2_y = i.get('boundingBox')['top'] + i.get('boundingBox')['height']

            point1_x = int(point1_x * width)
            point1_y = int(point1_y * height)
            point2_x = int(point2_x * width)
            point2_y = int(point2_y * height)
            center = [point1_x + (point2_x - point1_x) / 2,
                      point1_y - (point1_y - point2_y) / 2]
            cv2.circle(img, (int(center[0]), int(center[1])), 10, (0, 0, 255), 0)
            center = [int(center[0]), int(center[1])]
            centres.append([center, probability])
        cv2.imwrite(path, img)
    return centres, [width, height]








