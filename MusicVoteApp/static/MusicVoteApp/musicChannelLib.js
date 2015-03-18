<!--
    $(document).ready(function() {
        $(".voteBtn").click(function() {
            $.post('/vote/',
                    {'musicchannel': document.getElementById("channel-title").getAttribute("data-channel-id"), 
                        'song': $(this).val()}
            );
        });
    });
-->