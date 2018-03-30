// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// this is used to obtaine the search results from the API
// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


// search query being obtained

function getParameterByName(name, url) {
    if (!url) {
      url = window.location.href;
    }
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}



//this whole part is done for the search results only.

// Start

// $(document.body).on("click", "#score-up-detail", function(e){
// 	e.preventDefault()
// 	var this_ = $(this)
// 	var tweetId = this_.attr("data-id")
// 	var scoreupUrl = $(location).attr('href');
// 	var finalScore;

// 	var pathname = window.location.pathname; 
// 	var scoreupUrl = '/api' + pathname +'scoreup/'

// 	// console.log(this_)
// 	this_.text =("Liked")
// 	$("#score-up-detail").text(this_.text) ;
// 	this_.addClass("btn btn-success btn-sm icon ion-arrow-up-a m-1").removeClass('btn btn-light m-1');
 

//     console.log("urlx", scoreupUrl)

//     $.ajax({
//         method:"GET",
//         url: scoreupUrl,

//         success: function(data){
//           if (data){
//            finalScore = data.finalscore
//            console.log('finalScore',finalScore)
//            $("#score-net").text(finalScore);
//           }
//         },
//         error: function(data){
//           console.log("error from here ")	
//           console.log(data)
//         }

//       })
// })



$(document.body).on("click", "#topic", function(e){
	e.preventDefault()
	var this_ = $(this)
	var scoreupUrl = $(location).attr('href');
	var finalScore;

	var pathname = window.location.pathname; 
	var scoreupUrl = '/api' + pathname +'scoreup/'

	$('#topic').upvote();
	$('#topic').upvote({count: 5, upvoted: 1});
	$('#topic').upvote({count: 5, downvoted: 1});
	$('#topic').upvote({count: 5, upvoted: 1, starred: 1});

	$('#topic').upvote('upvoted');      // Get the upvoted state -> boolean
	$('#topic').upvote('downvoted');    // Get the downvoted state -> boolean
    $('#topic').upvote();

	// Mutators
	$('#topic').upvote('upvote');       // Upvote!
	$('#topic').upvote('downvote');     // Downvote!


	// console.log(this_)
	this_.text =("Liked")
	$("#score-up-detail").text(this_.text) ;
	// this_.addClass("btn btn-success btn-sm icon ion-arrow-up-a m-1").removeClass('btn btn-light m-1');
 

    console.log("urlx", scoreupUrl)

    $.ajax({
        method:"GET",
        url: scoreupUrl,

        success: function(data){
          if (data){
           finalScore = data.finalscore
           console.log('finalScore',finalScore)
           $("#data-id").text(finalScore);
          }
        },
        error: function(data){
          console.log("error from here ")	
          console.log(data)
        }
      })
})




$(document).ready(function(){
	console.log('JQ Working');
    var query = getParameterByName('q')
    var candidateList = [];
    var nextCandidateUrl;

    function candidateAttach(value){
		var candidateId = value.candidate_id;
		var candidateName = value.candiate_name; 
		var candidateSummary = value.summary_wiki;
		var candidateUrl = value.urlreturn;
		var candidateScoreUp = value.score_up;
		var candidateScoreDown = value.score_down;
		var candidateScore = value.score;

		var candidateHtmlForm ="<div class=\"media\"><div class =\"media-left\">" 
		 + candidateName 	+ "<br/>"
		 + candidateSummary + "<br/>"
		 +"<a href='" + candidateUrl + "'> See detailss </a>"
		 +"</div> </div><hr/>";

	    $("#candidate-search-results").append(candidateHtmlForm);


	    // candidate score 
	    // candidateScore =  candidateScoreUp - candidateScoreDown
	    // $("#score-net").text(candidateScore);

    }

	function parseCandidates(){
		if (candidateList == 0) {
			$("#candidate-search-results").text("No Candidates availble by that name")
		} else 
		// if candidate name exsist display the candidate
		 {
				$.each(candidateList , function(key, value)
				{		
						candidateAttach(value)	
				})
		 }	

	}

	function fetchCandidate(url)
		{

			var fetchUrl;
			if (!url) {
				fetchUrl = '/api/candidates/';
			} else {
				fetchUrl = url;
			}
			console.log("fetching candidates...");
			$.ajax({
			    url: '/api/candidates/',
			    data: {
			    	"q":query
			    },
			    method: 'get', // This is the default though, you don't actually need to always mention it
			    success: function(data) {
			    	candidateList = data.results;
			    	if(data.next) {
			    		nextCandidateUrl = data.next
			    	} else {
			    		$('#loadmore-candidates-search-results').css("display", "none")
			    	}
			    	
			    	parseCandidates();
			    },
			    failure: function(data) { 
			        alert('Got an error dude');
			    }
			}); 
	   }
	   fetchCandidate()

	   $('#loadmore-candidates-search-results').click(function(event) {
	   		event.preventDefault()
	   		if(nextCandidateUrl){
	   			 fetchCandidate(nextCandidateUrl)
	   		}
	   })

}); // end


// this part is for the search where when you type the search resutls are retrived automatically - Autosearching

$(document).ready(function(){
	var typingTimer;
	var doneInterval = 500;
	var searchInput = $("#main-search-form input[type=text]");
	var searchQuery;


	searchInput.keyup(function(event){
		searchQuery = $(this).val();
		clearTimeout(typingTimer);
		typingTimer = setTimeout(doneSearchTypying, doneInterval); 

	})

	searchInput.keydown(function(event){
		clearTimeout(typingTimer);
	})

	function doneSearchTypying(){
		if (searchQuery){
			// do search
			var url = '/candidates/search/?q=' + searchQuery;
			document.location.href =url;

		}

	}

})







// this part is for allocating the scores


// var scoreUp, scoreDown,  scoreNet, activeBtn, valueUpdated;
// scoreUp =0;
// scoreDown = 0
// scoreTotal = 0;
// activeBtn = 0;

// valueUpdatedUp = false;
// valueUpdatedDown = false;

// take the current value - from the database - Need to figure out how to do this
// scoreNet = Math.floor(Math.random() *10);

// document.querySelector('#score-net').textContent = ;



// // update the value based on the button 
// function calculate(){
// 			if (scoreUp === 0 ){
// 				scoreUp =1;
// 				scoreDown = 0;
// 				scoreNet = scoreNet + scoreUp;
// 				document.querySelector('#score-net').textContent = scoreNet;
// 			}
// 			else if (scoreDown === 0 ){
// 				scoreDown =1;
// 				scoreUp =0;
// 				scoreNet = scoreNet -  scoreDown;
// 				document.querySelector('#score-net').textContent = scoreNet;
// 			}		
// };
// document.querySelector('#score-up-detail').addEventListener('click', function(){
// 		calculate();
// });


// document.querySelector('#score-down-detail').addEventListener('click', function(){
// 		calculate();
// });



