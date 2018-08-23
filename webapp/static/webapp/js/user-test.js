$(document).ready(function () {
    $('#test-end').on('click', function () {
        let testAnswers = [];
        $('#test-form li').each(function () {
            let liIndex = $('#test-form li').index(this);
            let answer = $("input:checked", this).val();
            testAnswers.splice(liIndex, 1, answer);
        });
        $('#test-answers').val(testAnswers);
    });
});

function valid_form() {
    let answer = $('#test-answers').val().split(',');
    for (let i = 0; i < answer.length; i++) {
        if (answer[i] == '' || answer[i] == ' ') {
            swal("Error", "Contesta todas las preguntas antes de guardar", "error");
            return false;
        }
    }
}