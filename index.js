var selBrand = "all";
var withoutMatch = true;

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
    let trs = ratings.map(({name, rating, brand, win, loss, total}, idx) => {
        if (rating != prevValue) {
            rank = rank + buffer + 1;
            buffer = 0;
            prevValue = rating;
        } else {
            buffer++;
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