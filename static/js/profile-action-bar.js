$(document).ready(function() {
    $('.profile .action-bar .action-item.follow, .answer .action-bar .action-item.follow').click(function(e) {
        var $followObj = $(this);
        console.log($followObj);
        var userID;
        if ($followObj.closest('.user').length===1)
            userID = $followObj.closest('.user')[0].id.split('-')[1];
        else
            userID = $followObj.closest('.profile')[0].id.split('-')[1];
            if ($(this).hasClass('selected')){
                $.get("/follow_user/" + userID + "/", {'follow':'0'}, function (data) {
                    $followObj.parent().siblings('.follower-count').removeClass('selected')[0].innerHTML = data.count + ' دنبال‌کننده';
                    $followObj.removeClass('selected');
                });
            }else {
                $.get("/follow_user/" + userID + "/", {'follow':'1'}, function (data) {
                    $followObj.parent().siblings('.follower-count').addClass('selected')[0].innerHTML = data.count + ' دنبال‌کننده';
                    $followObj.addClass('selected');
                });
            }

        e.stopPropagation();
    });


    $(".profile .profile-image #id_avatar").change(function () {
        $(this).parents('form#edit_avatar_form').submit();
    });

    $(".profile .info .edit-input .submit_button").click(function (e) {
        var $submitObj = $(this);
        var action = $submitObj.attr('class').split(' ')[2];
        var userID = $submitObj.parents('.profile')[0].id.split('-')[1];
        if (action === 'edit-full-name'){
            var firstName = $submitObj.siblings("textarea.first-name")[0].value;
            var lastName = $submitObj.siblings("textarea.last-name")[0].value;
            $.get("/edit_full_name/" + userID + "/", {'first_name':firstName, 'last_name':lastName}, function (data) {
                $submitObj.parent().removeClass('show').addClass('hide');
                $submitObj.parent().siblings(".user-value").removeClass('hide').addClass('show').text(firstName + " " + lastName);
                $submitObj.parent().siblings(".profile-edit").removeClass('hide').addClass('show');
            });
        }else if(action === "add-main-credential" || action === "edit-main-credential"){
            var text = $submitObj.siblings("textarea")[0].value;
            $.get("/edit_main_credential/" + userID + "/", {'text':text}, function (data) {
                $submitObj.parent().removeClass('show').addClass('hide');
                $submitObj.parent().siblings(".user-value").removeClass('hide').addClass('show').text(text);
                $submitObj.parent().siblings(".profile-edit").removeClass('hide').addClass('show').text('ویرایش');
            });
        }

            e.stopPropagation();
    });

    $(".profile .info .profile-edit").click(function(e) {
        $(this).siblings(".edit-input").removeClass('hide').addClass('show');
        $(this).siblings(".user-value").removeClass('show').addClass('hide');
        $(this).removeClass('show').addClass('hide');


        e.stopPropagation();
    });

    $(".profile .info .edit-input .profile-cancel-edit").click(function(e) {
        var $parent = $(this).parents(".edit-input");
        $parent.removeClass('show').addClass('hide');
        $parent.siblings(".user-value").removeClass('hide').addClass('show');
        $parent.siblings(".profile-edit").removeClass('hide').addClass('show');


        e.stopPropagation();
    });


    $('.feed-bar .feed-item').click(function(e) {
        var $feedObj = $(this);
        var userID = $('.profile')[0].id.split('-')[1];
        if(!$feedObj.hasClass('selected')){
            var feedName = $feedObj.attr('class').split(' ')[1];
            $('.feed-bar .feed-item').removeClass('selected');
            $feedObj.addClass('selected');
            $.get("/profile_get_feed/" + userID + "/" + feedName + "/", {}, function (data) {
                $('.feeds').html(data);
            });
        }

        e.stopPropagation();
    });


});