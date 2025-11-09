export class InspectMenu {
    static elements = [];

    constructor(x, y, header, body, content) {
        const main = document.createElement("div");
        main.style.width = "300px";

        main.classList.add("glass", "inspect");
        main.style.left = x+"px";
        main.style.top = y+"px";

        const heightPercent = y/window.innerHeight;
        main.style.transform = `translate(${ x<(window.innerWidth/2) ? "0%" : "-100%" }, ${ (-heightPercent)*100+"%"})`
        
        if (header !== undefined) {
            const headerDiv = document.createElement("div");
            headerDiv.textContent = header;
            headerDiv.style.fontSize = "large";
            headerDiv.style.textAlign = "center";
            main.appendChild(headerDiv);
        }

        if (body !== undefined) {
            const bodyDiv = document.createElement("div");
            bodyDiv.textContent = body;
            bodyDiv.style.fontSize = "small";
            main.appendChild(bodyDiv);
        }

        if (content !== undefined) {
            main.appendChild(content);
        }

        self.div = main;
        document.body.appendChild(main);
        InspectMenu.elements.push(main);

        requestAnimationFrame(() => {
            main.style.visibility = "visible";
            main.style.opacity = 1;
        });
    }

    remove() {
        const div = self.div;
        div.style.visibility = "hidden";
        div.style.opacity = 0;
        setTimeout(() => {
            div.remove();
        }, 1000);
    }

    static removeAll() {
        for (const div of InspectMenu.elements) {
            div.style.visibility = "hidden";
            div.style.opacity = 0;
        }
        const divsToRemove = [...InspectMenu.elements];
        InspectMenu.elements = [];

        setTimeout(() => {
            for (const div of divsToRemove) {
               div.remove()
            }
        }, 1000);
    }
}