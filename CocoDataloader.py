from pycocotools.coco import COCO
from tqdm import tqdm
import numpy as np
from torch.utils.data import Dataset

class CocoLoader(Dataset):

    # Fallback location of coco dataset directory.
    DEFAULT_DIR = '../DS_coco'

    # Fallback COCO datatype
    VAL_TYPE = 'val2017'

    TRAIN_TYPE = 'train2017'

    def __init__(self, dataDir=None, dataType=None):
        self.dataDir = dataDir if dataDir is not None else CocoLoader.DEFAULT_DIR
        self.dataType = dataType if dataType is not None else CocoLoader.VAL_TYPE
        self.rootPath = self.dataDir + self.dataType

        annFile = '{}/annotations/instances_{}.json'.format(self.dataDir, self.dataType)
        self.coco = COCO(annFile)
        self._getCategoryIds()
        self._buildCategoryIdNameMapping()
        self._getImageIds()
        self._buildImageDataMapping()
        self._buildCatToListIndexMap()
    
    def _getCategoryIds(self):
        '''Build internal list of category Ids.
        
        '''

        self.categoryIds = self.coco.getCatIds()
    
    def _buildCatToListIndexMap(self):
        '''Build a mapping between category ids and index for one hot encoding.
        
        Category Ids are not sequential. Hence we need to add a mapping from the category Ids to 
        indexes for a normal list. This will be very helpful during one hot encoding.
        Needs to be called after _getCategoryIds

        Creates a new var called catToIdxMap which maps category ids to indexes. 
        '''

        self.catToIdxMap = {}
        count = 0
        for i in self.categoryIds:
            self.catToIdxMap[i] = count
            count += 1
    
    def OHECategoryId(self, catId):
        '''One Hot Encode a given category ID
        
        Needs to be called after _buildCatToListIndexMap

        :param catId: Category Id
        :type catId: int
        '''

        oheCat = np.zeros((len(self.categoryIds), 1))
        idx = self.catToIdxMap[catId]
        oheCat[idx][0] = 1
        return oheCat
    
    def _buildCategoryIdNameMapping(self):
        '''Builds an internal mapping between category IDs and names.
        
        Needs to be called after _getCategoryIds        

        Creates self.catIdNameMap, a mapping between IDs to category names
        '''

        catMap = self.coco.loadCats(self.categoryIds)
        self.catIdNameMap = {}
        for cat in catMap:
            self.catIdNameMap[cat['id']] = cat['name']
    
    def _getImageIds(self):
        '''Get list of image Ids
        
        Creates self.imageIds which contains the list of images.
        '''

        self.imageIds = self.coco.getImgIds()
    
    def _buildImageDataMapping(self):
        ''' List of <image_id, data_about_image>
        
        Image_Id is mapped to filepath and annotations in the image. Annotations include category_id,
        bounding box and segmentations.

        Creates self.imageDataList which contains a list of dictionaries. Each dict contains mappings
        for images to their annotations.
        '''

        # A list with image data as a map for each element
        self.imageDataList = []

        for imageId in tqdm(self.imageIds):
            imgMap = {}

            # Read in image path
            imageData = self.coco.loadImgs(imageId)

            filePath = self.rootPath + '/' + imageData[0]['file_name']

            # There may be more than one annotation/object in the given image.
            annotationIds = self.coco.getAnnIds(imgIds = imageId)
            annotations = self.coco.loadAnns(annotationIds)

            imgMap['filePath'] = filePath
            imgMap['annotations'] = annotations
            self.imageDataList.append(imgMap)
    
    def __len__(self):
        '''Returns length of dataset
        
        :return: length of dataset
        :rtype: int
        '''
        return len(self.imageDataList)
    
    def __getitem__(self, idx):
        return 