<!--
    var player = null;
    var vidId = "";
    var musicchannelId = "";
    $(document).ready(function() {
        musicchannelId = document.getElementById("channel-title").getAttribute("data-channel-id");

        $(".voteBtn").click(function() {
            $.post('/vote/',
                    {'musicchannel': musicchannelId, 
                     'song': $(this).attr('data-song-id')},
                     function(data) {
                        document.getElementById("song-votes-" + data.song_id).innerHTML = data.votes;
                     });
        });
        
        // Construct the YouTube player
        vidId = document.getElementById("player").getAttribute("data-video-id")
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
        $.get('/get_next_song/', 
                {'musicchannel': musicchannelId,
                 'song': vidId},
                 function(data) {
                    if (data.song_to_play != "") {
                        player.loadVideoById(data.song_to_play);
                    }
                 });
    }
-->