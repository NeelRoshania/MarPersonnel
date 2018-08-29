// C:\Users\nrosh\Anaconda2\Scripts\PROJECTS\PYTHON\DJANGO\acpersonnel\ajaxified\home\js
// Ctrl D to find all of same and type to replace

// about:config -> dom.moduleScripts.enabled;true

// console.log("JS_production.js found.")
import * as handler from "./handlerFunctions_production.js"
import * as notification from "/static/home/js/handleNotifications.js"

$(document).ready(function(){

    var $myForm = $('.production-form')
    var headers = new Headers();
    var $productionPage = 1;
    var $searchProductionPage = 1;
    var $searchRawMaterialsPage = 1
    var $urlLocation;

    // Setup deleteDiv as hidden and setup delete button event listener
    $(".deleteDiv").hide()
    // $("#updateItem").append("JS_production loaded.")

    // Assign date picker to form field
    $( ".datepicker" ).datepicker({
      changeMonth: true,
      changeYear: true,
      yearRange: "1900:2012",
      dateFormat: "yy-mm-dd",
      // You can put more options here.
    });

    // Setup search bar date picker to toggle on radio button change -> disable text input on date select
    $(".objectHeader").on("click", "#searchProduction", function(){
        $("#searchProductionForm").slideToggle("fast", function(){
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
    $(".objectHeader").on("click", "#addProduction", function(){
    	$("#addProductionForm").slideToggle("fast")
    })

    // Setup slideToggle for object form -> This will be a unique function
    $("#userToDo").on("click", function(){
        // alert("UserToDO clicked...")
        // $("#updateItem").append("UserToDo clicked.")
    })

    // Setup slideToggle for object form -> This will be a unique function
    $(".objectHeader").on("click", "#refreshProductionList", function(){
    	$urlLocation = $(this).attr("data-url")
    	// console.log("Initial refresh url: " + $urlLocation)

        function ajaxRefreshProductionPlan(ajaxStatus) {
            // Perform ajax call to refresh template in authorList.html
            $.ajax({
                method: "GET",
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    $("#productionPlan").addClass("blur-all")
                    $(".fa-sync").addClass("fa-spin")
                    notification.makeNotification("Refresh in progress...", "standard") 
                     },
                data: {'status': 'GET -> Request card info.'},
                url: $urlLocation,
                success: function(data) {
                            handler.objectRefreshSuccess_production("Refresh complete!", ajaxStatus, data)
                            // Pagination section must now be configured to continue search requests
                            $("#productionPaginationNext, #productionPaginationPrevious").attr("ajaxStatus", "refreshProductionList")
                            $productionPage = 1;
                            $searchProductionPage = 1;
                        },
                error: function(jqXHR){
                    handler.handleFormError_production("Error in #edit", jqXHR)
                },
            })
        }
    ajaxRefreshProductionPlan($(this).attr("ajaxStatus"))
    })

	$("#productionPlan, #addProductionForm").on("click", "#edit", function(event){
		event.preventDefault()
		var $urlLocation = $(this).attr('data-location')
		// console.log("populate form at: " + $urlLocation)

		// ajax doesn't recognise $(this).attr('ajaxStatus'), so developed function to run
        runAjax($(this).attr('ajaxStatus'))

        function runAjax(ajaxState) {
            // console.log("Run ajax called -> " + ajaxState)
            $.ajax({
                method: "GET",
                beforeSend: function(xhr) { 
                    $(".fa-sync").addClass("fa-spin")
                     },
                url: $urlLocation,
                data: {'csrfmiddlewaretoken': csrftoken, 'status': 'getFormObject'},
                success: function(data) {
                    handler.handleEditFormObject_production(ajaxState, data)
                },
                error: function(jqXHR){
                    handler.handleFormError_production("Error in #edit", jqXHR)
                },
            })            
            }
	   }
   );

	$("#productionPlan, #addProductionForm").on("click", "#deleteYes", function(){
        // alert("deleteYes clicked.")
		// Handle urlLocation
        if ($(this).attr('ajaxStatus') == "deleteProductionMeetingForm") {
            // alert("Deleting a production meeting..")
            // $(this).parent().parent().slideToggle("fast")
            $(this).closest("#productionList").slideUp("fast")
            // $(this).closest("#productionList").slideUp("fast")
        } else if ($(this).attr('ajaxStatus') == "deleteProductionNote"){
            // alert("Deleting a user note..")
            // $(this).parent().parent().parent().slideToggle("fast")
            $(this).closest("#subObject").slideUp("fast")
            $(this).slideUp("fast", function(){
                $(this).remove()
            })          
        } else if ($(this).attr('ajaxStatus') == "deleteRMShortageForm") {
            // alert("Deleting a user note..")
            // $(this).parent().parent().parent().slideToggle("fast")
            $(this).closest("#subObject").slideUp("fast")
            $(this).slideUp("fast", function(){
                $(this).remove()
            })       
        } else if ($(this).attr('ajaxStatus') == "deleteMaintenanceIssueForm") {
            // alert("Deleting a user note..")
            // $(this).parent().parent().parent().slideToggle("fast")
            $(this).closest("#subObject").slideUp("fast")
            $(this).slideUp("fast", function(){
                $(this).remove()
            })  
        } else if ($(this).attr('ajaxStatus') == "deleteProductionPlanForm") {
            // alert("Deleting a user note..")
            // $(this).parent().parent().parent().slideToggle("fast")
            $(this).closest("#subObject").slideUp("fast")
            $(this).slideUp("fast", function(){
                $(this).remove()
            })          
        } else if ($(this).attr('ajaxStatus') == "deleteRawMaterial") {
            if (confirm("Warning! If there are raw material shortages for this raw material, they will all be deleted too! \n\n Continue?")) {

                $(this).closest("#rawMaterialResult").slideUp("fast")
                
                // // Perform ajax call to delete entry -> Submit CRSF Token
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
                            notification.makeNotification(data["message"], "standard")
                            $("#refreshProductionList").trigger("click")
                            handler.handleDeleteSuccess_production(data)
                        },
                    error: function(jqXHR){
                        handler.handleFormError_production("Error in #deleteYes", jqXHR)
                    },

                })
            }
        }
        
	});

	// Handle Pagination Previous
	$("#productionPlan").on("click", "#productionPaginationPrevious", function(event){
		event.preventDefault()
		if (($(this).attr("ajaxStatus") == "refreshProductionList")) {
            // Is the user making a general pagination request for the delivery plans?
            $urlLocation = $("#refreshProductionList").attr("data-url")
            $productionPage -= 1
            // console.log("ajaxStatus: refreshProductionList")
            // console.log("Search for customerID - productionPaginationNext " + "$productionPage: " + $productionPage + " urlLocation: " + $urlLocation)

            $.ajax({
                method: "GET",
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    $("#productionPlan").addClass("blur-all")
                    $(".loaderStatus").empty().show()
                     },
                data: {
                        "productionPage" : $productionPage,
                        "ajaxStatus": $(this).attr("ajaxStatus")
                    },
                url: $urlLocation,
                success: function(data) {
                    if (data["errorMessage"]) {
                        alert(data["errorMessage"])
                    } else {
                        handler.handlePaginationSuccess_production("DeliveryPlanPagination", data)
                        $("#productionPaginationNext, #productionPaginationPrevious").attr("ajaxStatus", "refreshProductionList")

                    }
                },
                error: handler.handleFormError,
            }) //Setup jQuery AJAX Call   

        // Otherwise the request must be a search
        } else {
            // Has the user made a request to search for Delivery Plans?
            $searchProductionPage -= 1
            // console.log("ajaxStatus: " + $(this).attr("ajaxStatus"))
            // console.log("Search for anything in production - productionPaginationPrevious " + "$searchProductionPage: " + $searchProductionPage + " urlLocation: " + $urlLocation)

            function searchPaginationPrevious(searchTextResult, searchRequestType, urlLocation, dataToSend, ajaxStatus) {
                $.ajax({
                    method: "GET",
                    beforeSend: function(xhr) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        $("#productionPlan").addClass("blur-all")
                        $(".loaderStatus").empty().show()
                         },
                    data: dataToSend,
                    url: urlLocation,
                    success: function(data) {
                        if (data["errorMessage"]) {
                            alert(data["errorMessage"])
                        } else {
                            handler.handlePaginationSuccess_production("searchDeliveryPlan", data)
                            $("#productionPaginationNext").attr({"ajaxStatus":ajaxStatus})
                            $("#productionPaginationNext").attr({"searchObjectFieldText": searchTextResult})
                            $("#productionPaginationNext").attr({"requestType": searchRequestType})
                            $("#productionPaginationPrevious").attr("ajaxStatus", ajaxStatus)
                            $("#productionPaginationPrevious").attr({"searchObjectFieldText":searchTextResult})
                            $("#productionPaginationPrevious").attr({"requestType": searchRequestType})
                        }
                    },
                    error: handler.handleFormError,
                }) //Setup jQuery AJAX Call  
            }

            searchPaginationPrevious(
                $(this).attr("searchObjectFieldText"), 
                $(this).attr("requestType"),
                $(this).attr("data-url"), 
                {
                    "searchProductionPage" : $searchProductionPage, 
                    "searchObjectFieldText": $(this).attr("searchObjectFieldText"),
                    "ajaxStatus": $(this).attr("ajaxStatus"),
                    "requestType": $(this).attr("requestType"),
                },
                $(this).attr("ajaxStatus"),
            )
        }	
	});		

	// Handle Pagination Next
	$("#productionPlan").on("click", "#productionPaginationNext", function(event){
		event.preventDefault()
		if (($(this).attr("ajaxStatus") == "refreshProductionList")) {
            // Is the user making a general pagination request for the delivery plans?
            $urlLocation = $("#refreshProductionList").attr("data-url")
            $productionPage += 1
            // console.log("ajaxStatus: refreshProductionList")
            // console.log("$productionPage: " + $productionPage + " urlLocation: " + $("#refreshProductionList").attr("data-url"))

            $.ajax({
                method: "GET",
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    $("#productionPlan").addClass("blur-all")
                    $(".loaderStatus").empty().show()
                     },
                data: {
                        "productionPage" : $productionPage,
                        "ajaxStatus": $(this).attr("ajaxStatus")
                    },
                url: $urlLocation,
                success: function(data) {
                    if (data["errorMessage"]) {
                        alert(data["errorMessage"])
                    } else {
                        handler.handlePaginationSuccess_production("DeliveryPlanPagination", data)
                        $("#productionPaginationNext, #productionPaginationPrevious").attr("ajaxStatus", "refreshProductionList")
                    }
                },
                error: handler.handleFormError,
            }) //Setup jQuery AJAX Call     
        // Otherwise the request must be a search
        } else {
            // Has the user made a request to search for Delivery Plans?
            $searchProductionPage += 1
            // console.log("ajaxStatus: " + $(this).attr("ajaxStatus"))
            // console.log("Search for anything in production - customerIDPaginationNext " + "$searchProductionPage: " + $searchProductionPage + " urlLocation: " + $(this).attr("data-url"))

            function searchPaginationNext(searchTextResult, searchRequestType, urlLocation, dataToSend, ajaxStatus) {
                $.ajax({
                    method: "GET",
                    beforeSend: function(xhr) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        $("#productionPlan").addClass("blur-all")
                        $(".loaderStatus").empty().show()
                         },
                    data: dataToSend,
                    url: urlLocation,
                    success: function(data) {
                        if (data["errorMessage"]) {
                            alert(data["errorMessage"])
                        } else {
                            handler.handlePaginationSuccess_production("searchDeliveryPlan", data)
                            $("#productionPaginationNext").attr({"ajaxStatus":ajaxStatus})
                            $("#productionPaginationNext").attr({"searchObjectFieldText": searchTextResult})
                            $("#productionPaginationNext").attr({"requestType": searchRequestType})
                            $("#productionPaginationPrevious").attr("ajaxStatus", ajaxStatus)
                            $("#productionPaginationPrevious").attr({"searchObjectFieldText":searchTextResult})
                            $("#productionPaginationPrevious").attr({"requestType": searchRequestType})
                        }
                    },
                    error: handler.handleFormError,
                }) //Setup jQuery AJAX Call  
            }

            searchPaginationNext(
                $(this).attr("searchObjectFieldText"), 
                $(this).attr("requestType"),
                $(this).attr("data-url"), 
                {
                    "searchProductionPage" : $searchProductionPage, 
                    "searchObjectFieldText": $(this).attr("searchObjectFieldText"),
                    "ajaxStatus": $(this).attr("ajaxStatus"),
                    "requestType": $(this).attr("requestType"),
                },
                $(this).attr("ajaxStatus"),
            )
        }   	
	});

    // Handle Pagination Next - This needs to account for search CustomerID and general qualityList andsearched ones
    $("#addProductionForm").on("click", "#rawMaterialsPaginationNext", function(event){
        event.preventDefault()
        $urlLocation = $(this).attr("data-url")
        $searchRawMaterialsPage += 1
        // console.log("Search for RD Project - rawMaterialsPaginationNext ")

        function searchPaginationNext(searchTextResult, urlLocation, dataToSend) {
            $.ajax({
                method: "GET",
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    $("#rawMaterialResults").addClass("blur-all")
                    $(".loaderStatus").empty().show()
                     },
                data: dataToSend,
                url: $urlLocation,
                success: function(data) {
                    if (data["errorMessage"]) {
                        notification.makeNotification(data["errorMessage"], "standard")
                    } else {
                        handler.handlePaginationSuccess_production("RawMaterialPagination", data)
                        $("#rawMaterialsPaginationNext, #rawMaterialsPaginationPrevious").attr("searchObjectFieldText", searchTextResult)
                    }
                    
                },
                error: function(jqXHR){
                    handler.handleFormError_quality("Error in searchPaginationNext", jqXHR)
                },
            }) //Setup jQuery AJAX Call
        }

        searchPaginationNext(
                $(this).attr("searchObjectFieldText"),
                $(this).attr("data-url"),
                {
                    "searchObjectFieldText": $(this).attr("searchObjectFieldText"),
                    "searchRawMaterialsPage": $searchRawMaterialsPage,
                    "RawMaterialPaginate": true,
                },
                $(this).attr("ajaxStatus"),
            )
        }
    )

    $("#addProductionForm").on("click", "#rawMaterialsPaginationPrevious", function(event){
        event.preventDefault()
        $urlLocation = $(this).attr("data-url")
        $searchRawMaterialsPage -= 1
        // console.log("Search for RD Project - rawMaterialsPaginationPrevious ")

        function searchPaginationNext(searchTextResult, urlLocation, dataToSend) {
            $.ajax({
                method: "GET",
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    $("#rawMaterialResults").addClass("blur-all")
                    $(".loaderStatus").empty().show()
                     },
                data: dataToSend,
                url: $urlLocation,
                success: function(data) {
                    if (data["errorMessage"]) {
                        notification.makeNotification(data["errorMessage"], "standard")
                    } else {
                        handler.handlePaginationSuccess_production("RawMaterialPagination", data)
                        $("#rawMaterialsPaginationNext, #rawMaterialsPaginationPrevious").attr("searchObjectFieldText", searchTextResult)
                    }
                    
                },
                error: function(jqXHR){
                    handler.handleFormError_quality("Error in searchPaginationNext", jqXHR)
                },
            }) //Setup jQuery AJAX Call
        }

        searchPaginationNext(
                $(this).attr("searchObjectFieldText"),
                $(this).attr("data-url"),
                {
                    "searchObjectFieldText": $(this).attr("searchObjectFieldText"),
                    "searchRawMaterialsPage": $searchRawMaterialsPage,
                    "RawMaterialPaginate": true,
                },
                $(this).attr("ajaxStatus"),
            )
        }
    )

    // Handle add object form submission
    $(document).on('submit', '.production-form', function(event){
        if (confirm("Is this information correct?")) {
            // Perform ajax call to update entry
           // code
            event.preventDefault()  // Prevent the form from submitting straight away
            // alert(".my-ajax-form' clicked.")
            var $urlLocation = $(this).attr("data-url") // URL location specified in form to send data to
            var data = $(this).serializeArray() // Grab the form information effeciently
            $(this).clear   // Clear form to prevent double submit
            data.push(
                {name: "ajaxStatus", value: $(this).attr("ajaxStatus")},
                {name: "prodMeeting", value: $(this).attr("prodMeeting")},
                {name: "url", value: $urlLocation},
                {name: "newObjectSubmit", value: true},
                );  // Accumulate ajax data fields
            // console.log("POST URL Location --> " + $urlLocation + '\nSerialized AJAX Data --> ' + $.param(data) )

            // Perform ajax call to update entry
            $.ajax({
                method: "POST",
                url: $urlLocation,
                beforeSend: function(xhr) {
                        $("#productionPlan").addClass("blur-all")
                        xhr.setRequestHeader("X-CSRFToken", csrftoken)
                        $myForm[0].reset(); // reset form data 
                        // console.log("Data to send: ")
                        // console.log(data)
                         },
                data: $.param(data),
                success: function(data){
                    if(data["error"]) {
                        notification.makeNotification(data["errorMessage"], "error")
                    } else {
                        notification.makeNotification(data["message"], "online")
                        handler.handleFormSuccess_production($("#refreshProductionList").attr("data-url"), false, data, data['message'])
                        // console.log("Data: " + data)
                    }
                },
                error: function(jqXHR){
                    handler.handleFormError_production("Error in .production-form", jqXHR)
                },    
            });
        }
    })

	// Handle editObjectForm - Need to think of a way to identify each edit from uniquely from a js perspective
	$(document).on('submit', '.editProductionForm', function(event){
	   // code
        event.preventDefault()	// Prevent the form from submitting straight away
        if (confirm("Is this information correct?")) {
            // console.log("object Edit Form submitted...")
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
    					$("#productionPlan").addClass("blur-all")
    			        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        // $("#updateItem").append("Form submitted.")
    	        		 },
        		data:  $.param(data),
            	success: function(data){
                    if(data["error"]) {
                        notification.makeNotification(data["errorMessage"], "error")
                    } else {
                        notification.makeNotification(data["message"], "standard")
                        handler.handleFormSuccess_production($("#refreshProductionList").attr("data-url"), false, data, data['message'])
                    }
                },
                error: function(jqXHR){
                    handler.handleFormError_production("Error in .editProductionForm", jqXHR)
                },	   
			});
        }
    })	

    // Handle searchObjectForm - Need to think of a way to identify each edit from uniquely from a js perspective
	$(document).on('submit', '.searchProductionForm', function(event){
        event.preventDefault()	// Prevent the form from submitting straight away
        // alert("Search for object...")
        var $urlLocation = $(this).attr("data-url") // URL location specified in form to send data to
        var data = $(this).serializeArray() // Grab the form information effeciently
        data.push(
        	{name: "ajaxStatus", value: $(this).attr("ajaxStatus")},
            // {name: "searchObjectFieldText", value: $("#searchObjectFieldText[name=search_RMShortages_Field]").val()},
        	{name: "searchObjectSubmit", value: true},
            {name: "searchProductionPage", value: $searchProductionPage},
            {name: "searchRawMaterialsPage", value: $searchRawMaterialsPage},);	// Accumulate ajax data fields
        $(this).clear	// Clear form to prevent double submit
        // console.log("GET URL Location --> " + $urlLocation)
        // console.log("Search GET data:" + $.param(data))
        // console.log("Checked radio field: " + $('input[name=radio]:checked').val())
        // console.log("Search text: " + $(this).find('.searchField').val())

        // Perform ajax call to update entry 
        function searchInProduction(urlAjaxLocation, ajaxStatus, dataToPass, searchTextResult, searchRequestType){
            // Perform ajax call to update entry
            // console.log("searchInProduction called")
            $.ajax({
            	method: "GET",
            	url: $urlLocation,
            	beforeSend: function(xhr) {
    					$("#productionPlan").addClass("blur-all")
    			        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        notification.makeNotification("Search in progress...", "standard")
    	        		 },
        		data:  $.param(dataToPass),
                success: function(data) {
                        if (data["errorMessage"]) {
                            notification.makeNotification(data["errorMessage"], "alert")
                        } else {
                            if (data["message"]) {
                                notification.makeNotification(data["message"], "standard")
                            } else {
                                handler.objectRefreshSuccess_production("Search complete!", ajaxStatus, data)
                                // Pagination section must now be configured to continue search requests

                                if (ajaxStatus == "search_EDIT_RawMaterialPaginate"){
                                    $("#rawMaterialsPaginationNext, #rawMaterialsPaginationPrevious").attr({"ajaxStatus":"RDProjectPaginate"})
                                    $("#rawMaterialsPaginationNext, #rawMaterialsPaginationPrevious").attr({"searchObjectFieldText": searchTextResult})
                                    $("#rawMaterialsPaginationNext, #rawMaterialsPaginationPrevious").attr({"requestType": searchRequestType})
                                    $searchRawMaterialsPage = 1
                                } else if (ajaxStatus == "search_EDIT_QualityProject") {
                                    $("#productionPaginationNext").attr({"ajaxStatus":ajaxStatus})
                                    $("#productionPaginationNext").attr({"searchObjectFieldText": searchTextResult})
                                    $("#productionPaginationNext").attr({"requestType": searchRequestType})
                                    $("#productionPaginationPrevious").attr("ajaxStatus", ajaxStatus)
                                    $("#productionPaginationPrevious").attr({"searchObjectFieldText":searchTextResult})
                                    $("#productionPaginationPrevious").attr({"requestType": searchRequestType})
                                    $searchProductionPage = 1
                                } 
                            }
                            
                        }
                    },
                error: function(jqXHR){
                    handler.handleFormError_production("Error in .searchObjectForm", jqXHR)
                },   
    		});
        }

        // Execture production ajax
        searchInProduction(
            $(this).attr("data-url"),
            $(this).attr("ajaxStatus"), 
            data, 
             $(this).find('.searchField').val(),
            $('input[name=radio]:checked').val(),
        )

        $('input[name=radio]:checked').removeAttr('checked')
    })			

})