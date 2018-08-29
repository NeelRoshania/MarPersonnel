// C:\Users\nrosh\Anaconda2\Scripts\PROJECTS\PYTHON\DJANGO\acpersonnel\ajaxified\home\js
// Ctrl D to find all of same and type to replace

// about:config -> dom.moduleScripts.enabled;true

// console.log("JS_userToDo.js found.")
import * as handler from "./handlerFunctions.js"
import * as notification from "./handleNotifications.js"
// import * from "./handlerFunctions.js"

$(document).ready(function(){


    var $myForm = $('.my-ajax-form')
    var headers = new Headers();
    var $userToDoPage = 1;
    var $searchHomePage = 1;
    var $urlLocation;

    // Setup deleteDiv as hidden and setup delete button event listener
    $(".deleteDiv").hide()
    // $("#updateItem").append("ajax loaded.")

    // Assign date picker to form field
    $( ".datepicker" ).datepicker({
      changeMonth: true,
      changeYear: true,
      yearRange: "1900:2012",
      dateFormat: "yy-mm-dd",
      // You can put more options here.
    });

    // Setup search bar date picker to toggle on radio button change -> disable text input on date select
    $(".objectHeader").on("click", "#searchObject", function(){
        $("#searchObjectForm").slideToggle("fast", function(){
    		$(this).find(".form-check").children("input:nth-child(1)").change(function(){
    			if ($(this).attr("value") == 'date') {
    				// console.log("Add datepicker...")
    				$("#searchObjectField").attr("readonly", true).val('').prop('disabled', false)
        			$("#searchObjectField").datepicker({
    			      changeMonth: true,
    			      changeYear: true,
    			      yearRange: "2017:2022",
    			      dateFormat: "yy-mm-dd",
    					onSelect: function(date) {
    					    // $("#searchObjectField").attr("readonly", true).prop('disabled', false)
    					},
    			      // You can put more options here.
    			    }) 
    			} else {
    				// console.log("Remove datepicker...")
    				$("#searchObjectField").datepicker("destroy").attr("readonly", false).prop('disabled', false)
    			}
        	})
        })
	})

    // Setup slideToggle for object form -> This will be a unique function
    $(".objectHeader").on("click", "#addObject", function(){
    	$("#addObjectForm").slideToggle("fast")
    })

    // Setup slideToggle for object form -> This will be a unique function
    $("#userToDo").on("click", function(){
        // alert("UserToDO clicked...")
        // $("#updateItem").append("UserToDo clicked.")
    })

    // Setup slideToggle for object form -> This will be a unique function
    $(".objectHeader").on("click", "#refreshObjectList", function(){
    	$urlLocation = $(this).attr("data-url")
    	// console.log("Initial refresh url: " + $urlLocation)
        // Perform ajax call to refresh template in authorList.html
        notification.makeNotification("Refresh in progress...", "standard") 
        $.ajax({
        	method: "GET",
        	beforeSend: function(xhr) {
        		xhr.setRequestHeader("X-CSRFToken", csrftoken);
        		$("#object").addClass("blur-all")
        		$(".fa-sync").addClass("fa-spin")
        		 },
    		data: {'status': 'GET -> Request card info.'},
        	url: $urlLocation,

        	success: function(data) {
                handler.objectRefreshSuccess(data, "Refresh Complete!")
                $("#paginationNext, #paginationPrevious").attr("ajaxStatus", "refreshObjectList")
                $searchHomePage = 1

            },
            error: function(jqXHR){
                    handler.handleFormError(jqXHR)
                },
        })

    })

	$("#objectList").on("click", "#edit", function(event){
		event.preventDefault()
		var $urlLocation = $(this).attr('data-location')
		// console.log("populate form at: " + $urlLocation)
		
		// Perform ajax call to populate form data -> Submit CRSF Token
        $.ajax({
        	method: "GET",
        	beforeSend: function(xhr) { 
        		$(".fa-sync").addClass("fa-spin")
        		 },
        	url: $urlLocation,
        	data: {'csrfmiddlewaretoken': csrftoken, 'status': 'getFormObject'},
        	success: handler.handleEditFormObject,
            error: function(jqXHR){
                    handler.handleFormError(jqXHR)
                },
        })			
		
	});

	$("#objectList").on("click", "#deleteYes", function(){
		// Handle urlLocation
        
        if ($(this).attr('ajaxStatus') == "deleteUserToDo") {
            // alert("Deleting a user to do..")
            // $(this).parent().slideToggle("fast")
            $(this).closest("#UserToDo").slideUp("fast")

        } else if ($(this).attr('ajaxStatus') == "deleteUserNote"){
            // alert("Deleting a user note..")
            // $(this).parent().parent().parent().slideToggle("fast")
            $(this).closest("#userNote").slideUp("fast")
        } else if ($(this).attr('ajaxStatus') == "deleteNoteDescriptionForm"){
            // alert("Deleting a user note..")
            // $(this).parent().parent().parent().slideToggle("fast")
            $(this).closest("#noteDescription").slideUp("fast")
            // $(this).slideUp("fast", function(){
            //     $(this).remove()
            // })          
        }


        // Perform ajax call to delete entry -> Submit CRSF Token
        var data = []
        data.push(
            {name: "ajaxStatus", value: $(this).attr('ajaxStatus')},
            {name: "csrfmiddlewaretoken", value: csrftoken},
            )
        var $urlLocation = $(this).attr('href')
        headers.append('X-CSRFToken', csrftoken);
        // console.log($urlLocation)
        // console.log($.param(data))
        $.ajax({
        	method: "POST",
        	beforeSend: function(xhr) { 
        		$(".fa-sync").addClass("fa-spin")
        		xhr.setRequestHeader("X-CSRFToken", csrftoken);
				$("#object").addClass(".blur-all")
        		 },
        	// headers: headers,
        	url: $urlLocation,
        	data: $.param(data),
        	success: function(data) {
                handler.handleDeleteSuccess(data)
            },
            error: function(jqXHR){
                    handler.handleFormError(jqXHR)
                },

        })
	});

	// Handle Pagination Previous
	$("#objectList").on("click", "#paginationPrevious", function(event){
		event.preventDefault()
        if (($(this).attr("ajaxStatus") == "refreshObjectList")) {
            // Is the user making a general pagination request for the delivery plans?
            $urlLocation = $("#refreshObjectList").attr("data-url")
            $userToDoPage -= 1
            // console.log("ajaxStatus: refreshObjectList")
            // console.log("$userToDoPage: " + $userToDoPage + " urlLocation: " + $("#refreshObjectList").attr("data-url"))

            $.ajax({
                method: "GET",
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    $("#objectList").addClass("blur-all")
                    $(".loaderStatus").empty().show()
                    // console.log("#paginationNext beforeSend ajax.")
                     },
                data: {"userToDoPage" : $userToDoPage},
                url: $urlLocation,
                success: function(data) {
                    if (data["errorMessage"]) {
                        notification.makeNotification(data["errorMessage"], "error")
                    } else {
                        handler.handlePaginationSuccess(data)
                        $("#paginationNext, #paginationPrevious").attr("ajaxStatus", "refreshObjectList")
                    }
                },
                error: function(jqXHR){
                    handler.handleFormError(jqXHR)
                },
            }) //Setup jQuery AJAX Call     
        // Otherwise the request must be a search
        } else {
            // Has the user made a request to search for Delivery Plans?
            $searchHomePage -= 1
            // console.log("ajaxStatus: " + $(this).attr("ajaxStatus"))
            // console.log("Search for anything in home - paginationPrevious " + "$searchHomePage: " + $searchHomePage + " urlLocation: " + $(this).attr("data-url"))

            function searchpaginationPrevious(searchTextResult, searchRequestType, urlLocation, dataToSend, ajaxStatus) {
                $.ajax({
                    method: "GET",
                    beforeSend: function(xhr) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        $("#objectList").addClass("blur-all")
                        $(".loaderStatus").empty().show()
                        // console.log("#paginationPrevious beforeSend ajax.")
                         },
                    data: dataToSend,
                    url: urlLocation,
                    success: function(data) {
                        if (data["errorMessage"]) {
                            notification.makeNotification(data["errorMessage"], "error")
                        } else {
                            handler.handlePaginationSuccess(data)
                            $("#paginationNext").attr({"ajaxStatus":ajaxStatus})
                            $("#paginationNext").attr({"searchObjectFieldText": searchTextResult})
                            $("#paginationNext").attr({"requestType": searchRequestType})
                            $("#paginationPrevious").attr("ajaxStatus", ajaxStatus)
                            $("#paginationPrevious").attr({"searchObjectFieldText":searchTextResult})
                            $("#paginationPrevious").attr({"requestType": searchRequestType})
                        }
                    },
                    error: function(jqXHR){
                    handler.handleFormError(jqXHR)
                },
                }) //Setup jQuery AJAX Call  
            }

            searchpaginationPrevious(
                $(this).attr("searchObjectFieldText"), 
                $(this).attr("requestType"),
                $(this).attr("data-url"), 
                {
                    "searchHomePage" : $searchHomePage, 
                    "searchObjectFieldText": $(this).attr("searchObjectFieldText"),
                    "ajaxStatus": $(this).attr("ajaxStatus"),
                    "requestType": $(this).attr("requestType"),
                },
                $(this).attr("ajaxStatus"),
            )
        }
	});		

	// Handle Pagination Next
	$("#objectList").on("click", "#paginationNext", function(event){
		event.preventDefault()

        if (($(this).attr("ajaxStatus") == "refreshObjectList")) {
            // Is the user making a general pagination request for the delivery plans?
            $urlLocation = $("#refreshObjectList").attr("data-url")
            $userToDoPage += 1
            // console.log("ajaxStatus: refreshObjectList")
            // console.log("$userToDoPage: " + $userToDoPage + " urlLocation: " + $("#refreshObjectList").attr("data-url"))

            $.ajax({
                method: "GET",
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    $("#objectList").addClass("blur-all")
                    $(".loaderStatus").empty().show()
                    // console.log("#paginationNext beforeSend ajax.")
                     },
                data: {"userToDoPage" : $userToDoPage},
                url: $urlLocation,
                success: function(data) {
                    if (data["errorMessage"]) {
                        notification.makeNotification(data["errorMessage"], "error")
                    } else {
                        handler.handlePaginationSuccess(data)
                        $("#paginationNext, #paginationPrevious").attr("ajaxStatus", "refreshObjectList")
                    }
                },
                error: function(jqXHR){
                    handler.handleFormError(jqXHR)
                },
            }) //Setup jQuery AJAX Call     
        // Otherwise the request must be a search
        } else {
            // Has the user made a request to search for Delivery Plans?
            $searchHomePage += 1
            // console.log("ajaxStatus: " + $(this).attr("ajaxStatus"))
            // console.log("Search for anything in home - paginationNext " + "$searchHomePage: " + $searchHomePage + " urlLocation: " + $(this).attr("data-url"))

            function searchPaginationNext(searchTextResult, searchRequestType, urlLocation, dataToSend, ajaxStatus) {
                $.ajax({
                    method: "GET",
                    beforeSend: function(xhr) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        $("#objectList").addClass("blur-all")
                        $(".loaderStatus").empty().show()
                        // console.log("#paginationNext beforeSend ajax.")
                         },
                    data: dataToSend,
                    url: urlLocation,
                    success: function(data) {
                        if (data["errorMessage"]) {
                            notification.makeNotification(data["errorMessage"], "error")
                        } else {
                            handler.handlePaginationSuccess(data)
                            $("#paginationNext").attr({"ajaxStatus":ajaxStatus})
                            $("#paginationNext").attr({"searchObjectFieldText": searchTextResult})
                            $("#paginationNext").attr({"requestType": searchRequestType})
                            $("#paginationPrevious").attr("ajaxStatus", ajaxStatus)
                            $("#paginationPrevious").attr({"searchObjectFieldText":searchTextResult})
                            $("#paginationPrevious").attr({"requestType": searchRequestType})
                        }
                    },
                    error: function(jqXHR){
                    handler.handleFormError(jqXHR)
                },
                }) //Setup jQuery AJAX Call  
            }

            searchPaginationNext(
                $(this).attr("searchObjectFieldText"), 
                $(this).attr("requestType"),
                $(this).attr("data-url"), 
                {
                    "searchHomePage" : $searchHomePage, 
                    "searchObjectFieldText": $(this).attr("searchObjectFieldText"),
                    "ajaxStatus": $(this).attr("ajaxStatus"),
                    "requestType": $(this).attr("requestType"),
                },
                $(this).attr("ajaxStatus"),
            )
        }	
	});	

	// Handle add object form submission
	$(document).on('submit', '.my-ajax-form', function(event){
        if (confirm("Is this information correct?")) {
            event.preventDefault()	// Prevent the form from submitting straight away
            // alert(".my-ajax-form' clicked.")
            var $urlLocation = $(this).attr("data-url") // URL location specified in form to send data to
            var data = $(this).serializeArray() // Grab the form information effeciently
            $(this).clear	// Clear form to prevent double submit
            data.push(
            	{name: "ajaxStatus", value: $(this).attr("ajaxStatus")},
            	{name: "userToDo", value: $(this).attr("userTodo")}, 
                {name: "userNote", value: $(this).attr("userNote")},
                {name: "url", value: $urlLocation},
                {name: "newObjectSubmit", value: true},
                );	// Accumulate ajax data fields
            // console.log("POST URL Location --> " + $urlLocation + '\nSerialized AJAX Data --> ' + $.param(data) )

            // Perform ajax call to update entry
            $.ajax({
            	method: "POST",
            	url: $urlLocation,
            	beforeSend: function(xhr) {
        				$("#object").addClass("blur-all")
        		        xhr.setRequestHeader("X-CSRFToken", csrftoken)
                        $myForm[0].reset(); // reset form data 
                        // console.log(data)
                		 },
        		data: $.param(data),
            	success: function(data){
                    if (data["errorMessage"]) {
                        notification.makeNotification(data["errorMessage"], "error")
                    } else {
                        notification.makeNotification(data["message"], "online")
                        handler.handleFormSuccess($("#refreshObjectList").attr("data-url"), false)
                    }
                },
                error: function(jqXHR){
                    handler.handleFormError(jqXHR)
                },	   
        	});
        }
    })

	// Handle editObjectForm - Need to think of a way to identify each edit from uniquely from a js perspective
	$(document).on('submit', '.editObjectForm', function(event){
        // Perform ajax call to update entry
        event.preventDefault()	// Prevent the form from submitting straight away
        if (confirm("Is this information correct?")) {
            // console.log("Confirmation of edit submit")
            var $urlLocation = $(this).attr("data-url") // URL location specified in form to send data to
            var data = $(this).serializeArray() // Grab the form information effeciently
            data.push(
            	{name: "ajaxStatus", value: $(this).attr("ajaxStatus")},
            	{name: "editObjectSubmit", value: true} );	// Accumulate ajax data fields
            $(this).clear	// Clear form to prevent double submit
            // console.log("POST URL Location --> " + $urlLocation + '\nSerialized AJAX Data --> ' + $.param(data) )

            // Perform ajax call to update entry
            $.ajax({
            	method: "POST",
            	url: $urlLocation,
            	beforeSend: function(xhr) {
        				$("#object").addClass("blur-all")
        		        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        // $("#updateItem").append("Form submitted.")
                		 },
        		data:  $.param(data),
            	success: function(data){
                    if (data["errorMessage"]) {
                        notification.makeNotification(data["errorMessage"], "error")
                    } else {
                        notification.makeNotification(data["message"], "online")
                        handler.handleFormSuccess($("#refreshObjectList").attr("data-url"), false)
                    }
                },
                error: function(jqXHR){
                    handler.handleFormError(jqXHR)
                },	   
    		});
        }
    })	

    // Handle searchObjectForm - Need to think of a way to identify each edit from uniquely from a js perspective
	$(document).on('submit', '.searchObjectForm', function(event){
        event.preventDefault()	// Prevent the form from submitting straight away
        // alert("Search for object...")
        var $urlLocation = $(this).attr("data-url") // URL location specified in form to send data to
        var data = $(this).serializeArray() // Grab the form information effeciently
        data.push(
        	{name: "ajaxStatus", value: $(this).attr("ajaxStatus")},
        	{name: "searchObjectSubmit", value: true},
            {name: "searchHomePage", value: $searchHomePage},
        );	// Accumulate ajax data fields
        $(this).clear	// Clear form to prevent double submit
        // console.log("GET URL Location --> " + $urlLocation)
        // console.log("Search GET data:" + $.param(data))
        // console.log("searchObjectFieldText: " + $(this).find('.searchField').val())

        // Perform ajax call to update entry 
        function searchInHome(urlAjaxLocation, ajaxStatus, dataToPass, searchTextResult, searchRequestType){
            // Perform ajax call to update entry
            // console.log("searchInProduction called")

            // Perform ajax call to update entry - home_handlePagination
            $.ajax({
            	method: "GET",
            	url: $urlLocation,
            	beforeSend: function(xhr) {
    					$("#objectList").addClass("blur-all")
    			        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        notification.makeNotification("Search in progress...", "standard")
    	        		 },
        		data:  $.param(dataToPass),
            	success: function(data) {
                    if (data["errorMessage"]) {
                        notification.makeNotification(data["errorMessage"], "error")
                    } else {
                        if (data["message"]) {
                            notification.makeNotification(data["message"], "error")
                        } else {
                            handler.objectRefreshSuccess(data, "Search complete!")
                            // Pagination section must now be configured to continue search requests
                            $("#paginationNext").attr({"ajaxStatus":ajaxStatus})
                            $("#paginationNext").attr({"searchObjectFieldText": searchTextResult})
                            $("#paginationNext").attr({"requestType": searchRequestType})
                            $("#paginationPrevious").attr("ajaxStatus", ajaxStatus)
                            $("#paginationPrevious").attr({"searchObjectFieldText":searchTextResult})
                            $("#paginationPrevious").attr({"requestType": searchRequestType})
                            $searchHomePage = 1
                        }
                        
                    }
                },
                error: function(jqXHR){
                    handler.handleFormError(jqXHR)
                },	   
			});
        }

        // Execture home ajax
        searchInHome(
            $(this).attr("data-url"),
            $(this).attr("ajaxStatus"), 
            data, 
             $(this).find('.searchField').val(),
            $('input[name=radio]:checked').val(),
        )

        $('input[name=radio]:checked').removeAttr('checked')
    })
})