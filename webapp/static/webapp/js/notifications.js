$(document).ready(function() {
  let notiCont = $('#notiCont');

  $.ajax({
    type: 'GET',
    url: '/api/notifications',
    data: {
      learner: learner,
    },
    success: function(data) {
      let notifications = data.notifications;
      let avatarEvol = data.avatar[0];
      for (let i = 0; i < notifications.length; i++) {
        let notiType,
          notiTitle = notifications[i].title,
          notiViewed = notifications[i].viewed;
        if (notifications[i].type === 'achievement') {
          notiType = '<i class="fas fa-trophy"></i>';
        } else if (notifications[i].type === 'level_up') {
          notiType = '<i class="fas fa-chart-line"></i>';
        } else if (notifications[i].type === 'avatar_evolution') {
          notiType = '<i class="fas fa-child"></i>';
        } else if (notifications[i].type === 'uoda_completed') {
          notiType = '<i class="fas fa-book"></i>';
        } else if (notifications[i].type === 'evaluation_completed') {
          notiType = '<i class="fas fa-file-alt"></i>';
        }
        if (notiViewed === false) {
          notiViewed = 'new';
        } else {
          notiViewed = '';
        }
        $('#notiCont').append(`
          <div class="noti ${notiViewed}">
          <div class="noti_icon">
            <div class="icon_container">
              ${notiType}
            </div>
          </div>
          <div class="noti_text">
            ${notiTitle}
          </div>
        </div>
        `);
      }
      if(avatarEvol.viewed === false){
        $('#evolutionModal .avatar img').attr('src', '/static/webapp/media/'+avatarEvol.avatar_name+'0'+avatarEvol.previous_evolution+'.png')
        $('#evolutionModal .avatar-new img').attr('src', '/static/webapp/media/'+avatarEvol.avatar_name+'0'+avatarEvol.current_evolution+'.png')
        $('#evolutionModal').foundation('open');
      }
    },
  });

  let notiClick = false;
  $('#noti-btn').on('click', function() {
    if (notiClick === false) {
      $.ajax({
        method: 'POST',
        type: 'POST',
        url: '/api/notifications/',
        data: {
          learner: learner,
        },
      });
    }
    notiClick = true;
  });
});
