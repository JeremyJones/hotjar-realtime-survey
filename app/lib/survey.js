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
			
			var target = "#tick4" + this.pt_id;
			$(target).html('<i class="fa fa-check"></i>');

			// successful answer posting (or in progress answer)
			// also sets the cookie:
			Cookies.set('mid', app.myIdentifier, {path:''}); // struct ok
		    }
		}});
    },
    
    "getQuestions": function() {
        $.ajax({
            'url': '/questions',
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

	if ("undefined" != typeof(existingId))
	    app.myIdentifier = existingId;
	else
	    $.ajax({'url': '/getIdentifier',
		    'method': 'POST',
		    'success': function (id) {
			app.myIdentifier = id;
		    }});
    },
    
    "drawScreen": function (questions=app.questions, targetDiv=app.config.targetDiv) {

	var screenquestions = [],
	    sliceStart = app.myIdentifier.que - 1
	sliceEnd = sliceStart + app.config.questionsPerScreen;
	
	screenquestions = questions.slice(sliceStart,sliceEnd);
	return app.renderQuestions(screenquestions, targetDiv);
    },

    "renderQuestion": function (question) {
	var html = '',
	    answerHTML = '',
	    answerTick = '<div style="display:inline" class="tick" id="tick4answer2question' + question.id + '"></div>',
	    addHandlers = null;

	if (question.answer_type.match(/^(?:text|email)$/)) {
	    answerHTML = '<input type="' + question.answer_type + '" ' +
		' class="form-control mAnswer" ' +
		' id="answer2question' + question.id + '" ' +
		(question.required == 'y' ? ' required="true" ' : '') +
		' /> ';

	    addHandlers = function () {
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
	
	var html = '<form class="form form-condensed">',
	    counter, toRender = [], handlers = [], h = null;

	for (counter = 0; counter < qs.length; ++counter) {
	    
	    toRender = app.renderQuestion(qs[counter]);
	    
	    html += toRender[0] + '<hr/>';

	    if (toRender[1])
		handlers.push(toRender[1]);
	}
	html += '</form>';
	
	target.html(html);

	if (handlers.length > 0)
	    for (h in handlers) handlers[h]();
	
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
