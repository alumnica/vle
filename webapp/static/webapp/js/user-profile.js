 $('#selected-avatar').val($('.avatar-main img').attr('id'));
 /**
  * Sends avatar changed event
  */
 $('.other-avatars').on('click', 'img', function () {
     let clicked = $(this);
     let main = $('.the-avatar img');
     clicked.parent().append(main.attr('class', 'the-others'));
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
 $('#user-info-btn').on('click', function(){
     let matFav = $('#materia-fav').val(),
         hora = $('#horario').val(),
         uni = $('#univ').val(),
         first_name = $('#first_name').val(),
         last_name = $('#last_name').val(),
         birth_date = $('#birth_date').val(),
         gender = $('input:radio[name=gender]:checked').val();

     let url = '/api/profile_info/';

     $.ajax({
         method: 'POST',
         type: 'POST',
         url: url,
         data: {
             'first_name': first_name,
             'last_name': last_name,
             'birth_date': birth_date,
             'gender': gender,
             'favourite_subject': matFav,
             'working_time': hora,
             'university_studies': uni,
             'learner': learner
         },
         success: function () {
           $('#info').foundation('close');
           swal({
             type: 'success',
            title: 'Cambios guardados',
            showConfirmButton: false,
            timer: 1500
           });
         }
     });
      // Create div
     const span = document.createElement('span');
     // Add classes
     span.className = 'saved';
     span.innerHTML = 'GUARDADO';

     $('.extra-info').append(span);
 //     Timeout after 3 sec
     setTimeout(function(){
       document.querySelector('.saved').remove();
     }, 3000);
 });
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
  });

         $.ajax({
         type: 'GET',
         url: '/api/profile_info',
         data: {
             'learner': learner
         },
         success: function (data) {
             $('#first_name').val(data.first_name);
             $('#last_name').val(data.last_name);
             $('#birth_date').val(data.birth_date);
             let radios = $('input:radio[name=gender]');
             radios.filter('[value='+data.gender+']').prop('checked', true);
             $('#materia-fav').val(data.favourite_subject);
             $('#horario').val(data.working_time);
             $('#univ').val(data.university_studies);

         }
     })

});