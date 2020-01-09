import numpy as np
import tensorflow as tf
import cv2

from utils import label_map_util
from utils import visualization_utils as vis_util

# Define the video stream
img = cv2.imread('C:\\Users\\Yuken4real\\PycharmProjects\\Automated_carpark\\images\\test3.jpg')

plate_number = ''
plate_number_sorted = ''
coordinates = []
list_id = []
list_position = []
char_singles = [' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', '1', 'J', 'K', 'L', 'M', 'N', '0', 'P', 'Q', 'R', 'S', 'T',
                'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']


# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = 'C:\\Users\\Yuken4real\\PycharmProjects\\Automated_carpark\\tensor_files\\frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = 'C:\\Users\\Yuken4real\\PycharmProjects\\Automated_carpark\\tensor_files\\char_label_map.pbtxt'

# Number of classes to detect
NUM_CLASSES = 36


# Load a (frozen) Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')


# Loading label map
# Label maps map indices to category names, so that when our convolution network predicts `5`,
# we know that this corresponds to `airplane`. Here we use internal utility functions,
# but anything that returns a dictionary mapping integers to appropriate string labels would be fine

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(
    label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


#Rearrange accordingly

def sortChars(list1, list2):
    list_temp = []
    list = []
    dico_temp = {}
    if len(list1) == len(list2):
        siz = len(list1)
        for k in range(siz):
            dico_temp[list2[k]] = list1[k]

        for k in sorted(dico_temp):
            list_temp.append(k)

        for k in range(siz):
            list.append(dico_temp[list_temp[k]])
    else:
        print(len(list1))
        print(len(list2))
        print('\n')
        print('An error occured!')

    return list





# Helper code
def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)


# Detection
with detection_graph.as_default():
    with tf.Session(graph=detection_graph) as sess:
        # Read image from from doc and Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(img, axis=0)
        # Extract image tensor
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        # Extract detection boxes
        boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        # Extract detection scores
        scores = detection_graph.get_tensor_by_name('detection_scores:0')
        # Extract detection classes
        classes = detection_graph.get_tensor_by_name('detection_classes:0')
        # Extract number of detectionsd
        num_detections = detection_graph.get_tensor_by_name(
            'num_detections:0')
        # Actual detection.
        (boxes, scores, classes, num_detections) = sess.run(
            [boxes, scores, classes, num_detections],
            feed_dict={image_tensor: image_np_expanded})


        result = [category_index.get(value) for index, value in enumerate(classes[0]) if scores[0, index] > 0.8]

        # myboxes = np.squeeze(boxes)
        # myscores = np.squeeze(scores)
        # ms = 0.8
        # bboxes = myboxes[myscores > ms]
        # img_w, img_h = img.size
        # final_box = []
        # for box in bboxes:
        #     ymin, xmin, ymax, xmax = box
        #     final_box.append([xmin*img_w, xmax*img_h, ymin*img_h, ymax*img_h])
        #
        # print(final_box)

        # print(result)
        # Visualization of the results of a detection.
        vis_util.visualize_boxes_and_labels_on_image_array(
            img,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=2
        )
        coordinates = vis_util.return_coordinates(
            img,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=2,
            min_score_thresh=0.80)



        for val in result:
            plate_number += str(char_singles[int(val['id'])])
            list_id.append(val['id'])
        print(plate_number)

        for val in coordinates:
            # list_position.append(val[2])
            print(val)

        list = sortChars(list_id, list_position)

        for x in list:
            plate_number_sorted += str(char_singles[x])
        print(plate_number_sorted)





        # Display output
        cv2.imshow('object detection', cv2.resize(img, (800, 600)))

cv2.waitKey(0)
cv2.destroyAllWindows()
