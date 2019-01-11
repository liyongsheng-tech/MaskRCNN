import torch
import torch.nn
import torch.nn.Functional as F

from torchvision import models

class MaskModel(torch.nn.Module):

    OBJECTNESS_THRESHOLD = 0.7

    def __init__(self, model, classifier):
        self.model = model
        self.classifier = classifier

        self.catClassifier
        self.regressor

    def forward(self, x):
        features = self.model(x)

        # TODO
        # Add ROI Features. Anchoring is also needed here.

        RoIs = self.getRoI(x, features)
        for RoI in RoIs:
            objectnessScore = self.classifier(RoI)
            if objectnessScore > MaskModel.OBJECTNESS_THRESHOLD:

