import numpy as np
import tensorflow as tf
import cv2
import time

from utils import label_map_util
from utils import visualization_utils as vis_util

def rotateImg(image, angle, center=None, scale=1.0):
    (h, w) = image.shape[:2]
    if center is None:
        center = (w//2, h//2)
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated




# Define the video stream
vid = cv2.VideoCapture('videos\\vid6.mp4')


# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = 'tensor_files\\upgrade_frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = 'tensor_files\\slots_label_map.pbtxt'

# Number of classes to detect
NUM_CLASSES = 7

#String of empty parking slots
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



# Helper code
def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)


# Detection
with detection_graph.as_default():
    with tf.Session(graph=detection_graph) as sess:

        while vid.isOpened():
            ret, img = vid.read()
            if ret == False:
                vid.release()
            img = rotateImg(img, 90)
            img = cv2.resize(img, (1080, 700), interpolation=cv2.INTER_AREA)
            # img = cv2.flip(img, -2)
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

            print('LIST OF EMPTY CAR PARKING SPACE : {}'.format(empty))
            empty = ''
            for val in result:
                if empty.__contains__(str(val['id'])):
                    print()
                else:
                    empty += str((val['id']))
                    empty += ' '

            # Display output
            cv2.imshow('object detection', img)
            if cv2.waitKey(1)==ord('q'):
                break



vid.release()
cv2.destroyAllWindows()
