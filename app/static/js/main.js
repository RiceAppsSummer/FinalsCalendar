$(document).ready(function(){

	$('#calendar').fullCalendar({
        // put your options and callbacks here
          // defaultView: "agendaWeek"
        });
	$("#coursenumber").prop('disabled', true);
	$("#teacher").prop('disabled', true);
	$("#section").prop('disabled', true);
	$.getJSON("/courses",function(courses){

		console.log(courses);
		$("#coursenumber").prop('disabled', false);
	    $("#coursenumber").autocomplete({
	      	source: Object.keys(courses), 
	      	

	    });
	    $("#coursenumber").keyup(function(){
	    	var course = $("#coursenumber").val();
	    	if(courses.hasOwnProperty(course)){
	    		$("#teacher").empty();
	    		for (teacher in courses[course]){
	    			var option = $('<option></option>').attr("value",teacher).text(teacher);
	    			$("#teacher").append(option);
	    		}
	    		$("#teacher").prop('disabled', false);
	    	} 
	    	
	    });
	});
});


