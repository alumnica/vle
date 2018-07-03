$(document).ready(function () {
    var finished = false;
    
    $('#evaluate').fullpage({
        verticalCentered: false,
        anchors: ['firstPage', 'secondPage', 'thirdPage', 'fourthPage', 'fifthPage', 'sixthPage', 'seventhPage', 'eighthPage', 'ninethPage', 'tenthPage', 'eleventhPage', 'twelvethPage'],
        menu: '#evalMenu',

        
 
    });




    $('.next').on('click', '.button', function () {
        $.fn.fullpage.moveSectionDown();
    });


    $('.end button').click(function(){
        let relationship_answers = document.getElementById('relationship').value;
        let multiple_option_answers = document.getElementById('multiple_option').value;
        let multiple_answer_answers = document.getElementById('multiple_answer').value;
        let numeric_answer_answers = document.getElementById('numeric_answer').value;
        let pulldown_list_answers = document.getElementById('pulldown_list').value;

        $.ajax({
            url: '/api/evaluation/',
            data: {evaluation: JSON.stringify(evaluation_object),
                   relationship_answers: relationship_answers,
                    multiple_option_answers: multiple_option_answers,
                    multiple_answer_answers: multiple_answer_answers,
                    numeric_answer_answers: numeric_answer_answers,
                    pulldown_list_answers: pulldown_list_answers,
                    pk: user_pk},
            success: function(data){
                let questions_array = JSON.parse(data.data);
                let score = data.score;
                $('.resultado').html(score);
                for (i = 0 ; i < questions_array.length ; i++){
                    $('.question[question-type]').each(function (){
                        var theQuestion = $(this);
                        var qType = $(this).attr('question-type'),
                            qPK = $(this).attr('pk'),
                            theTab = $(this).parent().find('.the-tab'),
                            theIcon = $(this).parent().find('.icon'),
                            answerText = $(this).parent().find('.the-answer-text p'),
                            dataAnchor = $(this).parent().attr('data-anchor');
                            
                            if(questions_array[i].type == qType && questions_array[i].pk == qPK){
                                if(questions_array[i].status == 'correct'){
                                    theTab.addClass('correct');
                                    theIcon.html('<i class="far fa-check-circle"></i>');
                                    $('#evalMenu li[data-menuanchor="'+dataAnchor+'"] a').css('color', 'green');
                                } else {
                                    theTab.addClass('incorrect');
                                    theIcon.html('<i class="far fa-times-circle"></i>');
                                    $('#evalMenu li[data-menuanchor="'+dataAnchor+'"] a').css('color', 'red');
                                }				
                                answerText.html(questions_array[i].description);
                            }
                    });
                }

                if (score >= 7){
                    for (let j = 0; j<data.suggestions.length; j++){
                        let suggestion = data.suggestions[j];
                        let rec_div = document.getElementById('suggestions');

                        $(rec_div).append("<a class='rec' id='rec'><div class='oda-image'><img src='"+suggestion.image+"' alt='\'></div><div class='oda-text'>"+suggestion.oda+"</div></a>");
                        $(rec_div).find('#rec').attr("href", gettext("/odas/"+suggestion.pk+"/"));


                    }
                }
            }
        });
        $('.answer-text').removeClass('is-hidden');
        $(this).parent().parent().remove();
        $('.the-score').fadeIn(500);
        $('input').prop('disabled', true);
        $('select').prop('disabled', true);
        $('.reset').remove();
    });

    var relAnswersLength = $('.question[question-type="relationship"]').length;
    var relMOAnswersLength = $('.question[question-type="multiple_option"]').length;
    var relMAAnswersLength = $('.question[question-type="multiple_answer"]').length;
    var relNAAnswersLength = $('.question[question-type="numeric_answer"]').length;
    var relAnswers = new Array(relAnswersLength);
    var relMOAnswers = new Array(relMOAnswersLength);
    var relMAAnswers = new Array(relMAAnswersLength);
    var relNAAnswers = new Array(relNAAnswersLength);
    var relPLAnswers = new Array();

    $('.question[question-type="relationship"]').each(function () {
        var dataAnchor = $(this).parent().attr('data-anchor');
        var thePk = $(this).attr('pk');
        var qIndex = $('.question[question-type="relationship"]').index(this);
        var colors = ["red", "orange", "yellow", "green", "blue", "purple"];
        var theQuest = $(this);
        var theAnswersLength = $(this).find(".left-side ul li").length;
        var theAnswers = new Array($(this).find(".left-side ul li").length);

        $(this).on("click", "li", function () {

            if(!theAnswers.includes(undefined)){
                $('#evalMenu li[data-menuanchor="'+dataAnchor+'"] a').html('<i class="fa fa-circle"></i>');

                theAnswers.unshift(thePk);
                relAnswers.splice(qIndex,1,theAnswers.join(';'));
                $('#relationship').val(relAnswers.join('|'));

                console.log(theAnswers);

            }

            var selected = $(this);

            if (selected.hasClass("ls")) {
                var indexLeft = theQuest.find(".left-side li").index(this);
                $(".ls").each(function () {
                    $(this).removeAttr("style");
                });

                selected.css("background-color", colors[0]);

                $(".right-side ul").selectable({
                    filter: "li.rs",
                    stop: function () {
                        var matched = $(".ui-selected", this);
                        var indexRight = '';
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
                var indexRight = theQuest.find(".right-side li").index(this);
                $(".rs").each(function () {
                    $(this).removeAttr("style");
                });


                selected.css("background-color", colors[0]);

                $(".left-side ul").selectable({
                    filter: "li.ls",
                    stop: function () {
                        var matched = $(".ui-selected", this);
                        var indexLeft = '';
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
            relAnswers.splice(qIndex,1,'');
            $('#relationship').val(relAnswers.join('|'));
            $('#evalMenu li[data-menuanchor="'+dataAnchor+'"] a').html('<i class="far fa-circle"></i>');
        });


    });

    $('.question[question-type="multiple_option"]').each(function () {
        var dataAnchor = $(this).parent().attr('data-anchor');
        var thePk = $(this).attr('pk');
        var qIndex = $('.question[question-type="multiple_option"]').index(this);
		var theAnswer = new Array(2);

		$( "input", this ).on( "click", function() {
			$('#evalMenu li[data-menuanchor="'+dataAnchor+'"] a').html('<i class="fa fa-circle"></i>');

            theAnswer.splice(1, 1, $(this).val());

            console.log(theAnswer);

			theAnswer.splice(0, 1, thePk);

            console.log(theAnswer);

            relMOAnswers.splice(qIndex,1,theAnswer.join(';'));
            $('#multiple_option').val(relMOAnswers.join('|'));



		});


    });

    $('.question[question-type="multiple_answer"').each(function () {
        var dataAnchor = $(this).parent().attr('data-anchor');
        var thePk = $(this).attr('pk');
        var qIndex = $('.question[question-type="multiple_answer"]').index(this);
        var theAnswer = new Array();
        var theQuest = $(this);

        $('input', this).on('click', function () {

            var allVals = [];
            theQuest.find(':checked').each(function() {
            allVals.push($(this).val());
            console.log(allVals);
            });
            allVals.unshift(thePk);
            // console.log(allVals);
            relMAAnswers.splice(qIndex,1,allVals.join(';'));
            $('#multiple_answer').val(relMAAnswers.join('|'));

            if ($('input', $(this).parent().parent()).is(':checked')) {
                $('#evalMenu li[data-menuanchor="' + dataAnchor + '"] a').html('<i class="fa fa-circle"></i>');
            } else if (!$('input', $(this).parent().parent()).is(':checked')) {
                $('#evalMenu li[data-menuanchor="' + dataAnchor + '"] a').html('<i class="far fa-circle"></i>');
            }
        });

    });

    $('.question[question-type="numeric_answer"').each(function () {
        var dataAnchor = $(this).parent().attr('data-anchor');
        var thePk = $(this).attr('pk');
        var qIndex = $('.question[question-type="numeric_answer"]').index(this);
        var theAnswer = [];

        $('input', this).change(function() {

            if ($(this).val()!="") {
                $('#evalMenu li[data-menuanchor="' + dataAnchor + '"] a').html('<i class="fa fa-circle"></i>');
                theAnswer = [];
                theAnswer.push($(this).val());
                theAnswer.unshift(thePk);
                relNAAnswers.splice(qIndex,1,theAnswer.join(';'));
                $('#numeric_answer').val(relNAAnswers.join('|'));
            } else {
                $('#evalMenu li[data-menuanchor="' + dataAnchor + '"] a').html('<i class="far fa-circle"></i>');
                theAnswer = [];
                // theAnswer.push($(this).val());
                // theAnswer.unshift(thePk);
                relNAAnswers.splice(qIndex,1,theAnswer.join(';'));
                $('#numeric_answer').val(relNAAnswers.join('|'));
            }


        });


    });

    $('.question[question-type="pulldown_list"').each(function (){
        var dataAnchor = $(this).parent().attr('data-anchor');
        var thePk = $(this).attr('pk');
        var qIndex = $('.question[question-type="pulldown_list"]').index(this);
        var theAnswersLength = $(this).find("select").length;
        var theAnswer = new Array(theAnswersLength);
        var theQuest = $(this);



        $('select', this).change(function(){

            var thisAnswer = [];
            var selIndex = theQuest.find("select").index(this);
            thisAnswer = ([selIndex, $(this).val()]);
            theAnswer.splice(selIndex, 1, thisAnswer);
            console.log(theAnswer);

            if(!theAnswer.includes(undefined)){
                $('#evalMenu li[data-menuanchor="'+dataAnchor+'"] a').html('<i class="fa fa-circle"></i>');

                // theAnswer.unshift(thePk);
                relPLAnswers.splice(qIndex,1,thePk +';'+theAnswer.join(';'));
                $('#pulldown_list').val(relPLAnswers.join('|'));

                console.log(theAnswer);
    
            }
        });

        

    });

    $('.question').each(function () {
        
        if ($(window).height() > 450) {

            var element = $(this)
            var dims = element.height();

            var parentHeight = element.parent().height();

            var newMargin = ((parentHeight - dims) / 3);
            // console.log(newMargin);
            element.css('padding-top', newMargin);
        }
    });
    window.onresize = resize;

    function resize() {
        $('.question').each(function () {

            var element = $(this)
            var dims = element.height();

            if ($(window).height() > 450) {

                var parentHeight = element.parent().height();

                var newMargin = ((parentHeight - dims) / 3);
                // console.log(newMargin);
                element.css('padding-top', newMargin);
            } else {
                element.css('padding-top', '0');
            }
        });

    }
    
});

$('.section').on('click', '.the-tab', function(){
    $(this).parent().toggleClass('closed1');
});

