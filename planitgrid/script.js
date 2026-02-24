// JavaScript for tab switching
function openTab(evt, tabName) {
    let i, tabcontent, tabbuttons;

    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    tabbuttons = document.getElementsByClassName("tab-button");
    for (i = 0; i < tabbuttons.length; i++) {
        tabbuttons[i].className = tabbuttons[i].className.replace(" active", "");
    }

    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";

    // Populate grid when Tab 2 is opened
    if (tabName === 'Tab2') {
        populateGrid();
    }
}
/*// Initial load: show Tab 1 and populate grid if Tab 2 is active by default
document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('.tab-button').click(); // Simulate click on the first tab button
});*/
