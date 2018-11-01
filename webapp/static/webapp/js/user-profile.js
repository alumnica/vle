 $('#selected-avatar').val($('.avatar-main img').attr('id'));
 /**
  * Sends avatar changed event
  */
 $('.other-avatars').on('click', 'img', function () {
     let clicked = $(this);
     let main = $('.the-avatar img');
     clicked.parent().html(main);
     $('.the-avatar').html(clicked);
     $('#selected-avatar').val(clicked.attr('id'));

     $.ajax({
         url: '/api/avatar',
         data: {
             'avatar': clicked.attr('id'),
             'learner': learner
         }
     });
 });

// /**
//  * Sends profile extra information
//  */
// $('#user-info-btn').on('click', function(){
//     let matFav = $('#materia-fav').val(),
//         hora = $('#horario').val(),
//         uni = $('#univ').val();
//
//     let url = '/api/profile_info/';
//
//     $.ajax({
//         method: 'POST',
//         type: 'POST',
//         url: url,
//         data: {
//             'favourite_subject': matFav,
//             'working_time': hora,
//             'university_studies': uni,
//             'learner': pk
//         }
//     });
//      // Create div
//     const span = document.createElement('span');
//     // Add classes
//     span.className = 'saved';
//     span.innerHTML = 'GUARDADO';
//
//     $('.extra-info').append(span);
// //     Timeout after 3 sec
//     setTimeout(function(){
//       document.querySelector('.saved').remove();
//     }, 3000);
// });
//
// /**
//  *
//  */
// $(document).ready(function () {
//     $.ajax({
//         type: 'GET',
//         url: '/api/profile_info',
//         data: {
//             'learner': pk
//         },
//         success: function (data) {
//             $('#materia-fav').val(data.favourite_subject);
//             $('#horario').val(data.working_time);
//             $('#univ').val(data.university_studies);
//
//         }
//     })
// });
$(document).ready(function () {
  // add notification icon to recent activity depending on the type of notification
  $('.recent-cell').each(function () {
    let notiType = $(this).attr('noti-type');
    if(notiType === 'achievement'){
        $(this).find('.recent-cell_icon').append('<i class="fas fa-trophy"></i>')
    } else if (notiType === 'level_up'){
        $(this).find('.recent-cell_icon').append('<i class="fas fa-chart-line"></i>')
    } else if (notiType === 'avatar_evolution'){
        $(this).find('.recent-cell_icon').append('<i class="fas fa-child"></i>')
    } else if (notiType === 'uoda_completed'){
        $(this).find('.recent-cell_icon').append('<i class="fas fa-book"></i>')
    } else if (notiType === 'evaluation_completed'){
        $(this).find('.recent-cell_icon').append('<i class="fas fa-file-alt"></i>')
    }
  });

    // check badge version and color in the stars appropriately
  $('.badge-cell').each( function () {
    let starCount = $(this).attr('version');
    if(starCount == 1){
      $(this).find('.badge-cell_stars').append(
        '<i class="fa fa-star earned"></i><i class="fa fa-star"></i><i class="fa fa-star"></i>'
        )
      } else if (starCount == 2){
        $(this).find('.badge-cell_stars').append(
        '<i class="fa fa-star earned"></i><i class="fa fa-star earned"></i><i class="fa fa-star"></i>'
        )
      } else if (starCount == 3){
        $(this).find('.badge-cell_stars').append(
        '<i class="fa fa-star earned"></i><i class="fa fa-star earned"></i><i class="fa fa-star earned"></i>'
        )
      }
    });
  $('.achievement').each(function () {
    let ach = $(this);
    if(ach.attr('earned') == 1){
      ach.removeClass('wip')
    }
  })
});