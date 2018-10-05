$(document).ready(function() {
    $('.feeds').on('click', '.user-list .user-item .action-item', function (e) {
        var $userObj = $(this).parents('.user-item');
        var userID = $userObj[0].id.split('-')[1];
        if ($(this).hasClass('follow')){
            $.get("/follow_user/" + userID + "/", {'follow':'1'}, function (data) {
                var $userItems = $('.feeds .user-list .user-item#u-' + userID );
                $userItems.find('.follow.action-item').removeClass('show').addClass('hide');
                $userItems.find('.unfollow.action-item').removeClass('hide').addClass('show').find('.follower-count').text(data.count);
            });
        }else {
            $.get("/follow_user/" + userID + "/", {'follow':'0'}, function (data) {
                var $userItems = $('.feeds .user-list .user-item#u-' + userID );
                $userItems.find('.unfollow.action-item').removeClass('show').addClass('hide');
                $userItems.find('.follow.action-item').removeClass('hide').addClass('show').find('.follower-count').text(data.count);
            });
        }

            e.stopPropagation();
    });
});