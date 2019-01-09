from PIL import Image, ImageDraw

def OpenImage(imgJson, rootPath):
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

def getCategoryName(catId, categoryJson):
    '''Returns the name of the category, given the category ID
    
    :param catId: Category ID
    :type catId: int
    :param categoryJson: JSON containing all categories
    :type categoryJson: JSON
    :return: name of Category
    :rtype: String
    '''

    for cat in categoryJson:
        if cat['id'] == catId:
            return cat['name']

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