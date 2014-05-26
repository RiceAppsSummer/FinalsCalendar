$(document).ready(function(){
	var currentCourses = [];
	function disableTeachAndSect(){
		$("#teacher").prop('disabled', true);
		$("#teacher").empty();
		var noTeach = $('<option></option>').text("Please type in a Course");
		$("#teacher").append(noTeach);
		$("#section").prop('disabled', true);
		$("#section").empty();
		var noSect = $('<option></option>').text("Please select a teacher");
		$("#section").append(noSect);
	}
	$('#calendar').fullCalendar({
        // put your options and callbacks here
        defaultView: "agendaWeek",
        defaultDate: "2014-04-30", 
        timezone:"UTC"
        });
	$("#coursenumber").prop('disabled', true);
	disableTeachAndSect();
	$.getJSON("/courses",function(courses){
		$("#add").click(function(){
			var course = $("#coursenumber").val();
			if(courses.hasOwnProperty(course)&& currentCourses.indexOf(course)==-1){
				var teacher = $("#teacher").val();
				var section = $("#section").val();
				var stime = courses[course][teacher][section].start_time
				var etime = courses[course][teacher][section].end_time
				console.log(courses[course][teacher][section].start_time);
				console.log(stime);
				var examDuration = {title:course,start:stime,end:etime,allDay:false,id:course}
				$("#calendar").fullCalendar('addEventSource',[examDuration])
				currentCourses.push(course)
				var deleteButton = $('<a class="btn btn-danger" href="#"> <i class="glyphicon glyphicon-trash"></i></a>');
				var courseText = $('<span></span>').text(course).addClass("addedCourse")
				var courseAdded = $('<li></li>').addClass("list-group-item").append(courseText).append(deleteButton);
				$("#currentCourses").append(courseAdded);
				deleteButton.click(function(){
					courseAdded.remove();
					index = currentCourses.indexOf(course);
					currentCourses.splice(index,1);
					$("#calendar").fullCalendar('removeEvents',[course])


				})
			}
		})
		console.log(courses);
		$("#coursenumber").prop('disabled', false);
	    $("#coursenumber").autocomplete({
	      	source: Object.keys(courses),   	
	    });
	    $("#coursenumber").on("keyup autocompleteclose",function(){
	    	var course = $("#coursenumber").val();
	    	if(courses.hasOwnProperty(course)){
	    		$("#teacher").empty();
	    		for (teacher in courses[course]){
	    			var option = $('<option></option>').attr("value",teacher).text(teacher);
	    			$("#teacher").append(option);
	    		}
	    		$("#teacher").prop('disabled', false);   		

	    		$("#teacher").on('change',function(){
		    		var instructor = $("#teacher").val()	
    				$("#section").empty();
		    		for (section in courses[course][instructor]){
		    			var option = $('<option></option>').attr("value",section).text(section);
		    			$("#section").append(option);
		    		}


	    		});

	    		$("#section").prop('disabled', false);  
	    		 
	    		$("#teacher").change(); 

	    	}
	    	else{
	    		disableTeachAndSect();
	    	}

	    	
	    }); // coursenumer.keyup()
	});
});


