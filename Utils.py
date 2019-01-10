from PIL import Image, ImageDraw
import math

def openImage(imgJson, rootPath):
    '''Opens PIL image given path.
    
    :param imgJson: JSON which contains image information
    :type imgJson: JSON
    :param rootPath: Path to image
    :type rootPath: String
    :return: Image read from path
    :rtype: PIL image
    '''

    path = rootPath + '/' + imgJson[0]['file_name']
    im = Image.open(path)
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
        bbox.append(annotations['bbox'])
    return bbox

def drawBoundingBox(img, annotations):
    '''Draw bounding boxes around objects in given image. Done in place.
    
    :param img: Image which contains objects
    :type img: PIL Image
    :param annotations: COCO Annotations which contain bounding box values
    :type annotations: JSON
    :return: Image with bounding boxes drawn on it.
    :rtype: PIL Image
    '''

    draw = ImageDraw.Draw(img)
    x1, y1, x2, y2 = 0, 0, 0, 0
    for annotation in annotations:
        bbox = annotation['bbox']
        x1 = int(bbox[0])
        y1 = int(bbox[1])
    
        x2 = int(bbox[2]) + x1
        y2 = int(bbox[3]) + y1
    
        draw.rectangle([(x1, y1), (x2, y2)])

    ## Good practice?
    del draw

    return img