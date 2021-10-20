console.log("Running")
$('#dashboard-but').on('click',function() {
    console.log("Running1")
    //If 1 is showing, show 2, hide all other divs
    $('#main-1').show().siblings('main').hide();
});
$('#orders-but').on('click',function() {
    console.log("Running2")
    //If 1 is showing, show 2, hide all other divs
    $('#main-2').show().siblings('main').hide();
});
$('#products-but').on('click',function() {
    console.log("Running4")
    //If 1 is showing, show 2, hide all other divs
    $('#main-3').show().siblings('main').hide();
});
$('#customers-but').on('click',function() {
    console.log("Running5")
    //If 1 is showing, show 2, hide all other divs
    $('#main-4').show().siblings('main').hide();
});
$('#settings-but').on('click',function() {
    console.log("Running3")
    //If 1 is showing, show 2, hide all other divs
    $('#main-5').show().siblings('main').hide();
});

