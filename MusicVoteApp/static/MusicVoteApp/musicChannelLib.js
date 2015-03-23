<!--
    var player = null;
    var vidId = "";
    var musicchannelId = "";
    $(document).ready(function() {
        musicchannelId = document.getElementById("channel-title").getAttribute("data-channel-id");
        vidId = document.getElementById("player").getAttribute("data-video-id")
        
        $(".voteBtn").click(function() {
            $.post('/vote/',
                    {'musicchannel': musicchannelId, 
                     'song': $(this).attr('data-song-id')},
                     function(data) {
                        document.getElementById("song-votes-" + data.song_id).innerHTML = data.votes;
                     });
        });
        
        $("#submit-message").click(function() {
            $.post('/send_message/', 
                    {'musicchannel': musicchannelId, 'message': $("#new-message-input").val()});
        });

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

    (function poll() {
        setTimeout(function() {
            $.ajax({
                url: '/get_messages/',
                data: {'musicchannel': musicchannelId},
                type: 'GET',
                success: function(data) {
                    document.getElementById('#chatlist').innerHTML = data.messages;
                },
                dataType: 'json',
                complete: poll,
                timeout: 2000
            })
        }, 5000);
    })();
-->