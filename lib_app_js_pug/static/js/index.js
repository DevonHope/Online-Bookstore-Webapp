 function menu(x){
     x.classList.toggle("change");
     console.log(x.classList);
     var sidenavw = document.getElementById("sideNav").style.width
     if(sidenavw == "250px"){
         closeNav();
     }else{
         openNav();
     }
 }
 function openNav(){
   document.getElementById("sideNav").style.width = "250px";
 }
 function closeNav(){
   document.getElementById("sideNav").style.width = "0";
 }
 const input = document.getElementById("search-input");
 const searchBtn = document.getElementById("search-btn");
 const expand = () => {
 searchBtn.classList.toggle("close");
   input.classList.toggle("square");
 };
 searchBtn.addEventListener("click", expand);
