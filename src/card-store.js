window.onload = function () {

    function getCards() {
        return cards;
    }

    let cards; // Array of card names
    updateList();

    function updateList() {
        const cards_json = sessionStorage.getItem('card-store');
        if (cards_json) {
            cards = JSON.parse(cards_json);
            const card_list = document.getElementById('card-list');
            if (card_list) {
                for (let i = 0; i < cards.length; i++) {
                    const li = document.createElement("li");
                    li.innerText = cards[i];
                    card_list.appendChild(li);
                }
            }
        }
    }

    function addCard(card_name) {
        cards.push(card_name);
        saveCards();
        updateList();
    }

    function saveCards() {
        sessionStorage.setItem('card-store', JSON.stringify(cards));
    }

    function clearAndGetList() {
        const card_list = document.getElementById("cards-to-add");
        while (card_list.hasChildNodes()) {
            card_list.removeChild(card_list.lastChild);
        }
        return card_list;
    }

    function addCardToList() {
        const cards_to_add = clearAndGetList();
        const url = "https://api.scryfall.com/cards/autocomplete?q=" + document.getElementById("card-name").value;
        fetch(url).then(function (response) {
            return response.json();
        }).then(function (data) {
            for (let i = 0; i < data["data"].length; i++) {
                const li = document.createElement("li");
                const regex = new RegExp(",|\"");
                const card_name = data["data"][i].toLowerCase().replace(regex, "");
                if (card_name) {
                    li.innerText = card_name;
                    li.addEventListener("click", function () {
                        addCard(card_name);
                    });
                    cards_to_add.appendChild(li);
                }
            }
        }).catch(function (err) {
            alert("HTTP-Error: " + err);
        });
    }

    const card_name_input = document.getElementById("card-name");
    if (card_name_input) {
        card_name_input.addEventListener("input", addCardToList);
    }
}