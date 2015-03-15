<!--
	$(document).ready(function() {
		$(".voteBtn").click(function() {
			$.ajax({
				url: '/vote/',
				data: {'musicchannel': $("#channel-title").val(), 'song': $(this).val()},
				type: 'POST',
				failure: function(data) {
					alert("error");
				}
			});
		});
	});
-->