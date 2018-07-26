$(document).ready(function () {
    $('#test-end').on('click', function(){
        var testAnswers = [];
        $('#test-form li').each(function(){
           var liIndex = $('#test-form li').index(this);
           var answer = $("input:checked", this).val();
            testAnswers.splice(liIndex,1,answer);
        });
        $('#test-answers').val(testAnswers);
    });
});

function valid_form() {
    let answer = $('#test-answers').val().split(',');
    for (let i = 0; i<answer.length; i++){
        if (answer[i] == '' || answer[i] == ' '){
            swal("Error", gettext("Pelase answer all the questions before saving"), "error")
            return false;
        }
    }
}