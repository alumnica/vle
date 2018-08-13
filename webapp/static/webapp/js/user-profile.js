$('#selected-avatar').val($('.avatar-main img').attr('id'));

$('.avatar-options').on('click', 'img', function () {
    var clicked = $(this);
    var main = $('.avatar-main img');
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