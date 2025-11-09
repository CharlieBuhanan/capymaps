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
    
    async placeCapy(mapX, mapY, relX, relY) {
        console.log("Placing capy at:", mapX, mapY);
        try {
            // Default activity (no UI yet)
            const markerData = {
                x_coord: mapX,
                y_coord: mapY,
                activity: "generic" // must match your ActivityEnum value (adjust if needed)
            };

            const response = await fetch("http://localhost:8000/markers", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(markerData)
            });

            if (!response.ok) {
                throw new Error(`Backend error: ${response.status}`);
            }

            const newMarker = await response.json();

            // Create a visual capybara marker
            new MapCapy(this, newMarker.x_coord, newMarker.y_coord, newMarker.activity, newMarker.id);
            console.log("Capybara placed successfully!");

        } catch (err) {
            console.error("Failed to place capybara:", err);
            alert("Could not place capybara. Check console for details.");
        } finally {
            this.togglePlacingCapy(false);
        }
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
    static globalClickHandler = null; // shared handler function

    constructor(map, x, y, accessory, id) {
        const capy = new Capy(accessory);
        super(map, x, y, `${accessory}-capy`, capy.div);
        this.id = id;
        this.div.style.zIndex = 10001;
        this.div.classList.add("interactive");
        MapCapy.ids.set(id, this);

        // Attach the shared handler if it exists
        this.div.addEventListener("click", (event) => {
            event.stopPropagation();
            if (MapCapy.globalClickHandler) {
                MapCapy.globalClickHandler(this, event);
            }
        });
    }
    static setGlobalClickHandler(handler) {
        MapCapy.globalClickHandler = handler;
    }
}
MapCapy.setGlobalClickHandler(async (capy, event) => {
    console.log("Capy clicked: {capy.id}");
    InspectMenu.removeAll();
    const randomNumber = Math.floor(Math.random() * 10);
    const capyQuotes = [
        "Capy diem. Seize the lettuce!",
        "Keep calm and capy on.",
        "Don't worry, be capy.",
        "This capy is locked in a staring contest with you.",
        "Why did the capybara cross the road? To prove it wasn't chicken!",
        "Feeling a bit capy-tivated by you.",
        "This capybara is asleep. Zzz...",
        "Yo.",
        "This capybara is to shy to talk.",
        "Just a capybara living its best life."
    ];
    let id = "";
    if (capy.id===undefined) {
        id = "Random Capybara";
    } else {
        id = "Capybara Number " + (capy.id).toString();
    }
    const accessory = capy.accessory===undefined? "Nothing":capy.accessory;
    const quote = capyQuotes[randomNumber];

    InspectMenu.removeAll();
    new InspectMenu(
        event.clientX,
        event.clientY,
        `${id}`,
        `This Capybara is busy with: ${accessory}. \n\n ${quote}`,
        undefined
    );
});


class MapAlert extends MapElement {
    static ids = new Map();
    static globalClickHandler = null;

    constructor(map, x, y, name, id) {
        const img = document.createElement("img");
        img.src = `../assets/misc/alert.png`;
        img.alt = name;

        super(map, x, y, `${name}-alert`, img);
        this.id = id;
        this.name = name;
        this.type = "alert";

        this.div.classList.add("interactive");
        MapAlert.ids.set(id, this);
        const self = this;
        this.div.addEventListener("click", (event) => {
            event.stopPropagation();
            if (MapAlert.globalClickHandler) {
                MapAlert.globalClickHandler(self, event);
            }
        });
    }

    static setGlobalClickHandler(handler) {
        MapAlert.globalClickHandler = handler;
    }
}
MapAlert.setGlobalClickHandler(async (alert, event) => {
    console.log(`Clicked alert #${alert.id} (${alert.name})`);
    console.log("Loading events from backend...");
    let dbEvent = null;
    try {
        const response = await fetch("http://localhost:8000/events", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });
        if (!response.ok) {
            throw new Error(`Backend error: ${response.status}`);
        }
        const events = await response.json();
        console.log(`Fetched ${events.length} events from backend.`);
        // Loop through and place each event marker on the map
        dbEvent = events.find(ev => ev.id === alert.id);
        if (!dbEvent) {
            throw new Error(`Event with ID ${alert.id} not found.`);
        }
    } catch (err) {
        console.error("Failed to load events:", err);
        alert("Could not load events. Check console for details.");
    }
    const content = document.createElement("div");
    const jsDate = new Date(dbEvent.time);
    content.innerHTML = `
        <p><strong>Host:</strong> ${dbEvent.host}</p>
        <p><strong>Time:</strong> (${jsDate.toLocaleString()})</p>
    `;
    // USE THIS
    InspectMenu.removeAll();
    new InspectMenu(
        event.clientX,
        event.clientY,
        dbEvent.title,
        dbEvent.description,
        content
    );
});

async function loadCapybaras(map) {
    try {
        const response = await fetch("http://localhost:8000/markers");
        if (!response.ok) {
            throw new Error(`Failed to fetch markers: ${response.status}`);
        }

        const markers = await response.json();

        markers.forEach(m => {
            new MapCapy(map, m.x_coord, m.y_coord, m.activity, m.id);
        });

        console.log(`Loaded ${markers.length} capybaras from backend.`);
    } catch (err) {
        console.error("Error loading capybaras:", err);
    }
}

const interactiveMap = new InteractiveMap(3000, 3000);
await loadCapybaras(interactiveMap);

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

async function loadEvents(n) {
    console.log("Loading events from backend...");
    try {

        const response = await fetch("http://localhost:8000/events", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (!response.ok) {
            throw new Error(`Backend error: ${response.status}`);
        }

        const events = await response.json();
        console.log(`Fetched ${events.length} events from backend.`);

        // Loop through and place each event marker on the map
        for (let i = 0; i < n; i++) {
            if (i >= events.length) break;
            const ev = events[i];
            // Assuming you have a class like MapEvent similar to MapCapy
            const alert = new MapAlert(
                interactiveMap,
                ev.x_coord + Math.floor(Math.random() * 150) + 50,
                ev.y_coord + Math.floor(Math.random() * 150) - 50,
                ev.title,
                ev.id
            );
            alert.zIndex = 100002;
        }
        console.log("All event markers placed!");

    } catch (err) {
        console.error("Failed to load events:", err);
        alert("Could not load events. Check console for details.");
    }
}
await loadEvents(43);
