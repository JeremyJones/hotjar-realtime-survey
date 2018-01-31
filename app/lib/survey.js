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
		    app.log("Got questions");
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
	/*
	console.log("Drawing " + questions.length + " questions. Should be " +
		    "screen " + app.myIdentifier.scr);
	*/

	var screenquestions = [],
	sliceStart = ((app.myIdentifier.scr - 1) *
		      app.config.questionsPerScreen),
	sliceEnd = sliceStart + app.config.questionsPerScreen;
	
	screenquestions = questions.slice(sliceStart,sliceEnd);
	app.renderQuestions(screenquestions, targetDiv);
    },

    "renderQuestion": function (question) {
	var html = '',
	answerHTML = '';

	if (question.answer_type == 'text')
	    answerHTML = '<input type="text" class="form-control mAnswer" ' +
		' id="answer2question' + question.id + '" ' +
		(question.required == 'y' ? ' required="true" ' : '') +
		' /> ';
	else
	    answerHTML = '[' + question.answer_type + ' unimplemented]';
	
	html = '<div class="row input-group"><div class="col">' +
	'<label for="answer2question' + question.id + '" >' +
	question.question + ': ' +
	'</label>' + 
	'</div><div class="col">' +
	answerHTML + 
	'</div></div>';
	
	return html;
    },
    
    "renderQuestions": function (qs, target) {
	
	app.log("rendering " + qs[0].question + " and " + qs[1].question);

	var html = "",
	counter;

	for (counter = 0; counter < qs.length; ++counter) {
	    html += app.renderQuestion(qs[counter]);
	    html += '<hr/>';
	}
	target.html(html);
	$(".mAnswer").first().focus();
    },
    
    "log": function (msg) {
	console.log(msg);
    },

    "runLoop": function () {
	//app.log("Running");

	if (! (app.myIdentifier && app.questions)) {
	    app.log("Not ready yet");
	    app._readyFails += 1;
	    if (app._readyFails < 100)
		setTimeout(app.runLoop, 100);
	    return false;
	}
	app.log("Ok ready");
	app.drawScreen(app.questions);
    },
    
    "start": function () {
	app.log("Starting");
	app.getQuestions();
	app.setIdentifier();
	app.runLoop();
	//app.drawScreen();
    } // last
};

app.start();
