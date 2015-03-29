<!--
    var player = null;
    var vidId = "";
    var musicchannelId = "";
    $(document).ready(function() {
        musicchannelId = document.getElementById("channel-title").getAttribute("data-channel-id");
        vidId = document.getElementById("player").getAttribute("data-video-id")
        scrollChat();

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
                {'musicchannel': musicchannelId, 'message': $("#new-message-input").val()},
                function(data) {
                    document.getElementById('chatlist').innerHTML += data.message;
                    scrollChat();
                });
        });

        $("#new-message-input").keypress(function(event) {
            if (event.keyCode == 13) {
                $(this).parent().find("button:eq(0)").trigger("click");
                $(this).val("");
            }
        });

        window.onYouTubeIframeAPIReady = function()  {
            if (vidId) {
                player = new YT.Player('player', {
                                        height: '390',
                                        width: '640',
                                        videoId: vidId,
                                        events: { 
                                            'onReady': onPlayerReady,
                                            'onStateChange': onPlayerStateChange
                                            }
                                        });
            }
        };
    });

    function scrollChat() {
        var chatbox = document.getElementById('chatbox');
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    function onPlayerStateChange(event) {
        if (event.data == 0) {
            getNextSong();
        }
    }

    function onPlayerReady(event) {
        event.target.playVideo();
    }

    function getNextSong() {
        /*
        TODO: need to remove the row from the playlist
        var row = document.getElementById("playlist-row-");
        row.parent.removeChild(row);
        */
        $.get('/get_next_song/', 
                {'musicchannel': musicchannelId,
                 'song': vidId},
                 function(data) {
                    if (data.song_to_play != "") {
                        vidId = data.song_to_play;
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
                    document.getElementById('chatlist').innerHTML = data.messages;
                    scrollChat();
                },
                dataType: 'json',
                complete: poll,
                timeout: 2000
            })
        }, 5000);
    })();
-->