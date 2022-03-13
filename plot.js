import "https://cdn.plot.ly/plotly-2.3.0.min.js";
const config = { responsive: true }

const layout = {
    xaxis: { title: "Date" },
    yaxis: {
        title: "Price",
        showspikes: true,
        rangemode: "tozero"
    },
    hoverlabel: {
        bgcolor: "black",
        bordercolor: "white",
        font: { size: 18 }
    },
    plot_bgcolor: "rgba(0,0,0,255)",
    paper_bgcolor: "rgba(0,0,0,255)",
    font: {
        size: 18,
        color: "white"
    },
    height: window.innerHeight - 100
};
const card_map = new Map();

const response = await fetch("./output.csv");

if (response.ok) {
    const text = await response.text();
    const lines = text.split("\r\n");
    for (let i = 0; i < lines.length; i++) {
        const line_data = lines[i].split(",");
        const card_name = line_data[1] ? line_data[1] : "";
        if (card_name.includes("\/\/")) {
            card_name.split("\/\/").forEach(split_card_name => {
                card_map.set(sanitize_card_name(split_card_name), line_data.slice(2));
            });
        }
        card_map.set(sanitize_card_name(line_data[1]), line_data.slice(2));
    }
} else {
    alert("HTTP-Error: " + response.status);
}

function createPlot(card_name) {
    const card_prices = card_map.get(card_name);

    if (card_prices) {
        layout.title = card_name;
        Plotly.newPlot("plot-div", [
            {
                y: card_prices.slice(2),
                x: card_map.get("card name").slice(2),
                hovertemplate: "$%{y:.2f}<extra></extra>"
            }],
            layout,
            config);
    } else {
        layout.title = "No data found for: " + card_name;
        Plotly.newPlot("plot-div", [], layout, config);
    }
}

function sanitize_card_name(card_name) {
    if (card_name) {
        const cardNameRegex = new RegExp(/[^\sa-zA-Z]/g);
        return card_name.replaceAll(cardNameRegex, '').toLowerCase().trim();
    }
    return "";
}

function clearAndGetList() {
    const card_list = document.getElementById("card-list");
    while (card_list.hasChildNodes()) {
        card_list.removeChild(card_list.lastChild);
    }
    return card_list;
}

function autocomplete_card_name() {
    const card_name = document.getElementById("card_name");
    const url = "https://api.scryfall.com/cards/autocomplete?q=" + card_name.value;
    fetch(url).then(function (response) {
        return response.json();
    }).then(function (data) {
        const card_list = clearAndGetList();
        const card_prices_arr = [];
        for (let i = 0; i < data["data"].length; i++) {
            const li = document.createElement("li");
            li.innerText = sanitize_card_name(data["data"][i].toLowerCase());

            if (li.innerText != "" && card_map.has(sanitize_card_name(li.innerText))) {
                li.onclick = function () { createPlot(li.innerText) };
                const a_tag = document.createElement("a");
                a_tag.href = "#";
                a_tag.appendChild(li);
                card_list.appendChild(a_tag);
                const obj = {
                    y: card_map.get(sanitize_card_name(li.innerText)).slice(2),
                    x: card_map.get("card name").slice(2),
                    hovertemplate: "$%{y:.2f}",
                    name: li.innerText
                };
                card_prices_arr.push(obj);
            }
        }
        layout.title = card_name.value;
        Plotly.newPlot("plot-div", card_prices_arr, layout, config);
    }).catch(function (err) {
        alert("Scryfall API Error: " + err);
    });
}
document.getElementById("card_name").addEventListener("input", autocomplete_card_name);