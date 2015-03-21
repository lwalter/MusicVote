<!--
    var player = null;
    var vidId = "";
    var musicchannelId = "";

    $(document).ready(function() {
        musicchannelId = document.getElementById("channel-title").getAttribute("data-channel-id");

        $(".voteBtn").click(function() {
            $.post('/vote/',
                    {'musicchannel': musicchannelId, 
                        'song': $(this).val()}
            );
        });

        $("#testBtn").click(function() {
            alert(player.getCurrentTime());
        });
        
        // Construct the YouTube player
        vidId = document.getElementById("player").getAttribute("data-song-id")
        window.onYouTubeIframeAPIReady = function()  {
            player = new YT.Player('player', {
            height: '390',
            width: '640',
            videoId: vidId,
            events: { 
                'onReady': onPlayerReady,
                'onStateChange': onPlayerStateChange
                }
            });
        };
    });

    function onPlayerStateChange(event) {
        if (event.data == 0) {
            getNextSong();
        }
    }

    function onPlayerReady(event) {
        event.target.playVideo();
    }

    function getNextSong() {
        alert("Time to get the next song!")
        $.get('/get_next_song/', 
                {'musicchannel': musicchannelId,
                 'song': vidId},
                alert("Success"));
    }
-->