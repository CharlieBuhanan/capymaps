export class Capy {
    constructor(accessory) {
        this.div = document.createElement("div");
        this.div.style.scale = 0.6;

        const capyImg = document.createElement("img");
        capyImg.src = "../assets/capys/generic.png";
        capyImg.alt = `${accessory} capybara`;
        capyImg.style.position = "absolute";
        capyImg.style.transform = "translate(-100%, -100%)";
        this.div.appendChild(capyImg);

        if (accessory !== undefined) {
            const accessoryImg = document.createElement("img");
            accessoryImg.src = `../assets/accessories/${accessory}.png`;
            accessoryImg.style.position = "absolute";
            accessoryImg.style.transform = "translate(-100%, -100%)";
            this.div.appendChild(accessoryImg);
        }
    }
}