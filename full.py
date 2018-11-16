import cv2
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
            if img[0] == '{}'.format(i):
                coordinates = get_detect(path + '/' + img)
                size = coordinates[1]
                radius = 0.002
                ratio_1 = radius/max(size)
                ratio_2 = radius/max(size)
                print(jpg_c)
                for c in coordinates[0]:
                    for j in range(0, d):
                        if img[2] == '{}'.format(j):
                            c_1 = c[0][0] + size[0] *j   #(j - 1)
                            c_0 = c[0][1] + size[1] *(d - i - 1) #(- i + 1)
                            # print(jpg_c[2] - c_1 * ratio_1, jpg_c[1] + c_0 * ratio_2)
                            probability = c[1]
                            #
                            myFile = open('output/output.csv', 'a')
                            # with open('output/output.csv', 'a') as file:
                            #     wr = csv.writer(file)
                            #     wr.writerow([float('{:.6f}'.format(jpg_c[2] - c_1 * ratio_1)),
                            #                  float('{:.6f}'.format(jpg_c[1] + c_0 * ratio_2))])
                            with myFile:
                                myFields = ['coordinates', 'probability']
                                writer = csv.DictWriter(myFile, fieldnames=myFields)
                                writer.writerow({'coordinates': [float('{:.6f}'.format(jpg_c[2] - c_0 * ratio_1)),
                                                                 float('{:.6f}'.format(jpg_c[1] + c_1 * ratio_2))],
                                                 'probability': probability})
                cv2.imwrite(path + '/full_image.jpeg', full)



