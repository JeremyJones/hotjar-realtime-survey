var newapp = angular.module("survey", []);

newapp.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{ng ');
    $interpolateProvider.endSymbol(' ng}');
}]);


//


var app = {

    /*

     */

    "config": {"questionsPerScreen": 2,
	       "targetDiv": $("#surveySays")},
    
    //
    "questions": null,
    "myIdentifier": null,
    "_readyFails": 0,
    //
    //
    "lastAnswers": {},
    //
    //

    "sendAnswer": function () { // my callback to be run on blur or keyup
	var my_val = $(this).val(),
	    my_id = $(this).attr('id');

	// don't send empty answers when the page is first loaded
	if (my_val === "" && "undefined" == typeof(app.lastAnswers[my_id]))
	    return false;
	
	// don't send answers which are the same as what's already been saved
	if ("undefined" != typeof(app.lastAnswers[my_id]))
	    if (my_val == app.lastAnswers[my_id])
		return false;
	
	$.ajax({'url': '/answer',
		'method': 'POST',
		'data': {
		    "q": my_id,
		    "a": my_val,
		    "who": app.myIdentifier.eui
		},
		'processData': true,
		// passthrough data for the callback function:
		'pt_id': my_id,
		'pt_val': my_val,
		//
		'success': function (d) {
		    if (d.status && d.status == 'OK' && this.pt_val) {
			
			app.lastAnswers[this.pt_id] = this.pt_val;
			
			// feedback for successful answers
			if (d.validAnswer) {
			    var target = "#tick4" + this.pt_id;
			    $(target).html('<i class="fa fa-check"></i>');
			}

			// successful answer posting (or in progress answer)
			// also sets the cookie:
			Cookies.set('mid', app.myIdentifier, {path:''}); // struct ok
		    }
		}});
    },
    
    "getQuestions": function() {
        $.ajax({
            'url': '/questions',
	    'method': 'POST',
            'success': function(d) {
		app.questions = d._items;
	    }});
    },

    "setIdentifier": function () {
	if (app.myIdentifier) return true;

	app.getIdentifier();
    },

    "getIdentifier": function () {
	
	var existingId = Cookies.get('mid');

	if ("undefined" == typeof(existingId)) { // new session
	    $.ajax({'url': '/getIdentifier',
		    'method': 'POST',
		    'success': function (id) {
			app.myIdentifier = id;
		    }});
	}
	else { // cookie-d user
	    if ("string" == typeof(existingId))
		existingId = JSON.parse(existingId);
	    
	    app.myIdentifier = existingId;
	}
    },

    "drawThankyou": function (targetDiv=app.config.targetDiv) {
	targetDiv.html("Thank you. The survey is now complete.");
    },
    
    "drawScreen": function (questions=app.questions, targetDiv=app.config.targetDiv) {

	var screenquestions = [],
	    sliceStart = parseInt(app.myIdentifier["que"]) - 1,
	sliceEnd = sliceStart + app.config.questionsPerScreen;

	screenquestions = questions.slice(sliceStart,sliceEnd);

	return app.renderQuestions(screenquestions, targetDiv);
    },

    "renderQuestion": function (question) {
	var html = '',
	    answerHTML = '',
	    answerTick = ('<div style="display:inline" class="tick" id="tick4answer2question'
			  + question.id + '"></div>'),
	    addHandlers = null;

	if (question.answer_type.match(/^(?:text|email)$/)) {
	    answerHTML = '<input type="' + question.answer_type + '" ' +
		' class="form-control mAnswer" ' +
		' value="" ' +
		' id="answer2question' + question.id + '" ' +
		(question.required == 'y' ? ' required="true" ' : '') +
		' /> ';

	    addHandlers = function () {

		var lastAnswerKey = "answer2question" + question.id;
		if ("undefined" != typeof(app.lastAnswers[lastAnswerKey]))
		    $("#answer2question" + question.id).val(app.lastAnswers[lastAnswerKey]);
		
		$("#answer2question" + question.id).on("keyup", app.sendAnswer);
		$("#answer2question" + question.id).on("blur", app.sendAnswer);
	    };
	}
	else {
	    answerHTML = '[' + question.answer_type + ' unimplemented]';
	}
	
	html = '<div class="row input-group"><div class="col">' +
	    '<label for="answer2question' + question.id + '" >' +
	    question.question + ': ' +
	    '</label>' + 
	    '</div><div class="col">' +
	    answerHTML + answerTick + 
	    '</div></div>';
	
	return [html, addHandlers];
    },

    "renderQuestions": function (qs, target) {
	
	var html = '<form id="mForm" class="form form-condensed">',
	    handlers = [], tmp = null;

	_.each(qs, function (thisQuestion) {
		var toRender = app.renderQuestion(thisQuestion);
		html += toRender[0] + '<hr/>';

		if (toRender[1])
		    handlers.push(toRender[1]);
	    });

	// add back & next buttons
	html += '<a href="#" class="backnext btn btn-secondary btn-block" id="backButton">' +
	    '<i class="fa fa-arrow-left"></i> Previous</a> ' +
	    '&nbsp;' +
	    '<a href="#" class="backnext btn btn-primary btn-block" id="nextButton">' +
	    'Next <i class="fa fa-arrow-right"></i></a>';
	
	html += '</form>';

	handlers.push(function () {
	    $(".backnext").on('click',
			      function () {
				  if ($(this).attr('id') == 'nextButton') {
				      // need to verify that any 'required' or 'requiredUnique'
				      // questions have been correctly-answered.
				      app.myIdentifier.que += app.config.questionsPerScreen;
				  }
				  else {
				      app.myIdentifier.que -= app.config.questionsPerScreen;
				  }
				  
				  if (app.myIdentifier.que > app.questions.length)
				      app.drawThankyou();
				  else 
				      app.drawScreen();
				  
				  return false;
			      });
	});
	
	target.html(html);

	if (handlers.length > 0)
	    for (tmp in handlers) handlers[tmp]();
	
	$(".mAnswer").first().focus();
    },
    
    "log": function (msg) {
	console.log(msg);
    },

    "runLoop": function () {
	if (! (app.myIdentifier && app.questions)) {
	    app._readyFails += 1;
	    if (app._readyFails < 100)
		setTimeout(app.runLoop, 100);
	    return false;
	}
	return app.drawScreen(app.questions);
    },
    
    "start": function () {
	app.getQuestions();
	app.setIdentifier();
	app.runLoop();
    } // last
};

app.start();
