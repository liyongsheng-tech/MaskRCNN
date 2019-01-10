from PIL import Image, ImageDraw
import math

def openImage(imgPath):
    '''Opens PIL image given path.
    
    :param imgPath:  Path to image
    :type imgPath: String
    :return: Image read from path
    :rtype: PIL image
    '''

    im = Image.open(imgPath)
    return im

def calcBoundingBoxParams(bbox, anchorBBox):
    '''Calculate the regressor parameters, given a bounding box
    
    The 4 params, tx, ty, tw and th are not the same as the bbox.
    The params are as given in the Faster RCNN paper. 
    
    :param bbox: bbox values, (x, y, w, h)
    :type bbox: Tuple of floats
    :param anchorBBox: Anchor bbox values (xa, ya, wa, ha)
    :type anchorBBox: Tuple of floats
    :return: set of 4 parameters
    :rtype: 4 tuple of floats
    '''
    x, y, w, h = bbox
    xa, ya, wa, ha = anchorBBox

    tx = (x - xa) / float(wa)
    ty = (y - ya) / float(ha)
    tw = math.log(float(w / wa))
    th = math.log(float(h / ha))

    return (tx, ty, tw, th)


def getBoundingBoxes(annotations):
    '''Parse bounding boxes from given annotations
    
    :param annotations: annotations containing bounding boxes
    :type annotations: dict
    :return: bounding box coords
    :rtype: list
    '''

    bbox = []
    for annotation in annotations:
        bbox.append(annotation['bbox'])
    return bbox

def drawBoundingBox(img, bboxList):
    '''Draw bounding boxes around objects in given image. Done in place.
    
    :param img: Image which contains objects
    :type img: PIL Image
    :param bboxList: list of bounding boxes
    :type bboxList: list of 4 tuples
    :return: Image with bounding boxes drawn on it.
    :rtype: PIL Image
    '''

    draw = ImageDraw.Draw(img)
    x1, y1, x2, y2 = 0, 0, 0, 0
    for bbox in bboxList:
        x1 = int(bbox[0])
        y1 = int(bbox[1])
    
        x2 = int(bbox[2]) + x1
        y2 = int(bbox[3]) + y1
    
        draw.rectangle([(x1, y1), (x2, y2)])

    ## Good practice?
    del draw

    return img