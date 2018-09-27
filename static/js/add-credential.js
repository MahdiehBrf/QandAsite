$(document).ready(function() {

    $(".choose-credential-form .popup .add-credential").click(function (e) {
        console.log($(this));
        $(this).siblings('.credentials').find('.credential-types').removeClass('hide').addClass('show');
        e.stopPropagation();
    });

    $(".choose-credential-form .popup-form .credential-types .credit-type-item").on('click', function (e) {
        var creditType = $(this).attr('class').split(' ')[1];
        var $popupFormObj = $('.choose-credential-form .popup-form');
        $popupFormObj.find('.main').removeClass('show').addClass('hide');
        $popupFormObj.find('.add-type-credential#' + creditType).removeClass('hide').addClass('show');
        e.stopPropagation();

    });

    $(".choose-credential-form .popup-form .add-type-credential .buttons #cancel").on('click', function (e) {
        $(this).parents('.add-type-credential').removeClass('show').addClass('hide');
        $('.choose-credential-form .popup-form .main').removeClass('hide').addClass('show');
        e.stopPropagation()
    });


    $(".choose-credential-form .popup .main .submit_button").click(function (e) {
        var $formObj = $(".choose-credential-form").removeClass('hide').addClass('show');
        var answerID = $formObj[0].id;
        if (answerID === '0') {
            $formObj.removeClass('show').addClass('hide');
            $('.overlay').css("opacity", "1").css("position", "unset");
            $.get("/user_credentials_all/", {}, function (data) {
                $('.creditional-bar ul').html(data);
            });
        } else {
            var $checkedCredential = $formObj.find('input[name=\'answer-credential-rdio\']:checked');
            var credentialID = $checkedCredential[0].id.split('-')[1];
            var credentialValue = $checkedCredential.parent().find('.credential-name').text();
            if (credentialID !== undefined) {

                $.get("/answer_add_credential/" + answerID + "/" + credentialID + "/", {}, function (data) {
                    $formObj.removeClass('show').addClass('hide');
                    $('.overlay').css("opacity", "1").css("position", "unset");
                    var $answerCredentialObj = $(".answer.full#a-" + answerID).find('.info .answer-credential');
                    $answerCredentialObj.find('.answer-credential-value').text(credentialValue)[0].id = "c-" + credentialID;
                    $answerCredentialObj.find('.edit-answer-credential').text('ویرایش');
                });
            }
        }

        e.stopPropagation();
    });


    $('.choose-credential-form .popup-form .add-type-credential').submit(function (e) {
        event.preventDefault();
        var creditType = $(this)[0].id;
        var $creditForm = $(this);
        $.post("/add_credential/" + creditType + "/", $(this).serializeArray(), function (data) {
            $creditForm.removeClass('show').addClass('hide');
            $('.choose-credential-form .popup-form .main').removeClass('hide').addClass('show').find('.credentials ul.' + creditType + '-set').append(data);

        });
        return false;
    });

    $('.choose-credential-form .popup-form .add-type-credential .buttons .submit_button').click(function (e) {

    });

    $(".choose-credential-form").click(function (e) {
        $(this).find('.credentials .credential-types').removeClass('show').addClass('hide');
    });

    $(".creditional-bar .edit").click(function (e) {
        var $formObj = $(".choose-credential-form").removeClass('hide').addClass('show');
        $formObj[0].id = 0;
        $formObj.find('input[type=\'radio\']').addClass('hide');
        $('.overlay').css("opacity", "0.2").css("position","absolute");
        e.stopPropagation();
    });

});