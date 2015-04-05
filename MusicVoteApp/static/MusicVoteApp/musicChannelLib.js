<!--
    var player = null;
    var vidId = "";
    var musicchannelId = "";
    
    $(document).ready(function() {
        musicchannelId = document.getElementById('channel-title').getAttribute('data-channel-id');
        vidId = document.getElementById('player').getAttribute('data-video-id')
        scrollChat();

        $('.voteBtn').on('click', voteBtnClickEvent);

        $('#submit-message').on('click', sendMessage);

        $('#new-message-input').keypress(function(event) {
            if (event.keyCode == 13) {
                $(this).parent().find('button:eq(0)').trigger('click');
                $(this).val('');
            }
        });

        window.onYouTubeIframeAPIReady = function()  {
            if (vidId) {
                player = new YT.Player('player', {
                                            height: '390',
                                            width: '640',
                                            videoId: vidId,
                                            events: {'onReady': onPlayerReady, 'onStateChange': onPlayerStateChange}
                                        });
            }
        };
    });

    function sendMessage() {
        var message_text = $('#new-message-input').val();

        if (message_text != "") {
            $.post('/send_message/',
                {'musicchannel': musicchannelId, 'message': message_text},
                function(data) {
                    document.getElementById('chatlist').innerHTML += data.message;
                    scrollChat();
                });
        }
    }

    function voteBtnClickEvent() {
        $.post('/vote/',
            {'musicchannel': musicchannelId, 
             'song': $(this).attr('data-song-id')},
             function(data) {
                document.getElementById('song-votes-' + data.song_id).innerHTML = data.votes;
         });
    }

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
        var row = document.getElementById('playlist-row-' + vidId);
        row.parentNode.removeChild(row);
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

    function updateChat(messages) {
        document.getElementById('chatlist').innerHTML = messages;
        scrollChat();
    }

    function updatePlaylist(playlist) {
        voteBtns = document.getElementsByClassName('voteBtn');
        for (var i = 0; i < voteBtns.length; i++) {
            voteBtns[i].on('click', voteBtnClickEvent);
        }

        tableHeader = '<tr><th>Song</th><th>Votes</th></tr>';
        document.getElementById('playlist-table').innerHTML = tableHeader + playlist
    }

    (function poll() {
        setTimeout(function() {
            $.ajax({
                url: '/polling/',
                data: {'musicchannel': musicchannelId},
                type: 'GET',
                success: function(data) {
                    updateChat(data.messages);
                    updatePlaylist(data.playlist);
                },
                dataType: 'json',
                complete: poll,
                timeout: 2000
            })
        }, 5000);
    })();
-->