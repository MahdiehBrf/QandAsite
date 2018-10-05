$(document).ready(function() {

    var span = $('<span>').css('display','inline-block')
        .css('word-break','break-all').appendTo('body').css('visibility','hidden');
        function initSpan(textarea){
          span.text(textarea.text())
              .width(textarea.width())
              .css('font',textarea.css('font'));
        }
        $('textarea.text').on({
            input: function(){
              var text = $(this).val();
              span.text(text);
              $(this).height(text ? span.height() : '1.1em');
            },
            focus: function(){
             initSpan($(this));
            },
            keypress: function(e){
                if(e.which == 13) e.preventDefault();
            }
        });


    function prepare_year_selects() {
            var select = $('select#year');

            for (var i = new Date().getFullYear(); i>=1900; i--){
                var opt = '<option value='+i+'>'+i+'</option>';
                select.append(opt);
            }
        }

        function prepare_topic_selects() {
            var select = $('select#topic');

            $.get("/topic_all/", {}, function (data) {
                for (var topicID in data.topics){
                    var opt = '<option value='+topicID+'>'+data.topics[topicID]+'</option>';
                    select.append(opt);
                }
            });

        }

        window.onload = function() {
          fetch_api_data();
          prepare_year_selects();
          prepare_topic_selects()
        };
});