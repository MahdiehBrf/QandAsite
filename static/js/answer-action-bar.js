$(document).ready(function() {

    var $mainSection = $(".main-section ");

    $mainSection.on('click','.answer .answ.action-bar .action-item.vote', function (e) {
        var $voteObj = $(this);
        var answerID = $(e.target).closest('.answer')[0].id.split('-')[1];
        console.log(answerID);
            if ($voteObj.hasClass('selected')){
                $.get("/devote/"+ answerID + "/", {}, function(data) {
                    $voteObj.find('.vote-count')[0].innerHTML = data.vote_count;
                    $voteObj.removeClass('selected');
                });
            }else {
                $.get("/vote/"+ answerID + "/", {}, function(data) {
                    $voteObj.find('.vote-count')[0].innerHTML = data.vote_count;
                    $voteObj.addClass('selected');
                });
            }

        e.stopPropagation();
    });

    $mainSection.on('click','.answer .answ.action-bar .action-item.bookmark', function (e) {
        var $bookmarkObj = $(this);
        var answerID = $(e.target).closest('.answer')[0].id.split('-')[1];
            if ($bookmarkObj.hasClass('selected')){
                $.get("/unbookmark/"+ answerID + "/", {}, function(data) {
                    $bookmarkObj.find('img').attr('src','/static/image/bookmark add.svg');
                    $bookmarkObj.find('div').text("اضافه به نشانه‌ها");
                    $bookmarkObj.removeClass('selected');
                });
            }else {
                $.get("/bookmark/"+ answerID + "/", {}, function(data) {
                    $bookmarkObj.find('img').attr('src',"/static/image/bookmark remove.svg");
                    $bookmarkObj.find('div').text("حذف از نشانه‌ها");
                    $bookmarkObj.addClass('selected');
                });
            }
         e.stopPropagation();
    });

    $mainSection.on('click','.answer .answ.action-bar .action-item.share', function (e) {
        var $shareObj = $(this);
        var answerID = $(e.target).closest('.answer')[0].id.split('-')[1];
            if ($shareObj.hasClass('selected')){
                $.get("/unshare/"+ answerID + "/", {}, function(data) {
                    $shareObj.removeClass('selected');
                });
            }else {
                $.get("/share/"+ answerID + "/", {}, function(data) {
                    $shareObj.addClass('selected');
                });
            }
         e.stopPropagation();
    });

    $mainSection.on('click','.answer .answ.action-bar .action-item.delete', function (e) {
        var $deleteObj = $(this);
        var answerID = $(e.target).closest('.answer')[0].id.split('-')[1];
        var $answer_question = $(e.target).closest('.question');
        $.get("/answer_delete/" + answerID + "/", {}, function (data) {
            if ($answer_question.length !== 0)
                $answer_question.find('.answers .answer#a-'+ answerID).remove();
            else
                $('.answer#a-' + answerID).remove()
        });
         e.stopPropagation();
    });

    $mainSection.on('click','.answer .action-bar .action-item.edit', function (e) {
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


    // $mainSection.on('click','', function (e) {
    //
    // });



});