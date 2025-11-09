export class Capy {
    static accessories = [
        "generic",
        "art",
        "computer",
        "cooking",
        "exercise",
        "food",
        "formal",
        "gaming",
        "party",
        "silly",
        "sleeping",
        "sports",
        "study",
    ];

    constructor(accessory) {
        this.div = document.createElement("div");
        this.accessory = accessory;

        const capyImg = document.createElement("img");
        capyImg.src = "../assets/capys/generic.png";
        capyImg.alt = `${accessory} capybara`;
        capyImg.style.position = "absolute";
        capyImg.style.transform = "translate(-100%, -100%)";
        this.div.appendChild(capyImg);

        if (accessory !== "generic") {
            const accessoryImg = document.createElement("img");
            accessoryImg.src = `../assets/accessories/${accessory}.png`;
            accessoryImg.style.position = "absolute";
            accessoryImg.style.transform = "translate(-100%, -100%)";
            this.div.appendChild(accessoryImg);
        }
    }
}