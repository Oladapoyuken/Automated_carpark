import numpy as np
import tensorflow as tf
import cv2

from utils import label_map_util
from utils import visualization_utils as vis_util

# Define the video stream
img = cv2.imread('park_images\\park12.jpg')
# cv2.imwrite(filename='newImage.jpg', img=img)
# img = cv2.imread('C:\\Users\\Yuken4real\\PycharmProjects\\Automated_carpark\\newImage.jpg')


coordinates = []
list_id = []
list_position = []


# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = 'tensor_files\\frozen_inference_graph_raspNew.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = 'tensor_files\\label_map_new.pbtxt'

# Number of classes to detect
NUM_CLASSES = 7

empty = ''


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
        result = [category_index.get(value) for index, value in enumerate(classes[0]) if scores[0, index] > 0.5]
        # print(result)
        # Visualization of the results of a detection.
        vis_util.visualize_boxes_and_labels_on_image_array(
            img,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=5
        )
        # coordinates = vis_util.return_coordinates(
        #     img,
        #     np.squeeze(boxes),
        #     np.squeeze(classes).astype(np.int32),
        #     np.squeeze(scores),
        #     category_index,
        #     use_normalized_coordinates=True,
        #     line_thickness=5,
        #     min_score_thresh=0.9)

        # print('LIST OF EMPTY CAR PARKING SPACE : {}'.format(empty))
        empty = ''
        for val in result:
            if empty.__contains__(str(val['id'])):
                print()
            else:
                empty += str((val['id']))
                empty += ' '
        print('LIST OF EMPTY CAR PARKING SPACE : {}'.format(empty))

        # for val in coordinates:
        #     list_position.append(val[2])
        #
        # list = sortChars(list_id, list_position)
        # print(list)


        # print('LIST OF EMPTY CAR PARKING SPACE :')
        # print(list_id)
        # print('coordinates : ')
        # print(list_position)





        # Display output
        cv2.imshow('object detection', cv2.resize(img, (800, 600)))

cv2.waitKey(0)
cv2.destroyAllWindows()
