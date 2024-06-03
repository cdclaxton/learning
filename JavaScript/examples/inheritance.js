// Constructor function
class Shape {
    constructor(h, w) {
        this.h = h;
        this.w = w;
    }
    area() {
        return this.h * this.w;
    }
}

// Class that inherit from the 'Shape' class
class ColouredShape extends Shape {
    constructor(h, w, colour) {
        super(h, w);
        this.colour = colour;
    }
    show() {
        return this.colour + " shape with bounding box area " + this.area();
    }
}
    
let shape1 = new ColouredShape(2, 3, "blue");
console.log(`Height: ${shape1.h}, Width: ${shape1.w}`);
console.log(shape1.show());