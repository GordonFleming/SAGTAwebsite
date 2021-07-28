$('.carousel').carousel({
    interval: 2000
})

var apply = document.getElementById("applyNav");
apply.addEventListener("click",function(){
    document.getElementById('Apply').scrollIntoView({ behavior: 'smooth', block: 'center' });
})