import numpy as np


class Point:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y


class Mark(Point):
    def __init__(self, landmark, image):
        super().__init__(int(landmark.x * image.shape[1]),
                         int(landmark.y * image.shape[0]))


class Oval:
    def __init__(self, landmarks, image):
        self.indecies = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]
        self.points = [Mark(landmarks[i], image) for i in self.indecies]
        self.np_points = np.array([[p.x,p.y] for p in self.points], np.int32)


class Tesselation:
    def __init__(self, landmarks, image):
        self.indecies = [
                [54, 103, 67, 109, 10, 338, 297, 332, 284],
                [21, 68, 104, 69, 108, 151, 337, 299, 333, 298, 251],
                [162, 71, 63, 105, 66, 107, 9, 336, 296, 334, 293, 301, 389],
                [127, 139, 70, 53, 52, 56, 55, 8, 285, 295, 282, 283, 300, 368, 356],
                [34, 156, 56, 224, 223, 222, 221, 441, 442, 443, 444, 276, 383, 264]]
        self.points = []
        self.np_points = []
        for rows in self.indecies:
            row = [Mark(landmarks[i], image) for i in rows]
            self.points.append(row)
            self.np_points.append([np.array([[p.x,p.y] for p in row], np.int32)])
            

class Eye:
    def __init__(self, eye, landmarks, image):
        c = [386,374] if type(eye) == LeftEye else [158,145]
        c1 = Mark(landmarks[c[0]], image)
        c2 = Mark(landmarks[c[1]], image)
        self.center = Point(c1.x+(c2.x-c1.x)//2, c1.y+(c2.y-c1.y)//2)
        self.points = [Mark(landmarks[i], image) for i in eye.indecies]
        self.np_points = np.array([[p.x,p.y] for p in self.points], np.int32)
        

class LeftEye(Eye):
    def __init__(self, landmarks, image):
        self.indecies = [263, 466, 388, 387, 386, 385, 384, 398, 362, 382, 381, 380, 374, 373, 390, 249]
        super().__init__(self, landmarks, image)
        
class RightEye(Eye):
    def __init__(self, landmarks, image):
        self.indecies = [33, 246, 161, 160, 159, 158, 157, 173, 133, 155, 154, 153, 145, 144, 163, 7]
        super().__init__(self, landmarks, image)


class Nose:
    def __init__(self, landmarks, image):
        self.indecies = [168,4,48,2,278]
        self.points = [Mark(landmarks[i], image) for i in self.indecies]
        self.np_points = np.array([[p.x,p.y] for p in self.points], np.int32)

