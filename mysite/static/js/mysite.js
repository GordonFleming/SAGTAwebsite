$('.carousel').carousel({
    interval: 6000   
})

var apply = document.getElementById("applyNav");
apply.addEventListener("click",function(){
    document.getElementById('Apply').scrollIntoView({ behavior: 'smooth', block: 'center' });
})