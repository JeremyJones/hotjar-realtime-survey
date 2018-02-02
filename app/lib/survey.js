var newapp = angular.module("survey", []);

newapp.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{ng ');
    $interpolateProvider.endSymbol(' ng}');
}]);

//

var app = {

    "config": {"questionsPerScreen": 2,
	       "targetDiv": $("#surveySays")},
    
    //
    "screen": null,
    "questions": null,
    "myIdentifier": null,
    "_readyFails": 0,
    //
    "lastAnswers": {},
    //
    "sendAnswer": function () { // my callback to be run on input change
	var my_val = null,
	    my_id = null;

	if ($(this).attr('type') == 'checkbox') { // checkboxes are special
	    my_id = $(this).attr('name');

	    var miniPostAnswer = function (data, async=true) {
		$.ajax({'url':'/answer',
			'method': 'POST',
 			'data': data,
			'processData': true,
			'async': async});
	    };
	    
	    miniPostAnswer({"q": my_id,
			    "z": 'delete',
			    "who": app.myIdentifier.eui}, false);

	    $("input[type=checkbox][name=" + my_id + "]:checked").each(
		function () {
		    var value = $(this).attr('value');
		    app.log("Sending val " + value);
		    miniPostAnswer({"q": my_id,    "a": value,
				       "who": app.myIdentifier.eui});
		   });
	    
	    return;
	}	
	else if ($(this).attr('type') == 'radio') { // radios don't use html id
	    my_id = $(this).attr('name');
	    my_val= $(this).val();
	}
	else {
	    my_id = $(this).attr('id');
	    my_val= $(this).val();
	}
	
	// don't send empty answers when the page is first loaded
	if (my_val === "" && "undefined" == typeof(app.lastAnswers[my_id]))
	    return false;
	
	// don't send answers which are the same as what's already been saved
	if ("undefined" != typeof(app.lastAnswers[my_id]))
	    if (my_val == app.lastAnswers[my_id]['value'])
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
			
			app.lastAnswers[this.pt_id] = {'value': this.pt_val,
						       'validated': false };
			
			// feedback for successful answers
			if (d.validAnswer) {
			    var target = "#tick4" + this.pt_id;
			    $('i.fa', target).addClass('fa-check');
			    app.lastAnswers[this.pt_id]['validated'] = true;
			}

			// any successful answer posting (or in progress answer)
			// also sets the cookie so you're in a current session:
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

    "showNumSteps": function () {
	if (! app.questions) return;
	//app.log("showing");
	
	$("#numberOfSteps").text((app.questions.length / app.config.questionsPerScreen))
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
	targetDiv.html("Thank you. The survey is now complete. " +
		       '<div><a href="/" class="btn btn-primary">' +
		       'Finish</a></div>');
    },

    "finalise": function () {
	$.ajax({url:'/finalise',
		data: {"who":app.myIdentifier.eui},
		async: false,
		method: 'POST',
		success: function (d) {
		    Cookies.remove('mid', {path:''});
		    app.drawThankyou();
		}});
    },
    
    "setScreen": function (s) {  // set the app.current_screen variable
	app.current_screen = s;
    },

    "getCurrentQuestions": function () {  // returns a list of the current questions to display
	var screenquestions = [],
	    sliceStart = parseInt(app.myIdentifier["que"]) - 1,
	sliceEnd = sliceStart + app.config.questionsPerScreen;

	app.setScreen((sliceStart / app.config.questionsPerScreen) + 1);
	
	return app.questions.slice(sliceStart,sliceEnd);
    },
    
    "drawScreen": function () {

	var screenquestions = app.getCurrentQuestions();

	return app.renderQuestions(screenquestions, app.config.targetDiv);
    },

    "canGoBack": function () {  // tell the caller if we can go 'back'
	//return(app.getCurrentQuestions()[0].id == app.questions[0].id);
	return(false || (app.current_screen > 1));
    },

    "canGoFwd": function () {  // we can go forward if all the 'required' questions on the screen are valid
	var allAnswersValid = _.every(app.getCurrentQuestions(),
				      function (q) {
					  var lastAnswerKey = "answer2question" + q.id;
					  return(("undefined" != typeof(app.lastAnswers[lastAnswerKey]))
						 &&
						 app.lastAnswers[lastAnswerKey]['validated']);
				      });

	return true;  // dev
	
	if (! allAnswersValid) {
	    alert('Please answer all required fields.');
	    return false;
	} else {
	    return true;
	}
    },
    
    "renderQuestion": function (question) {
	var html = '',
	    answerHTML = '',
	    answerTick = ('<div style="display:inline" class="tick" id="tick4answer2question'
			  + question.id + '"><i class="fa fa-block"></i></div>'),
	    postRenderCallback = null;

	if (question.answer_type.match(/^(?:text(?:area)?|email)$/)) {

	    if (question.answer_type === 'textarea') {
		answerHTML = '<textarea class="form-control mAnswer" ' +
		    ' id="answer2question' + question.id + '"></textarea>';
	    } else {
		answerHTML = '<input type="' + question.answer_type + '" ' +
		    ' class="form-control mAnswer" ' +
		    ' value="" ' +
		    ' id="answer2question' + question.id + '" ' +
		    (question.required == 'y' ? ' required="true" ' : '') +
		    ' /> ';
	    }

	    postRenderCallback = function () {

		var lastAnswerKey = "answer2question" + question.id;
		if ("undefined" != typeof(app.lastAnswers[lastAnswerKey]))
		    $("#answer2question" + question.id).val(app.lastAnswers[lastAnswerKey]['value']);
		
		$("#answer2question" + question.id).on("keyup", app.sendAnswer);
		$("#answer2question" + question.id).on("blur", app.sendAnswer);
	    };
	}
	else if (question.answer_type == 'select') {
	    answerHTML = '<select id="answer2question' + question.id + '" ' +
	    ' class="form-control mAnswer" ' +
	    ' ><option>Please select</option>';

	    var answerOptions = [];
	    
	    _.each(JSON.parse(question.answer_options),
		   function (o) {
		       var so = new String(o);
		       //app.log("adding option " + so);
		       answerOptions.push('<option value="' + so + '">' +
					  so + '</option>')
		   });

	    answerHTML += answerOptions.join("\n");
	    answerHTML += '</select>';

	    postRenderCallback = function () {
		var lastAnswerKey = "answer2question" + question.id;
		if ("undefined" != typeof(app.lastAnswers[lastAnswerKey]))
		    $("#answer2question" + question.id).val(app.lastAnswers[lastAnswerKey]['value']);

		$("#answer2question" + question.id).on("change", app.sendAnswer);
	    };
	}
	else if (question.answer_type == 'radio' || question.answer_type == 'checkbox') {
	    answerHTML = '<div class="form-group">';
	    var theseoptions = [];

	    _.each(JSON.parse(question.answer_options),
		   function (o) {
		       var tnow = new Date(),
			   mmid = ("" + tnow.valueOf()).substring(-4) + "a2q" + question.id;

		       theseoptions.push('<div class="form-check"><input type="' +
					 question.answer_type + '" ' +
					 ' id="' + mmid + '" ' +
					 ' class="form-check-input" name="answer2question' + question.id +
					 '" value="' + o + '" /><label class="form-check-label"' +
					 ' for="' + mmid + '">' + o + '</label></div>');
		   });

	    if (theseoptions.length < 5)
		answerHTML += theseoptions.join("\n");
	    else {
		var sliceat = parseInt(theseoptions.length/2);

		answerHTML += '<table class="table table-condensed"><tr>' +
		    '<td>' + theseoptions.slice(0,sliceat).join("\n") +
		    '</td><td>' + theseoptions.slice(sliceat+1,theseoptions.length).join("\n") +
		    '</td></tr></table>';
	    }
	    
	    answerHTML += '</div>';

	    postRenderCallback = function () {
		var selector = 'input:' + question.answer_type +
		    '[name="answer2question' + question.id + '"]';
		
		$(selector).on("click", app.sendAnswer);
	    };
	}
	else {
	    answerHTML = '[' + question.answer_type + ' unimplemented]';
	}
	
	html = '<div xstyle="border-width:1px; border-style:solid; border-color:black" class="row input-group"><div class="col">' +
	    '<label for="answer2question' + question.id + '" >' +
	    question.question + ':' + 
	    (question.required == 'y'
	     ? '<sup><small class="danger"><i class="fa fa-asterisk" title="required"></i></small></sup>'
	     : '') +
	    ' ' +
	    '</label>' + 
	    '</div>' +
	    '<div class="col">' + answerHTML + '</div><div class="col">' + answerTick + '</div>' +
	    '</div>';
	
	return [html, postRenderCallback];
    },

    "renderQuestions": function (qs, target) {
	
	var html = '<form id="mForm" class="form form-condensed">',
	    handlers = [], tmp = null;

	html += '<div style="min-height: 150px">';
	
	_.each(qs, function (thisQuestion) {
		var toRender = app.renderQuestion(thisQuestion);
		html += toRender[0] + '<hr/>';

		if (toRender[1])
		    handlers.push(toRender[1]);
	});

	html += '</div>';

	// add back & next buttons
	html += '<nav aria-label="backnext"><ul class="pagination d-flex justify-content-center">' + 
	'<li id=liback class="page-item"><a class="page-link backnext" id="backButton" ' +
	' href="#" tabindex="-1"><i class="fa fa-arrow-left"></i> Previous</a> ' + 
	    '</li>' +
	    '<li class="page-item"><a class="page-link bnstep" href="#" disabled="true" ' +
	    ' tabindex="-1" style="text-decoration:none" ' +
	    ' onclick="return false"><font color="#333">Step ' +
	    app.current_screen + ' of ' +
	    '<span id="numberOfSteps"></span></font></a></li>' +
	'<li class="page-item"><a class="page-link backnext" id="nextButton" ' +
	' href="#">Next <i class="fa fa-arrow-right"></i></a> ' + 
	'</li></ul></nav>';

	handlers.push(app.showNumSteps);;
	
	html += '</form>';

	handlers.push(function () {
	    $(".backnext").on('click',
			      function () {
				  if ($(this).attr('id') == 'nextButton') {
				      if (! app.canGoFwd()) return false;

				      app.myIdentifier.que += app.config.questionsPerScreen;
				  }
				  else {
				      if (! app.canGoBack()) return false;
				      
				      app.myIdentifier.que -= app.config.questionsPerScreen;
				  }
				  
				  if (app.myIdentifier.que > app.questions.length)
				      app.finalise();
				  else 
				      app.drawScreen();
				  
				  return false;
			      });
	});

	// if the back button is inactive then also make it appear disabled
	if (! app.canGoBack()) 
	    handlers.push(function () {
		    $("#backButton").attr('disabled',true).addClass('btn-disabled');
		    $("#liback").addClass('disabled');
		});
	
	target.html(html);

	_.each(handlers, function (handler) {
		handler();
	    });
	
	$(".mAnswer").first().focus();
    },
    
    "log": function (msg) {
	return; // default
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
	return app.drawScreen();
    },
    
    "start": function () {
	app.getQuestions();
	app.setIdentifier();
	app.runLoop();
    } // last
};

app.start();
