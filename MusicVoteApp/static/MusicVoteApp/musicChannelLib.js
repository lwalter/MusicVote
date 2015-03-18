<!--
    $(document).ready(function() {
        $(".voteBtn").click(function() {
            $.ajax({
                url: '/vote/',
                data: {'musicchannel': document.getElementById("channel-title").getAttribute("data-channel-id"), 
                        'song': $(this).val()},
                type: 'POST',
                failure: function(data) {
                    alert("Error");
                }
            });
        });
    });
-->