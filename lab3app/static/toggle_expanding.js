window.onload = () => {
    filtersButton = document.getElementById("filter-button");
    filtersButton.addEventListener('click', () => {
        filters = document.getElementsByClassName("filters")[0];
        if(filters.classList.contains("expanded")){
            filters.classList.remove("expanded");
        }
        else {
            filters.classList.add("expanded");
        }
    });
}