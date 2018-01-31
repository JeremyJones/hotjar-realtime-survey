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
    "getQuestions": function() {
        $.ajax({
            'url': '/questions',
            'success': function(d) {
		    app.questions = d._items
            }
        });
    },

    "setIdentifier": function () {
	if (app.myIdentifier) return true;

	app.getIdentifier();
    },

    "getIdentifier": function () {
	
	var existingId = Cookies.get('mid');

	if ("undefined" != typeof(existingId))
	    app.myIdentifier = JSON.parse(existingId);
	else
	    $.ajax({'url': '/getIdentifier',
			'method': 'POST',
			'success': function (id) {
			app.myIdentifier = id;
			// answer posting should set the cookie:
			//Cookies.set('mid', JSON.stringify(id));
		    }});
    },
    
    "drawScreen": function (questions=app.questions, targetDiv=app.config.targetDiv) {

	var screenquestions = [],
	sliceStart = ((app.myIdentifier.scr - 1) *
		      app.config.questionsPerScreen),
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

		var mycall = function () { // my callback to be run on blur or keyup
				      $.ajax({'url': '/answer',
						  'param__id': $(this).attr('id'),
						  'method': 'POST',
						  'data': {"q": $(this).attr('id'),
						      "a": $(this).val(),
						      "who": app.myIdentifier.eui},
						  'processData': true,
						  'success': function (d) {
						  if (d.status && d.status == 'OK') {
						      var target = "#tick4" + this.param__id;
						      $(target).html('<i class="fa fa-check"></i>');
						  }
					      }});
		};

		$("#answer2question" + question.id).on("keyup", mycall);
		$("#answer2question" + question.id).on("blur", mycall);
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
