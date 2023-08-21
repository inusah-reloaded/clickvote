var iconMenu = document.getElementById('menu-icon');
iconMenu.addEventListener("click", function(){
     elem = document.getElementById('sidenav');
    if(elem.style.width === "0px" || elem.style.width === ''){
        elem.style.width = "40%";
    } else {
         elem.style.width = "0";
    }

});

function openSideNav(){
    document.getElementById("sidenav").style.width = "40%";
};
function closeSideNav(){
    document.getElementById("sidenav").style.width = "0";
}
