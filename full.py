import cv2
import re
import csv
from connect import get_detect


def get_full(path, radius, jpg_c, filename, d):
    full = cv2.imread(path + '/full_image.jpeg')
    if filename == path + '/full_image.jpeg':
        return True
    else:
        folder, img = filename.split('/')
        print(img)

        for i in range(0,d):
            number_1 = int(re.search(r'\d+', img).group())
            number_2 = int(re.search(r'\d+', img[2:]).group())
            print(number_1, number_2)
            if int(number_1) == i:
                coordinates = get_detect(path + '/' + img)
                size = coordinates[1]
                radius = 0.002
                ratio_1 = radius/max(size)
                ratio_2 = radius/max(size)
                for c in coordinates[0]:
                    for j in range(0, d):
                       if int(number_2) == j:
                            c_1 = c[0][0] + size[0] *j   #(j - 1)
                            c_0 = c[0][1] + size[1] *(d - i - 1) #(- i + 1)
                            probability = c[1]
                            print(probability)
                            myFile = open('output/output.csv', 'a')
                            with myFile:
                                myFields = ['coordinates', 'probability']
                                writer = csv.DictWriter(myFile, fieldnames=myFields)
                                writer.writerow({'coordinates': [float('{:.6f}'.format(jpg_c[2] - c_0 * ratio_1)),
                                                                 float('{:.6f}'.format(jpg_c[1] + c_1 * ratio_2))],
                                                 'probability': probability})
                cv2.imwrite(path + '/full_image.jpeg', full)



