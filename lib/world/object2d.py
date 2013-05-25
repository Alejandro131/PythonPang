class Object2D:
    
    def __init__(self, size, position):
        self.size = size
        self.position = position
        
    @property
    def x(self):
        return self.position.x
    
    @property
    def y(self):
        return self.position.y
    
    @property
    def width(self):
        return self.size.width
    
    @property
    def height(self):
        return self.size.height
