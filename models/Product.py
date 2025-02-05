class Product:
    # See below comments for each product types unique 3 attributes
    # All product objects are initialized with all product attributes to avoid later issues with inheritance
    # when creating products they only are given the attributes relevant and the rest are defaulted to None
    def __init__(self, productID, productName, price, type, gender, movable, isMirror, character, hasColour, dimensions, material, scale, isLimited, description, image_blob):
        self.productID = productID
        self.productName = productName
        self.price = price
        self.type = type
        self.gender = gender if gender is not None else None
        self.movable = movable if movable is not None else None
        self.isMirror = isMirror if isMirror is not None else None
        self.character = character if character is not None else None
        self.hasColour = hasColour if hasColour is not None else None
        self.dimensions = dimensions if dimensions is not None else None
        self.material = material if material is not None else None
        self.scale = scale if scale is not None else None
        self.isLimited = isLimited if isLimited is not None else None
        self.description = description
        self.image_blob = image_blob

# unique attributes for figurines; gender, moveable, isMirror

#  unique attributes for poster; character(s), hasColour,dimensions

#  unique attributes for replicas; material, scale , isLimited


