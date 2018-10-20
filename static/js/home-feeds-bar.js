$(document).ready(function() {

    var $feeds = $(".feeds");

    $('.feed-bar .feed-item').click(function(e) { // limit click to children of main menu
        var $feedObj = $(this);
        var userID = $('.dropdown-menu.profile-menu')[0].id.split('-')[1];
        if(!$feedObj.hasClass('selected')){
            var feedName = $feedObj.attr('class').split(' ')[1];
            $('.feed-bar .feed-item').removeClass('selected');
            $feedObj.addClass('selected');
            $.get("/account/profile_get_feed/" + userID + "/" + feedName + "/", {}, function (data) {
                $('.feeds').html(data);
            });
        }

        e.stopPropagation();
    });



     $feeds.on('click', '.search-topic img', function (e) {
        var name = $(this).siblings('textarea')[0].value;
        $.get("/account/search-topic/", {'name':name, 'way':'full'}, function (data) {
            $('.feeds .searched-topics').html(data);
        });
            e.stopPropagation();
    });
});