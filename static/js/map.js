import { Capy } from "../js/capy.js";
import { buildingData } from "../js/building.js";
import { InspectMenu } from "./inspect.js";

const viewport = document.getElementById('map-viewport');
const container = document.getElementById('map-container');
const placingCapyPopup = document.getElementById("placing-capy");

class InteractiveMap {
    constructor(width, height) {
        // Element References
        this.viewport = viewport;
        this.container = container;

        // Map Dimensions
        this.width = width;
        this.height = height;
        this.bound = 0; // Boundary for clamping

        // State Variables (now instance properties)
        this.scale = 1.0;
        this.panX = 0;
        this.panY = 0;
        this.isDragging = false;
        this.startX = 0;
        this.startY = 0;
        this.lastTouchDist = -1;
        this.placingCapy = false;

        // Set initial container size
        this.container.style.width = this.width + "px";
        this.container.style.height = this.height + "px";
        
        // Add Event Listeners, binding 'this' automatically using arrow functions
        this.viewport.addEventListener('mousedown', this.handleMouseDown);
        window.addEventListener('mousemove', this.handleMouseMove);
        window.addEventListener('mouseup', this.handleMouseUp);
        this.viewport.addEventListener('wheel', this.handleWheel, { passive: false });
        
        this.viewport.addEventListener('touchstart', this.handleTouchStart, { passive: false });
        this.viewport.addEventListener('touchmove', this.handleTouchMove, { passive: false });
        window.addEventListener('touchend', this.handleTouchEnd);

        document.getElementById("recenter-button").addEventListener("click", this.resetView);
        document.getElementById("zoomin-button").addEventListener("click", () => this.zoomCenter(1.1));
        document.getElementById("zoomout-button").addEventListener("click", () => this.zoomCenter(0.9));
        document.getElementById("create-button").addEventListener("click", () => this.togglePlacingCapy(!this.placingCapy));

        // Initial view setup
        this.resetView();
    }

    // --- Core Map Logic Methods ---

    updateTransform() {
        // container.style.transform = `translate(${panX}px, ${panY}px) scale(${scale})`; 
        // Use clientWidth/Height for accurate viewport size
        this.panX = Math.max(-(this.width+this.bound)*this.scale+window.innerWidth, Math.min(this.bound*this.scale, this.panX));
        this.panY = Math.max(-(this.height+this.bound)*this.scale+window.innerHeight, Math.min(this.bound*this.scale, this.panY));
        this.scale = Math.max(0.5, Math.min(3.0, this.scale));
        this.container.style.transform = `translate(${this.panX}px, ${this.panY}px) scale(${this.scale})`;
        InspectMenu.removeAll();
    }

    resetView = () => {
        this.scale = 1.0;
        // Center the map on the viewport area
        this.panX = -(this.width - window.innerWidth) / 2;
        this.panY = -(this.height - window.innerHeight) / 2;
        this.updateTransform();
    }

    zoomCenter(zoomAmount) {
        const newScale = Math.max(0.5, Math.min(3.0, this.scale * zoomAmount));

        const viewportWidth = window.innerWidth;
        const viewportHeight = window.innerHeight;

        // The coordinates (X, Y) of the center of the viewport
        const viewportCenterX = viewportWidth / 2;
        const viewportCenterY = viewportHeight / 2;

        // Calculate the corresponding point in the map's coordinate system
        const mapCenterX = (viewportCenterX - this.panX) / this.scale;
        const mapCenterY = (viewportCenterY - this.panY) / this.scale;

        // Calculate the new pan needed to keep the map center point under the viewport center
        this.panX = viewportCenterX - mapCenterX * newScale;
        this.panY = viewportCenterY - mapCenterY * newScale;
        
        // Apply new scale
        this.scale = newScale;
        this.updateTransform();
    }

    togglePlacingCapy(enable) {
        this.viewport.style.cursor = enable ? "pointer" : "";
        placingCapyPopup.style.opacity = enable ? 1 : 0;
        placingCapyPopup.style.visibility = enable ? "visible" : "hidden";
        this.placingCapy = enable;
        document.getElementById("create-plus-icon").style.visibility = enable ? "hidden" : "visible";
        document.getElementById("create-exit-icon").style.visibility = enable ? "visible" : "hidden";
        document.getElementById("create-button").title = enable ? "Stop placing a capybara" : "Place a capybara!";
    }
    
    placeCapy(mapX, mapY, relX, relY) {
        const accessoriesDiv = document.createElement("div");
        new InspectMenu(relX, relY, "New capybara!", "What is your capybara doing right now?");
        this.togglePlacingCapy(false);
    }

    // --- Mouse Event Handlers (Bound using arrow functions) ---

    handleMouseDown = (e) => {
        e.preventDefault();
        if (this.placingCapy) {
            const x = -((this.panX-e.clientX)/this.scale);
            const y = -((this.panY-e.clientY)/this.scale);
            this.placeCapy(x, y, e.clientX, e.clientY);
        } else {
            this.isDragging = true;
            this.viewport.style.cursor = 'grabbing';
            this.startX = e.clientX;
            this.startY = e.clientY;
        }
    }

    handleMouseMove = (e) => {
        if (!this.isDragging) return;
        e.preventDefault();
        
        const dx = e.clientX - this.startX;
        const dy = e.clientY - this.startY;
        
        this.panX += dx;
        this.panY += dy;
        
        this.startX = e.clientX;
        this.startY = e.clientY;
        
        this.updateTransform();
    }

    handleMouseUp = () => {
        this.isDragging = false;
        this.viewport.style.cursor = 'grab';
    }

    handleWheel = (e) => {
        e.preventDefault();
        
        const zoomAmount = e.deltaY < 0 ? 1.1 : 1 / 1.1;
        const newScale = Math.max(0.5, Math.min(3.0, this.scale * zoomAmount));
        
        const rect = this.viewport.getBoundingClientRect();
        const cursorX = e.clientX - rect.left;
        const cursorY = e.clientY - rect.top;
        
        const mapCursorX = (cursorX - this.panX) / this.scale;
        const mapCursorY = (cursorY - this.panY) / this.scale;
        
        this.panX = cursorX - mapCursorX * newScale;
        this.panY = cursorY - mapCursorY * newScale;
        
        this.scale = newScale;
        this.updateTransform();
    }

    // --- Touch Event Handlers (Bound using arrow functions) ---

    getDistance(touches) {
        if (touches.length < 2) return -1;
        const dx = touches[0].clientX - touches[1].clientX;
        const dy = touches[0].clientY - touches[1].clientY;
        return Math.sqrt(dx * dx + dy * dy);
    }

    handleTouchStart = (e) => {
        if (e.touches.length === 1) {
            this.handleMouseDown({ 
                clientX: e.touches[0].clientX, 
                clientY: e.touches[0].clientY,
                preventDefault: () => e.preventDefault()
            });
        } else if (e.touches.length === 2) {
            this.isDragging = false;
            this.lastTouchDist = this.getDistance(e.touches);
        }
    }

    handleTouchMove = (e) => {
        e.preventDefault();
        
        if (e.touches.length === 1 && this.isDragging) {
            this.handleMouseMove({ 
                clientX: e.touches[0].clientX, 
                clientY: e.touches[0].clientY,
                preventDefault: () => e.preventDefault()
            });
        } else if (e.touches.length === 2 && this.lastTouchDist !== -1) {
            const newDist = this.getDistance(e.touches);
            const pinchRatio = newDist / this.lastTouchDist;
            
            const newScale = Math.max(0.2, Math.min(5.0, this.scale * pinchRatio)); 

            const rect = this.viewport.getBoundingClientRect();
            const centerX = (e.touches[0].clientX + e.touches[1].clientX) / 2;
            const centerY = (e.touches[0].clientY + e.touches[1].clientY) / 2;
            
            const cursorX = centerX - rect.left;
            const cursorY = centerY - rect.top;

            const mapCursorX = (cursorX - this.panX) / this.scale;
            const mapCursorY = (cursorY - this.panY) / this.scale;

            this.panX = cursorX - mapCursorX * newScale;
            this.panY = cursorY - mapCursorY * newScale;
            
            this.scale = newScale;
            this.lastTouchDist = newDist;
            this.updateTransform();
        }
    }

    handleTouchEnd = () => {
        this.isDragging = false;
        this.lastTouchDist = -1;
        this.viewport.style.cursor = 'grab';
    }
}

class MapElement {
    constructor(map, x, y, name, child) {
        console.log(x, y, name);
        this.x = x;
        this.y = y;
        this.name = name;
        this.div = document.createElement("div");
        this.div.classList.add("map-element");
        this.div.style.left = x+"px";
        this.div.style.top = y+"px";
        this.div.appendChild(child);
        this.div.style.zIndex = y+1000;
        map.container.appendChild(this.div);
    }
}

class MapBuilding extends MapElement {
    constructor(map, x, y, name) {
        const img = document.createElement("img");
        img.src = `../assets/buildings/${name}.png`;
        img.alt = name;
        super(map, x, y, name, img);
        this.div.classList.add("interactive");
    }
}

class MapDecor extends MapElement {
    static decorations = [
        // "bush1",
        // "bush2",
        // "flower1",
        // "flower2",
        // "grass1",
        // "grass2",
        // "grass3",
        // "rock1",
        "squirrel",
        "squiggle1",
        "squiggle2",
        "squiggle3",
        "squiggle4",
        "squiggle5",
        "squiggle6",
        "squiggle7",
        "squiggle8",
        "squiggle9",
        "squiggle10",
        "squiggle11",
        "squiggle12",
        "squiggle13",
        "squiggle14",
        "squiggle15",
        "squiggle16",
        "squiggle17"
    ];

    constructor(map, x, y) {
        const decoration = MapDecor.decorations[Math.floor(Math.random()*MapDecor.decorations.length)];

        const img = document.createElement("img");
        img.src = `../assets/misc/map-decoration/${decoration}.png`
        img.alt = decoration;
        if (Math.random() > 0.5) {
            img.style.transform = "scaleX(-1)";
        }

        if (decoration.match(/squiggle/i) && Math.random() > 0.5) {
            img.style.transform += "scaleY(-1)";
        }
        
        super(map, x, y, decoration, img);
    }
}

class MapCapy extends MapElement {
    static ids = new Map();
    constructor(map, x, y, accessory, id) {
        const capy = new Capy(accessory);
        super(map, x, y, `${accessory}-capy`, capy.div);
        this.div.classList.add("interactive");
        MapCapy.ids.set(id, this);
    }
}

class MapAlert extends MapElement {
    static ids = new Map();
    constructor(map, x, y, name, id) {
        const img = document.createElement("img");
        img.src = `../assets/misc/alert.png`;
        img.alt = name;
        super(map, x, y, `${name}-alert`, img);
        this.div.classList.add("interactive");
        MapAlert.ids.set(id, this);
        console.log(MapAlert.ids);
    }
}

const interactiveMap = new InteractiveMap(3000, 3000);

for (let i = 0; i < interactiveMap.width; i += 100) {
    for (let j = 0; j < interactiveMap.height; j += 100) {
        if (Math.random() > 0.3) {
            new MapDecor(interactiveMap, i + Math.random()*100, j + Math.random()*100);
        }
    }
}

buildingData.forEach(building => {
    new MapBuilding(interactiveMap, building.lat, building.long, building.name);
});
