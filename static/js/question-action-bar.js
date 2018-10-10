$(document).ready(function() {

    var $mainSection = $(".main-section ");

    $mainSection.on('click','.question .qu.action-bar .action-item.edit', function (e) {
       var $questionObj = $(this).closest('.question');
       var questionID = $questionObj[0].id.split('-')[1];
        var $formObj = $(".ask-form").removeClass('hide').addClass('show').find('form').attr('action', '/edit/' + questionID + '/');
        $formObj.find('textarea').text($questionObj.find('.question-title')[0].innerText);
        $formObj.find('input')[1].value = 'ویرایش';
        $('.overlay').css("opacity", "0.2").css("position","absolute");
        e.stopPropagation();
    });

    $mainSection.on('click','.question .qu.action-bar .action-item.answer', function (e) {
        var $editorObj = $(e.target).parents('.action-bar').siblings('form.editor');
        if ($editorObj.hasClass('hide')){
            $(this).addClass('selected');
            $editorObj.removeClass('hide').addClass('show');
        }else{
            $(this).removeClass('selected');
            $editorObj.removeClass('show').addClass('hide');
        }

        e.stopPropagation();
    });

    $mainSection.on('click','.question .qu.action-bar .action-item.follow', function (e) {
        var $editObj = $(this);
        var questionID = $(e.target).closest('.question')[0].id.split('-')[1];
            if ($(this).hasClass('selected')){
                $.get("/unfollow/"+ questionID + "/", {}, function(data) {
                    $editObj.find('.follower-count')[0].innerHTML = data.follower_count;
                    $editObj.removeClass('selected');
                });
            }else {
                $.get("/follow/"+ questionID + "/", {}, function(data) {
                    $editObj.find('.follower-count')[0].innerHTML = data.follower_count;
                    $editObj.addClass('selected');
                });
            }

        e.stopPropagation();
    });

    function get_best_question_based_users($topicObj, questionID) {
        $.get("/best_question_based_users/" + questionID + "/", {}, function (data) {
            $('.request-form .users').html(data);
            if($topicObj!==undefined){
                $('.request-form .topics .topic-item').removeClass('selected');
                $topicObj.addClass('selected');
            }

        });
    }

    //Request Answer

    $mainSection.on('click','.question .qu.action-bar .action-item.request', function (e) {
        var $formObj = $(".ask-answer-form").removeClass('hide').addClass('show');
        var questionID = $(this).closest('.question')[0].id.split('-')[1];
        $formObj[0].id = questionID;
        $('.overlay').css("opacity", "0.2").css("position","absolute");
        $.get("/question_topic/" + questionID + "/", {}, function (data) {
            $formObj.find('.request-form .topics ul').html(data);
        });
        get_best_question_based_users(undefined, questionID);
        e.stopPropagation();
    });


    $(".request-form .topics").on('click', '.topic-item',  function (e) {
        e.stopPropagation();
        var $topicObj = $(this);
        console.log($topicObj);
        var questionID = $(this).parents('.ask-answer-form')[0].id;
        if ($topicObj[0].id!=='all') {
            var topicID = $topicObj[0].id.split('-')[1];
            if (!$topicObj.hasClass('selected')) {
                $.get("/best_topic_based_users/" + topicID + "/" + questionID + "/", {}, function (data) {
                    $('.request-form .users').html(data);
                    $('.request-form .topics .topic-item').removeClass('selected');
                    $topicObj.addClass('selected');
                });
            }
        }else {
            if (!$topicObj.hasClass('selected')) {

                get_best_question_based_users($topicObj, questionID);
            }
        }

    });

    $(".request-form .users").on('click','.user-item svg', function (e) {

        e.stopPropagation();
        var $userObj = $(this);
        console.log($userObj);
        var questionID = $(this).parents('.ask-answer-form')[0].id;
        var userID = $userObj.parents('.user-item')[0].id.split('-')[1];
        $.get("/answer_request/" + userID + "/" + questionID + "/", {}, function (data) {
            $userObj.remove();
        });

    });




});