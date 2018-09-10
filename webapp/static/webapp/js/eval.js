$(document).ready(function () {

    $('#evaluate').fullpage({
        verticalCentered: false,
        anchors: ['firstPage', 'secondPage', 'thirdPage', 'fourthPage', 'fifthPage', 'sixthPage', 'seventhPage', 'eighthPage', 'ninethPage', 'tenthPage', 'eleventhPage', 'twelvethPage'],
        menu: '#evalMenu',


    });


    $('.next').on('click', '.button', function () {
        $.fn.fullpage.moveSectionDown();
    });


    $('.end button').click(function () {
        let relationship_answers = document.getElementById('relationship').value;
        let multiple_option_answers = document.getElementById('multiple_option').value;
        let multiple_answer_answers = document.getElementById('multiple_answer').value;
        let numeric_answer_answers = document.getElementById('numeric_answer').value;
        let pulldown_list_answers = document.getElementById('pulldown_list').value;

        let timeSpentOnPage = TimeMe.getTimeOnCurrentPageInSeconds();
        let duration = timeSpentOnPage.toString().slice(0, -1);
        duration = `PT${duration}S`;
        console.log(duration);


        $.ajax({
            url: '/api/evaluation/',
            method: 'POST',
            type: 'POST',
            data: {
                evaluation: JSON.stringify(evaluation_object),
                relationship_answers: relationship_answers,
                multiple_option_answers: multiple_option_answers,
                multiple_answer_answers: multiple_answer_answers,
                numeric_answer_answers: numeric_answer_answers,
                pulldown_list_answers: pulldown_list_answers,
                pk: user_pk,
                duration: duration
            },
            success: function (data) {
                let questions_array = JSON.parse(data.data);
                let score = data.score;
                let theSugg = data.suggestions;
                $('.resultado').html(score);
                $('.the-score').fadeIn(500);


                for (let i = 0; i < questions_array.length; i++) {
                    $('.question[question-type]').each(function () {
                        let theQuestion = $(this);
                        let qType = $(this).attr('question-type'),
                            qPK = $(this).attr('pk'),
                            theTab = $(this).parent().find('.the-tab'),
                            theIcon = $(this).parent().find('.icon'),
                            answerText = $(this).parent().find('.the-answer-text p'),
                            dataAnchor = $(this).parent().attr('data-anchor');

                        if (questions_array[i].type == qType && questions_array[i].pk == qPK) {
                            if (questions_array[i].status == 'correct') {
                                theTab.addClass('correct');
                                theIcon.html('<i class="far fa-check-circle"></i>');
                                $('#evalMenu li[data-menuanchor="' + dataAnchor + '"] a').css('color', 'green');
                            } else {
                                theTab.addClass('incorrect');
                                theIcon.html('<i class="far fa-times-circle"></i>');
                                $('#evalMenu li[data-menuanchor="' + dataAnchor + '"] a').css('color', 'red');
                            }
                            answerText.html(questions_array[i].description);
                        }
                    });
                }

                if (score >= 7) {
                    $('.the-xp').append('+ 100');
                    for (let j = 0; j < 2; j++) {
                        let suggestion = data.suggestions[j];
                        let rec_div = document.getElementById('suggestions');

                        $(rec_div).append("<a class='rec' id='rec'><div class='oda-image'><img src='" + suggestion.image + "' alt='\'></div><div class='oda-text'>" + suggestion.oda + "</div></a>");
                        $(rec_div).find('#rec').attr("href", "/odas/" + suggestion.pk + "/");


                    }
                } else if (score <= 6) {
                    $('.the-xp').append('+ 0');
                    for (let h = 0; h <= 2; h++) {
                        let suggestion = data.suggestions[h];
                        let rec_div = document.getElementById('suggestions');
                        if (suggestion.uoda == "exemplification") {
                            $(rec_div).append("<a class='rec' id='rec'><div class='oda-image'><img src='/static/webapp/media/uODAs/iconos/sens.png' alt='Ejemplificacion'></div><div class='oda-text'>Ejemplificación</div></a>")

                        } else if (suggestion.uoda == "formalization") {
                            $(rec_div).append("<a class='rec' id='rec'><div class='oda-image'><img src='/static/webapp/media/uODAs/iconos/forma.png' alt='Formalizacion'></div><div class='oda-text'>Formalización</div></a>")
                        } else if (suggestion.uoda == "application") {
                            $(rec_div).append("<a class='rec' id='rec'><div class='oda-image'><img src='/static/webapp/media/uODAs/iconos/apli.png' alt='Aplicacion'></div><div class='oda-text'>Aplicación</div></a>")
                        } else if (suggestion.uoda == "sensitization") {
                            $(rec_div).append("<a class='rec' id='rec'><div class='oda-image'><img src='/static/webapp/media/uODAs/iconos/sens.png' alt='Sensibilizacion'></div><div class='oda-text'>Sensibilzación</div></a>")
                        } else if (suggestion.uoda == "activation") {
                            $(rec_div).append("<a class='rec' id='rec'><div class='oda-image'><img src='/static/webapp/media/uODAs/iconos/activ.png' alt='Activacion'></div><div class='oda-text'>Activación</div></a>")
                        }
                        $(rec_div).find('#rec').attr("href", "/moments/" + suggestion.pk + "/");
                    }
                }
            }
        });
        $('.answer-text').removeClass('is-hidden');
        $(this).parent().parent().remove();

        $('#evaluate input').prop('disabled', true);
        $('select').prop('disabled', true);
        $('.reset').remove();
    });

    let relAnswersLength = $('.question[question-type="relationship"]').length;
    let relMOAnswersLength = $('.question[question-type="multiple_option"]').length;
    let relMAAnswersLength = $('.question[question-type="multiple_answer"]').length;
    let relNAAnswersLength = $('.question[question-type="numeric_answer"]').length;
    let relAnswers = new Array(relAnswersLength);
    let relMOAnswers = new Array(relMOAnswersLength);
    let relMAAnswers = new Array(relMAAnswersLength);
    let relNAAnswers = new Array(relNAAnswersLength);
    let relPLAnswers = new Array();

    $('.question[question-type="relationship"]').each(function () {
        let dataAnchor = $(this).parent().attr('data-anchor');
        let thePk = $(this).attr('pk');
        let qIndex = $('.question[question-type="relationship"]').index(this);
        let colors = ["red", "orange", "yellow", "green", "blue", "purple"];
        let theQuest = $(this);
        let theAnswersLength = $(this).find(".left-side ul li").length;
        let theAnswers = new Array($(this).find(".left-side ul li").length);

        $(this).on("click", "li", function () {

            if (!theAnswers.includes(undefined)) {
                $('#evalMenu li[data-menuanchor="' + dataAnchor + '"] a').html('<i class="fa fa-circle"></i>');

                theAnswers.unshift(thePk);
                relAnswers.splice(qIndex, 1, theAnswers.join(';'));
                $('#relationship').val(relAnswers.join('|'));

                console.log(theAnswers);

            }

            let selected = $(this);

            if (selected.hasClass("ls")) {
                let indexLeft = theQuest.find(".left-side li").index(this);
                $(".ls").each(function () {
                    $(this).removeAttr("style");
                });

                selected.css("background-color", colors[0]);

                $(".right-side ul").selectable({
                    filter: "li.rs",
                    stop: function () {
                        let matched = $(".ui-selected", this);
                        let indexRight = '';
                        matched.css("background-color", colors[0]);
                        matched.each(function () {
                            indexRight = theQuest.find(".right-side li").index(this);
                        });
                        selected.attr("pair", indexRight);
                        matched.attr("pair", indexLeft);

                        $(".right-side ul").selectable("destroy");
                        colors.splice(0, 1);
                        matched.toggleClass("rs").addClass("selected");
                        selected.removeClass("ls").addClass("selected");

                        theAnswers.splice(indexLeft, 1, [indexLeft, indexRight]);
                        console.log(theAnswers);


                    }
                });
            } else if (selected.hasClass("rs")) {
                let indexRight = theQuest.find(".right-side li").index(this);
                $(".rs").each(function () {
                    $(this).removeAttr("style");
                });


                selected.css("background-color", colors[0]);

                $(".left-side ul").selectable({
                    filter: "li.ls",
                    stop: function () {
                        let matched = $(".ui-selected", this);
                        let indexLeft = '';
                        matched.css("background-color", colors[0]);
                        matched.each(function () {
                            indexLeft = theQuest.find(".left-side li").index(this);
                        });
                        selected.attr("pair", indexRight);
                        matched.attr("pair", indexLeft);

                        $(".left-side ul").selectable("destroy");
                        colors.splice(0, 1);
                        matched.toggleClass("ls").addClass("selected");
                        selected.removeClass("rs").addClass("selected");

                        theAnswers.splice(indexLeft, 1, [indexLeft, indexRight]);
                        console.log(theAnswers);


                    }
                });
            }

        });


        //reset all

        theQuest.find(".reset").click(function () {
            colors = ["red", "orange", "yellow", "green", "blue", "purple"];
            theAnswers = new Array(theQuest.find(".left-side ul li").length);
            console.log(theAnswers);
            console.log(colors);
            theQuest.find(".left-side li").each(function () {
                $(this).removeClass("ls");
                $(this).addClass("ls");
                $(this).removeAttr("style");
            });
            theQuest.find(".right-side li").each(function () {
                $(this).removeClass("rs");
                $(this).addClass("rs");
                $(this).removeAttr("style");
            });
            relAnswers.splice(qIndex, 1, '');
            $('#relationship').val(relAnswers.join('|'));
            $('#evalMenu li[data-menuanchor="' + dataAnchor + '"] a').html('<i class="far fa-circle"></i>');
        });


    });

    $('.question[question-type="multiple_option"]').each(function () {
        let dataAnchor = $(this).parent().attr('data-anchor');
        let thePk = $(this).attr('pk');
        let qIndex = $('.question[question-type="multiple_option"]').index(this);
        let theAnswer = new Array(2);

        $("input", this).on("click", function () {
            $('#evalMenu li[data-menuanchor="' + dataAnchor + '"] a').html('<i class="fa fa-circle"></i>');

            theAnswer.splice(1, 1, $(this).val());

            console.log(theAnswer);

            theAnswer.splice(0, 1, thePk);

            console.log(theAnswer);

            relMOAnswers.splice(qIndex, 1, theAnswer.join(';'));
            $('#multiple_option').val(relMOAnswers.join('|'));


        });


    });

    $('.question[question-type="multiple_answer"]').each(function () {
        let dataAnchor = $(this).parent().attr('data-anchor');
        let thePk = $(this).attr('pk');
        let qIndex = $('.question[question-type="multiple_answer"]').index(this);
        let theAnswer = new Array();
        let theQuest = $(this);

        $('input', this).on('click', function () {

            let allVals = [];
            theQuest.find(':checked').each(function () {
                allVals.push($(this).val());
                console.log(allVals);
            });
            allVals.unshift(thePk);
            // console.log(allVals);
            relMAAnswers.splice(qIndex, 1, allVals.join(';'));
            $('#multiple_answer').val(relMAAnswers.join('|'));

            if ($('input', $(this).parent().parent()).is(':checked')) {
                $('#evalMenu li[data-menuanchor="' + dataAnchor + '"] a').html('<i class="fa fa-circle"></i>');
            } else if (!$('input', $(this).parent().parent()).is(':checked')) {
                $('#evalMenu li[data-menuanchor="' + dataAnchor + '"] a').html('<i class="far fa-circle"></i>');
            }
        });

    });

    $('.question[question-type="numeric_answer"]').each(function () {
        let dataAnchor = $(this).parent().attr('data-anchor');
        let thePk = $(this).attr('pk');
        let qIndex = $('.question[question-type="numeric_answer"]').index(this);
        let theAnswer = [];

        $('input', this).change(function () {

            if ($(this).val() != "") {
                $('#evalMenu li[data-menuanchor="' + dataAnchor + '"] a').html('<i class="fa fa-circle"></i>');
                theAnswer = [];
                theAnswer.push($(this).val());
                theAnswer.unshift(thePk);
                relNAAnswers.splice(qIndex, 1, theAnswer.join(';'));
                $('#numeric_answer').val(relNAAnswers.join('|'));
            } else {
                $('#evalMenu li[data-menuanchor="' + dataAnchor + '"] a').html('<i class="far fa-circle"></i>');
                theAnswer = [];
                // theAnswer.push($(this).val());
                // theAnswer.unshift(thePk);
                relNAAnswers.splice(qIndex, 1, theAnswer.join(';'));
                $('#numeric_answer').val(relNAAnswers.join('|'));
            }


        });


    });

    $('.question[question-type="pulldown_list"]').each(function () {
        let dataAnchor = $(this).parent().attr('data-anchor');
        let thePk = $(this).attr('pk');
        let qIndex = $('.question[question-type="pulldown_list"]').index(this);
        let theAnswersLength = $(this).find("select").length;
        let theAnswer = new Array(theAnswersLength);
        let theQuest = $(this);


        $('select', this).change(function () {

            let thisAnswer = [];
            let selIndex = theQuest.find("select").index(this);
            thisAnswer = ([selIndex, $(this).val()]);
            theAnswer.splice(selIndex, 1, thisAnswer);
            console.log(theAnswer);

            if (!theAnswer.includes(undefined)) {
                $('#evalMenu li[data-menuanchor="' + dataAnchor + '"] a').html('<i class="fa fa-circle"></i>');

                // theAnswer.unshift(thePk);
                relPLAnswers.splice(qIndex, 1, thePk + ';' + theAnswer.join(';'));
                $('#pulldown_list').val(relPLAnswers.join('|'));

                console.log(theAnswer);

            }
        });


    });

    $('.question').each(function () {

        if ($(window).height() > 450) {

            let element = $(this);
            let dims = element.height();

            let parentHeight = element.parent().height();

            let newMargin = ((parentHeight - dims) / 3);
            // console.log(newMargin);
            element.css('padding-top', newMargin);
        }
    });
    window.onresize = resize;

    function resize() {
        $('.question').each(function () {

            let element = $(this);
            let dims = element.height();

            if ($(window).height() > 450) {

                let parentHeight = element.parent().height();

                let newMargin = ((parentHeight - dims) / 3);
                // console.log(newMargin);
                element.css('padding-top', newMargin);
            } else {
                element.css('padding-top', '0');
            }
        });

    }

});

$('.section').on('click', '.the-tab', function () {
    $(this).parent().toggleClass('closed1');
});




