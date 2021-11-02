var selBrand = "all";
var withoutMatch = true;

// TODO: Find a better way to manage this
const champions = [
    "Roman Reigns",
    "Jimmy Uso",
    "Jey Uso",
    "Shinsuke Nakamura",
    "Charlotte Flair",
    "Xavier Woods",
    "Big E",
    "Damian Priest",
    "Randy Orton",
    "Riddle",
    "Zelina Vega",
    "Becky Lynch",
];

const champs = new Set();
champions.forEach(element => {
    champs.add(element);
});

let lastUpdatedElm = document.getElementById("lastUpdated");
lastUpdatedElm.textContent = data.last_episode;

let withoutMatchElm = document.getElementById("withoutMatch");
withoutMatchElm.onchange = (ev) => {
    withoutMatch = withoutMatchElm.checked;
    filterBy();
};

function filterBy() {
    if (selBrand != "RAW" && selBrand != "Smackdown") {
        renderData(data.ratings.filter(({total}) => (total > 0) || withoutMatch));
        return;
    }
    renderData(data.ratings.filter(({brand, total}) => (brand == selBrand) && (total > 0 || withoutMatch)));
}

function zall() {
    selBrand = "all";
    filterBy();
}

function raw() {
    selBrand = "RAW";
    filterBy();
}

function smackdown() {
    selBrand = "Smackdown";
    filterBy();
}

function renderData(ratings) {
    let tbodyElm = document.getElementById("ranks-body");
    var rank = 0;
    var buffer = 0;
    var prevValue = 0;

    const crown = ` <i class="fa fa-crown yellow-text text-darken-3"></i>`;
    let trs = ratings.map(({name, rating, brand, win, loss, total}, idx) => {
        if (rating != prevValue) {
            rank = rank + buffer + 1;
            buffer = 0;
            prevValue = rating;
        } else {
            buffer++;
        }

        if (champs.has(name)) {
            name += crown;
        }
        return `<tr>
            <td>${rank}</td>
            <td>${name}</td>
            <td>${rating}</td>
            <td><span class="white-text badge ${brand == "RAW" ? "red" : "blue"} darken-3" data-badge-caption="${brand}"></span></td>
            <td>${win}</td>
            <td>${loss}</td>
            <td>${total}</td>
        </tr>`;
    });
    tbodyElm.innerHTML = trs.join(" ");
}

filterBy();