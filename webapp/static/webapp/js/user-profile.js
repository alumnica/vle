$('#selected-avatar').val($('.avatar-main img').attr('id'));

$('.avatar-options').on('click', 'img', function () {
    let clicked = $(this);
    let main = $('.avatar-main img');
    clicked.parent().html(main);
    $('.avatar-main').html(clicked);
    $('#selected-avatar').val(clicked.attr('id'));

    $.ajax({
        url: '/api/avatar',
        data: {
            'avatar': clicked.attr('id'),
            'pk': pk
        }
    });
});

$('#user-info-btn').on('click', function(){
    let matFav = $('#materia-fav').val(),
        hora = $('#horario').val(),
        uni = $('#univ').val();

    let url = '/api/profile_info/';

    $.ajax({
        method: 'POST',
        type: 'POST',
        url: url,
        data: {
            'favourite_subject': matFav,
            'working_time': hora,
            'university_studies': uni,
            'learner': pk
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


$(document).ready(function () {
    $.ajax({
        type: 'GET',
        url: '/api/profile_info',
        data: {
            'learner': pk
        },
        success: function(data){
            $('#materia-fav').val(data.favourite_subject);
            $('#horario').val(data.working_time);
            $('#univ').val(data.university_studies);

        }
    })
});
