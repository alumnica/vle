$(document).ready(function () {
    var finished = false;
    
    $('#evaluate').fullpage({
        verticalCentered: false,
        anchors: ['firstPage', 'secondPage', 'thirdPage', 'fourthPage', 'fifthPage', 'sixthPage', 'seventhPage', 'eighthPage', 'ninethPage', 'tenthPage', 'eleventhPage', 'twelvethPage'],
        menu: '#evalMenu',

        afterLoad: function(anchorLink, index){
            var loadedSection = $(this);
    
            if(anchorLink == 'eleventhPage' && finished ==false){
                $.fn.fullpage.setAllowScrolling(false, 'down');
            } else if (anchorLink != 'eleventhPage' && finished == false) {
                $.fn.fullpage.setAllowScrolling(true);
            } else {
                $.fn.fullpage.setAllowScrolling(true);
            }
        }
 
    });

    // $.fn.fullpage.setAllowScrolling(false, 'down');
    // $.fn.fullpage.setKeyboardScrolling(false);

    $('.next').on('click', '.button', function () {
        $.fn.fullpage.moveSectionDown();
    });
    $('.reveal').on('click', '#end-eval', function () {
       finished = true;
       $.fn.fullpage.moveSectionDown();
       $('#score').attr('href', '#twelvethPage');
    });

    var relAnswersLength = $('.question[question-type="relationship"]').length;
    var relMOAnswersLength = $('.question[question-type="multiple_option"]').length;
    var relMAAnswersLength = $('.question[question-type="multiple_option"]').length;
    var relAnswers = new Array(relAnswersLength);
    var relMOAnswers = new Array(relMOAnswersLength);
    var relMAAnswers = new Array(relMAAnswersLength);
    var relNAAnswers = new Array();
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
                     
                        
                        
                    }
                });
            }

        });

        


        //reset all

        $(".reset").click(function () {
            colors = ["red", "orange", "yellow", "green", "blue", "purple"];            
            theAnswers = new Array(theQuest.find(".left-side ul li").length);
         
        
            $(".left-side li").each(function () {
                $(this).removeClass("ls");
                $(this).addClass("ls");
                $(this).removeAttr("style");
            });
            $(".right-side li").each(function () {
                $(this).removeClass("rs");
                $(this).addClass("rs");
                $(this).removeAttr("style");
            });
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
			theAnswer.splice(0, 1, thePk);		
            relMOAnswers.splice(qIndex,1,theAnswer.join(';'));
            $('#multiple_option').val(relMOAnswers.join('|'));

		});
				
    });

    $('.question[question-type="multiple_answers"').each(function () {
        var dataAnchor = $(this).parent().attr('data-anchor');
        var thePk = $(this).attr('pk');
        var qIndex = $('.question[question-type="multiple_answer"]').index(this);
        var theAnswer = new Array();
        var theQuest = $(this);

        $('input', this).on('click', function () {

            var allVals = [];
            theQuest.find(':checked').each(function() {
            allVals.push($(this).val());
            
            });
            allVals.unshift(thePk);
            
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
            

            if(!theAnswer.includes(undefined)){
                $('#evalMenu li[data-menuanchor="'+dataAnchor+'"] a').html('<i class="fa fa-circle"></i>');
                
                theAnswer.unshift(thePk);
                relPLAnswers.splice(qIndex,1,theAnswer.join(';'));
                $('#pulldown_list').val(relPLAnswers.join('|'));
    
                
    
            }
        });

        

    });
    
});

