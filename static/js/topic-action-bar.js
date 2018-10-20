$(document).ready(function() {

    var $feeds = $(".feeds");

    $feeds.on('click', '.topic-list .topic-item .action-item', function (e) {
        var $topicObj = $(this).parents('.topic-item');
        var topicID = $topicObj[0].id.split('-')[1];
        if ($(this).hasClass('follow')) {
            $.get("/account/follow_topic/" + topicID + "/", {'follow': '1'}, function (data) {
                var $topicItems = $feeds.find('.topic-list .topic-item#t-' + topicID);
                $topicItems.find('.follow.action-item').removeClass('show').addClass('hide');
                $topicItems.find('.unfollow.action-item').removeClass('hide').addClass('show').find('.follower-count').text(data.count);
                var topicHtml = '<li class="user-topic-item row d-flex align-items-center" id="t-' + topicID + '">\n' +
                    '                        <div class="photo-wrapper small-icon col-md-4">\n' +
                    '                            <a href="#">\n' +
                    '                                <img class="profile_photo_img" src="' + data.url + '"  alt="' + data.name + '" height="50" width="50">\n' +
                    '                            </a>\n' +
                    '                        </div>\n' +
                    '                        <div class="info col-md-8">\n' +
                    '                            <div class="full-name">' + data.name + '</div>\n' +
                    '                        </div>\n' +
                    '                    </li>';
                $('.user-topic-bar ul').append(topicHtml);
            });
        } else {
            $.get("/account/follow_topic/" + topicID + "/", {'follow': '0'}, function (data) {
                var $topicItems = $feeds.find('.topic-list .topic-item#t-' + topicID);
                $topicItems.find('.follow.action-item').removeClass('hide').addClass('show').find('.follower-count').text(data.count);
                $topicItems.find('.unfollow.action-item').removeClass('show').addClass('hide');
                $('.user-topic-bar ul li#t-' + topicID).remove();
            });
        }

        e.stopPropagation();
    });

});