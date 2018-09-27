$(document).ready(function() {
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