
$(document).ready(function() {

    $(".question .topics").on('click', '.topic-item.edit_topics', function (e) {
        var $formObj = $(".edit-topics-form").removeClass('hide').addClass('show');
        $formObj[0].id = $(this).closest('.question')[0].id.split('-')[1];
        $('.overlay').css("opacity", "0.2").css("position","absolute");
        e.stopPropagation();
    });

    $(".question-topics .added-topics .question-topic-item img").click(function (e) {
        var $topicObj = $(this).parent();
        var topicID = $topicObj[0].id.split('-')[1];
        var topicQuestionID = $(this).parents('.edit-topics-form')[0].id;
        $.get("/topic_delete/" + topicQuestionID + "/" + topicID + "/", {}, function (data) {
            $topicObj.remove();
        });
        e.stopPropagation();
    });

    $(".question-topics .search-topic img").click(function (e) {
        var name = $(this).siblings('textarea')[0].value;
        $.get("/account/search-topic/", {'name': name, 'way': 'summary'}, function (data) {
            $('.question-topics .searched-topics').html(data);
        });
        e.stopPropagation();
    });

    $(".question-topics .searched-topics").on('click', '.question-topic-item svg', function (e) {
        var $topicObj = $(this).parent();
        var topicID = $topicObj[0].id.split('-')[1];
        var topicQuestionID = $(this).parents('.edit-topics-form')[0].id;
        $.get("/topic_add/" + topicQuestionID + "/" + topicID + "/", {}, function (data) {
            $topicObj.remove();
            if (data.included === 0) {
                var newItem = '<li id="t-' + data.topic_id + '" class="question-topic-item d-flex align-items-center">\n' +
                    '<img src="/static/image/delete.png">\n' +
                    '<div>' + data.topic_name + '</div>\n' +
                    '</li>';
                $('.question-topics .added-topics').append(newItem);
            }
        });
        e.stopPropagation();
    });

    $(".edit-topics-form .popup .submit_button").click(function (e) {

        var $topics = $(this).siblings('.popup-form').find('.added-topics li');
        var newHtml = '';
        for (var i=0; i < $topics.length; i++) {
            if (i < 2)
                newHtml += '<div class="topic-item">' + $topics[i].children[1].innerText + '</div>';
            else {
                newHtml += '<div class="topic-item">+'+ ($topics.length - 2) +'</div>';
                break
            }
        }
        newHtml  += '<div class="topic-item edit_topics d-flex">\n' +
                    '    <img src="/static/image/edit.svg">\n' +
                    '    <div>ویرایش</div>\n' +
                    '</div>';
        $('.question .topics').html(newHtml);
    });


});
