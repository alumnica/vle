let input = document.getElementById("searcher");
input.addEventListener("keyup", function (event) {
    event.preventDefault();
    if (event.keyCode === 13) {
        let text = this.value;

        //text = text.normalize('NFD').replace(/[\u0300-\u036f]/g, "");

        window.location.href = "/search/search_odas/" + text + "/";
    }
});