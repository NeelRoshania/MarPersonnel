// C:\Users\nrosh\Anaconda2\Scripts\PROJECTS\PYTHON\DJANGO\acpersonnel\ajaxified\home\js
// Ctrl D to find all of same and type to replace

// about:config -> dom.moduleScripts.enabled;true

// console.log("JS_quality.js found.")
import * as handler from "./handlerFunctions_quality.js"
import * as notification from "/static/home/js/handleNotifications.js"
// import * from "./handlerFunctions.js"

$(document).ready(function(){

    var $myForm = $('.sales-form')
    var headers = new Headers();
    var $qualitypage = 1;
    var $rdProject = 1;
    var $searchqualityListPage = 1
    var $searchBatchProductListPage = 1
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
    $(".objectHeader").on("click", "#searchQuality", function(){
        $("#searchQualityList").slideToggle("fast", function(){
            $(this).on("click", ".form-check-input", function(){
                if ($(this).attr("value") == 'date to be delivered') {
                    // console.log("Add datepicker...")
                    $("#search_qualityList_Field").attr("readonly", true).val('').prop('disabled', false)
                    $("#search_qualityList_Field").datepicker({
                      changeMonth: true,
                      changeYear: true,
                      yearRange: "2017:2022",
                      dateFormat: "yy-mm-dd",
                        onSelect: function(date) {
                            // $("#search_qualityList_Field").attr("readonly", true).prop('disabled', false)
                        },
                      // You can put more options here.
                    }) 
                }

                else {
                    // console.log("Remove datepicker...")
                    $("#search_qualityList_Field").datepicker("destroy").attr("readonly", false).prop('disabled', false)
                }
            })
        })
	})

    // Setup search bar date picker for fields to be edited
    $("#qualityList").on("click", ".date", function(){
        // alert("Insert a date!")
        $(this).datepicker({
          changeMonth: true,
          changeYear: true,
          yearRange: "2017:2022",
          dateFormat: "yy-mm-dd",
          // You can put more options here.
        })
    })
    

    // Setup slideToggle for object form -> This will be a unique function
    $(".objectHeader").on("click", "#addQuality", function(){
    	$("#addQualityList").slideToggle("fast")
    })

    // Setup slideToggle for object form -> This will be a unique function
    $(".objectHeader").on("click", "#refreshQualityPlanList", function(){
        // console.log("ajaxStatus: " + $(this).attr("ajaxStatus"))
    	$urlLocation = $(this).attr("data-url")
        $qualitypage = 1
        $rdProject = 1
        $searchqualityListPage = 1

        // Perform ajax call to refresh template in authorList.html
        function ajaxrefreshQualityPlanList(ajaxStatus) {
            $.ajax({
                method: "GET",
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    $("#qualityList").addClass("blur-all")
                    $(".fa-sync").addClass("fa-spin")
                    notification.makeNotification("Refresh in progress...", "standard") 
                     },
                data: {'status': 'GET -> Request card info.'},
                url: $urlLocation,
                success: function(data) {
                    handler.objectRefreshSuccess_quality("Refresh requested!", ajaxStatus, data)
                    // Reset ajaxStatus for qualityPaginationNext and qualityPaginationPrevious
                    $("#qualityPaginationNext, #qualityPaginationPrevious").attr("ajaxStatus", "refreshQualityPlanList")
                },
                error: function(jqXHR){
                    handler.handleFormError_quality("Error in #edit", jqXHR)
                },
            })
        }
        
        ajaxrefreshQualityPlanList($(this).attr("ajaxStatus"))
    })

	$("#qualityList, #addQualityList").on("click", "#edit", function(event){
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
                data: {
                    'csrfmiddlewaretoken': csrftoken, 
                    'status': 'getFormObject',
                    'ajaxStatus': ajaxState},
                success: function(data) {
                    if (data["errorMessage"]) {
                            notification.makeNotification(data["errorMessage"], "error")
                        } else {
                            handler.handleEditFormObject_quality(ajaxState, data)
                        }
                },
                error: function(jqXHR){
                    handler.handleFormError_quality("Error in #edit", jqXHR)
                },
            })            
        }
   });

	$("#qualityList, #addQualityList").on("click", "#deleteYes", function(event){
        // alert("deleteYes clicked.")
		// Handle urlLocation
        event.preventDefault()
        if (($(this).attr('ajaxStatus') == "deleteQualityPlan") || ($(this).attr('ajaxStatus') == "updateQualityPlan")) {

            // If delete actionr required, slide up
            if ($(this).attr('ajaxStatus') == "deleteQualityPlan") {
                $(this).closest("#QualityPlanList").slideUp("fast")
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
                    success: function(data, jqXHR) {
                        if (data["errorMessage"]) {
                            notification.makeNotification(data["errorMessage"], "error")
                        } else {
                            handler.handleDeleteSuccess_quality(data["message"], jqXHR)
                        }
                    },
                    error: function(jqXHR){
                        handler.handleFormError_quality("Error in #deleteYes", jqXHR)
                    },
                })

        } else if ($(this).attr('ajaxStatus') == "deleteRDProjectForm") {
            if (confirm("Warning! If there are batches for this R&D project, they will all be deleted too! \n\n Continue?")) {
                
                $(this).closest("#rdProjectResult").slideUp("fast") 

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
                    success: function(data, jqXHR) {
                        if (data["errorMessage"]) {
                            notification.makeNotification(data["errorMessage"], "error")
                        } else {
                            handler.handleDeleteSuccess_quality("Lab project deleted!")
                            location.reload()
                            // console.log(jqXHR)
                        }
                    },
                    error: function(jqXHR){
                        handler.handleFormError_quality("Error in #deleteYes", jqXHR)
                    },
                })
                // Page must reload to update M2M
                // location.reload() 
            } 
        } else if ($(this).attr('ajaxStatus') == "deleteBatchProduct") {
            if (confirm("Warning! If there are batches for this batch product, they will all be deleted too! \n\n Continue?")) {
                
                $(this).closest("#batchProductResult").slideUp("fast") 

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
                    success: function(data, jqXHR) {
                        if (data["errorMessage"]) {
                            notification.makeNotification(data["errorMessage"], "error")
                        } else {
                            notification.makeNotification(data["message"], "online")
                            location.reload()
                            // console.log(jqXHR)
                        }
                        
                    },
                    error: function(jqXHR){
                        handler.handleFormError_quality("Error in #deleteYes", jqXHR)
                    },
                })
                // Page must reload to update M2M
                // location.reload() deleteBatchProduct
            } 
        }
	});

	// Handle Pagination Previous
	$("#qualityList, #addQualityList").on("click", "#qualityPaginationPrevious", function(event) {
		event.preventDefault()
		
        if (($(this).attr("ajaxStatus") == "refreshQualityPlanList")) {
            $urlLocation = $("#refreshQualityPlanList").attr("data-url")
            $qualitypage -= 1
            // console.log("ajaxStatus: refreshQualityPlanList")
            // console.log("Search for customerID - qualityPaginationPrevious " + "$qualitypage: " + $qualitypage + " urlLocation: " + $urlLocation)

            $.ajax({
                method: "GET",
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    $("#qualityList").addClass("blur-all")
                    $(".loaderStatus").empty().show()
                     },
                data: {
                        "qualitypage" : $qualitypage,
                        "ajaxStatus": $(this).attr("ajaxStatus")
                    },
                url: $urlLocation,
                success: function(data) {
                    if (data["errorMessage"]) {
                        notification.makeNotification(data["errorMessage"], "error")
                    } else {
                        handler.handlePaginationSuccess_quality("qualityListPagination", data)
                        $("#qualityPaginationNext, #qualityPaginationPrevious").attr("ajaxStatus", "refreshQualityPlanList")
                    }
                },
                error: function(jqXHR){
                        handler.handleFormError_quality("Error in qualityPaginationPrevious", jqXHR)
                    }, 
                

            }) //Setup jQuery AJAX Call     

        } else if (($(this).attr("ajaxStatus") == "search_QualityPlans")){
            // Has the user made a request to search for Delivery Plans?
            $urlLocation = $(this).attr("data-url")
            $searchqualityListPage -= 1
            // console.log("ajaxStatus: search_QualityPlans")
            // console.log("Search for customerID - qualityPaginationPrevious " + "$searchqualityListPage: " + $searchqualityListPage + " urlLocation: " + $urlLocation)

            function searchPaginationNext(searchTextResult, searchRequest, urlLocation, dataToSend) {
                $.ajax({
                    method: "GET",
                    beforeSend: function(xhr) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        $("#qualityList").addClass("blur-all")
                        $(".loaderStatus").empty().show()
                         },
                    data: dataToSend,
                    url: urlLocation,
                    success: function(data) {
                        if (data["errorMessage"]) {
                            notification.makeNotification(data["errorMessage"], "error")
                        } else {
                            handler.handlePaginationSuccess_quality("searchqualityList", data)
                            $("#qualityPaginationNext, #qualityPaginationPrevious").attr("ajaxStatus", "search_QualityPlans")
                            $("#qualityPaginationNext, #qualityPaginationPrevious").attr("searchObjectFieldText", searchTextResult)
                            $("#qualityPaginationNext, #qualityPaginationPrevious").attr({"requestType": searchRequest})
                        }
                    },
                    error: function(jqXHR){
                        handler.handleFormError_quality("Error in searchPaginationPrevious", jqXHR)
                    }, 
                    

                }) //Setup jQuery AJAX Call  
            }
            searchPaginationNext(
                $(this).attr("searchObjectFieldText"), 
                $(this).attr("requestType"),
                $(this).attr("data-url"), 
                {
                    "searchqualityListPage" : $searchqualityListPage, 
                    "searchObjectFieldText": $(this).attr("searchObjectFieldText"),
                    "ajaxStatus": $(this).attr("ajaxStatus"),
                    "requestType": $(this).attr("requestType"),
                }
            )
        }	
   });		

	// Handle Pagination Next - This needs to account for search CustomerID and general qualityList andsearched ones
	$("#qualityList, #addQualityList").on("click", "#qualityPaginationNext", function(event){
		event.preventDefault()

        if (($(this).attr("ajaxStatus") == "refreshQualityPlanList")) {
            // Is the user making a general pagination request for the delivery plans?
            $urlLocation = $("#refreshQualityPlanList").attr("data-url")
            $qualitypage += 1
            // console.log("ajaxStatus: refreshQualityPlanList")
            // console.log("Search for customerID - qualityPaginationNext " + "$qualitypage: " + $qualitypage + " urlLocation: " + $urlLocation)

            $.ajax({
                method: "GET",
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    $("#qualityList").addClass("blur-all")
                    $(".loaderStatus").empty().show()
                     },
                data: {
                        "qualitypage" : $qualitypage,
                        "ajaxStatus": $(this).attr("ajaxStatus")
                    },
                url: $urlLocation,
                success: function(data) {
                    if (data["errorMessage"]) {
                        notification.makeNotification(data["errorMessage"], "error")
                    } else {
                        handler.handlePaginationSuccess_quality("qualityListPagination", data)
                        $("#qualityPaginationNext, #qualityPaginationPrevious").attr("ajaxStatus", "refreshQualityPlanList")
                    }
                },
                error: function(jqXHR){
                        handler.handleFormError_quality("Error in searchPaginationNext", jqXHR)
                    }, 
            }) //Setup jQuery AJAX Call     
        } else if (($(this).attr("ajaxStatus") == "search_QualityPlans")) {
            // Has the user made a request to search for Delivery Plans?
            $searchqualityListPage += 1
            // console.log("ajaxStatus: search_QualityPlans")
            // console.log("Search for customerID - qualityPaginationNext " + "$searchqualityListPage: " + $searchqualityListPage + " urlLocation: " + $urlLocation)

            function searchPaginationNext(searchTextResult, searchRequestType, urlLocation, dataToSend) {
                $.ajax({
                    method: "GET",
                    beforeSend: function(xhr) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        $("#qualityList").addClass("blur-all")
                        $(".loaderStatus").empty().show()
                         },
                    data: dataToSend,
                    url: urlLocation,
                    success: function(data) {
                        if (data["errorMessage"]) {
                            notification.makeNotification(data["errorMessage"], "error")
                        } else {
                            handler.handlePaginationSuccess_quality("searchqualityList", data)
                            $("#qualityPaginationNext, #qualityPaginationPrevious").attr("ajaxStatus", "search_QualityPlans")
                            $("#qualityPaginationNext, #qualityPaginationPrevious").attr("searchObjectFieldText", searchTextResult)
                            $("#qualityPaginationNext, #qualityPaginationPrevious").attr({"requestType": searchRequestType})
                        }
                    },
                    error: function(jqXHR){
                        handler.handleFormError_quality("Error in searchPaginationNext", jqXHR)
                    },   
                }) //Setup jQuery AJAX Call  
            }
            searchPaginationNext(
                $(this).attr("searchObjectFieldText"), 
                $(this).attr("requestType"),
                $(this).attr("data-url"), 
                {
                    "searchqualityListPage" : $searchqualityListPage, 
                    "searchObjectFieldText": $(this).attr("searchObjectFieldText"),
                    "ajaxStatus": $(this).attr("ajaxStatus"),
                    "requestType": $(this).attr("requestType"),
                })
            }
        });	
    

    // Handle Pagination Next - This needs to account for search CustomerID and general qualityList andsearched ones
    $("#addQualityList").on("click", "#RDProjectsPaginationNext", function(event){
        event.preventDefault()
        $urlLocation = $(this).attr("data-url")
        $rdProject += 1
        // console.log("Search for RD Project - RDProjectsPaginationNext " + "$rdProject: " + $rdProject)

        function searchPaginationNext(searchTextResult, urlLocation, dataToSend) {
            $.ajax({
                method: "GET",
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    $("#RDProjectResults").addClass("blur-all")
                    $(".loaderStatus").empty().show()
                     },
                data: dataToSend,
                url: $urlLocation,
                success: function(data) {
                    if (data["errorMessage"]) {
                        notification.makeNotification(data["errorMessage"], "error")
                    } else {
                        handler.handlePaginationSuccess_quality("RDProjectPagination", data)
                        $("#RDProjectsPaginationNext, #RDProjectsPaginationPrevious").attr("searchObjectFieldText", searchTextResult)
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
                    "rdProject": $rdProject,
                    "RDProjectPaginate": true,
                },
                $(this).attr("ajaxStatus"),
            )
        }
    )

    $("#addQualityList").on("click", "#RDProjectsPaginationPrevious", function(event){
        event.preventDefault()
        $urlLocation = $(this).attr("data-url")
        $rdProject -= 1
        // console.log("Search for RD Project - RDProjectsPaginationPrevious " + "$rdProject: " + $rdProject)

        function searchPaginationNext(searchTextResult, urlLocation, dataToSend) {
            $.ajax({
                method: "GET",
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    $("#RDProjectResults").addClass("blur-all")
                    $(".loaderStatus").empty().show()
                     },
                data: dataToSend,
                url: $urlLocation,
                success: function(data) {
                    if (data["errorMessage"]) {
                        notification.makeNotification(data["errorMessage"], "error")
                    } else {
                        handler.handlePaginationSuccess_quality("RDProjectPagination", data)
                        $("#RDProjectsPaginationNext, #RDProjectsPaginationPrevious").attr("searchObjectFieldText", searchTextResult)
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
                    "rdProject": $rdProject,
                    "RDProjectPaginate": true,
                },
                $(this).attr("ajaxStatus"),
            )
        }
    )

    // Handle Pagination Next - This needs to account for search CustomerID and general qualityList andsearched ones
    $("#addQualityList").on("click", "#batchProjectsPaginationNext", function(event){
        event.preventDefault()
        $urlLocation = $(this).attr("data-url")
        $searchBatchProductListPage += 1
        // console.log("Search for batch product - batchProjectsPaginationNext " + "$searchBatchProductListPage: " + $searchBatchProductListPage)

        function searchPaginationNext(searchTextResult, urlLocation, dataToSend) {
            $.ajax({
                method: "GET",
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    $("#RDProjectResults").addClass("blur-all")
                    $(".loaderStatus").empty().show()
                     },
                data: dataToSend,
                url: $urlLocation,
                success: function(data) {
                    if (data["errorMessage"]) {
                        notification.makeNotification(data["errorMessage"], "error")
                    } else {
                        handler.handlePaginationSuccess_quality("batchProductPaginate", data)
                        $("#batchProjectsPaginationNext, #batchProjectsPaginationPrevious").attr("searchObjectFieldText", searchTextResult)
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
                    "searchBatchProductListPage": $searchBatchProductListPage,
                    "batchProductPaginate": true,
                },
                $(this).attr("ajaxStatus"),
            )
        }
    )

    // Handle Pagination Next - This needs to account for search CustomerID and general qualityList andsearched ones
    $("#addQualityList").on("click", "#batchProjectsPaginationPrevious", function(event){
        event.preventDefault()
        $urlLocation = $(this).attr("data-url")
        $searchBatchProductListPage -= 1
        // console.log("Search for batch product - batchProjectsPaginationNext " + "$searchBatchProductListPage: " + $searchBatchProductListPage)

        function searchPaginationNext(searchTextResult, urlLocation, dataToSend) {
            $.ajax({
                method: "GET",
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    $("#RDProjectResults").addClass("blur-all")
                    $(".loaderStatus").empty().show()
                     },
                data: dataToSend,
                url: $urlLocation,
                success: function(data) {
                    if (data["errorMessage"]) {
                        notification.makeNotification(data["errorMessage"], "error")
                    } else {
                        handler.handlePaginationSuccess_quality("batchProductPaginate", data)
                        $("#batchProjectsPaginationNext, #batchProjectsPaginationPrevious").attr("searchObjectFieldText", searchTextResult)
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
                    "searchBatchProductListPage": $searchBatchProductListPage,
                    "batchProductPaginate": true,
                },
                $(this).attr("ajaxStatus"),
            )
        }
    )

    // Handle add object form submission
    $(document).on('submit', '.quality-form', function(event){
       // code
        event.preventDefault()  // Prevent the form from submitting straight away
        // alert(".my-ajax-form' clicked.")
        var $urlLocation = $(this).attr("data-url") // URL location specified in form to send data to
        var data = $(this).serializeArray() // Grab the form information effeciently
        $(this).clear   // Clear form to prevent double submit
        data.push(
            {name: "ajaxStatus", value: $(this).attr("ajaxStatus")},
            {name: "paintInfo", value: $(this).attr("paintInfo")},
            {name: "url", value: $urlLocation},
            {name: "newObjectSubmit", value: true},
            );  // Accumulate ajax data fields
        // console.log("POST URL Location --> " + $urlLocation + '\nSerialized AJAX Data --> ' + $.param(data) )

        if (confirm("Is this information correct?")) {
            // Perform ajax call to update entry
            $.ajax({
                method: "POST",
                url: $urlLocation,
                beforeSend: function(xhr) {
                        $("#qualityList").addClass("blur-all")
                        xhr.setRequestHeader("X-CSRFToken", csrftoken)
                        $myForm[0].reset(); // reset form data 
                         },
                data: $.param(data),
                success: function(data){
                    if (data["errorMessage"]) {
                        notification.makeNotification(data["errorMessage"], "error")
                    } else {
                        notification.makeNotification(data["message"], "online")
                        handler.handleFormSuccess_quality($("#refreshQualityPlanList").attr("data-url"), false, "Information updated. Ok to refresh?", data)
                    }
                },
                error: function(jqXHR){
                    handler.handleFormError_quality("Error in .sales-form", jqXHR)
                },    
            });
        }
        
    })

	// Handle editObjectForm - Need to think of a way to identify each edit from uniquely from a js perspective
	$(document).on('submit', '.editQualityForm', function(event){
	   // code
        event.preventDefault()	// Prevent the form from submitting straight away
        // console.log("object Edit Form submitted...")
        var $urlLocation = $(this).attr("data-url") // URL location specified in form to send data to
        var data = $(this).serializeArray() // Grab the form information effeciently
        data.push(
        	{name: "ajaxStatus", value: $(this).attr("ajaxStatus")},
            {name: "paintInfo", value: $(this).attr("paintInfo")},
        	{name: "editObjectSubmit", value: true} );	// Accumulate ajax data fields
        $(this).clear	// Clear form to prevent double submit
        // console.log("POST URL Location --> " + $urlLocation + '\n\nSerialized AJAX Data --> ' + $.param(data) )

        if (confirm("Quality information correct?")) {
            // Perform ajax call to update entry
            $.ajax({
                method: "POST",
                url: $urlLocation,
                beforeSend: function(xhr) {
                        $("#qualityList").addClass("blur-all")
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        // $("#updateItem").append("Form submitted.")
                         },
                data:  $.param(data),
                success: function(data){
                    if (data["errorMessage"]) {
                        notification.makeNotification(data["errorMessage"], "error")
                    } else {
                        notification.makeNotification(data["message"], "online")
                        handler.handleFormSuccess_quality($("#refreshQualityPlanList").attr("data-url"), false, "Information updated. Ok to refresh?", data)
                    }
                },
                error: function(jqXHR){
                    handler.handleFormError_quality("Error in .editQualityForm", jqXHR)
                },     
            });
        }  
    })	

    // Handle searchObjectForm - Need to think of a way to identify each edit from uniquely from a js perspective
	$(document).on('submit', '.searchQuality-form', function(event){
        event.preventDefault()	// Prevent the form from submitting straight away

        var data = $(this).serializeArray() // Grab the form information effeciently
        var val = ""
        $qualitypage = 1;
        $rdProject = 1;
        $searchqualityListPage = 1
        $searchBatchProductListPage = 1

        data.push(
        	{name: "ajaxStatus", value: $(this).attr("ajaxStatus")},
        	{name: "searchObjectSubmit", value: true},
            {name: "urlLocation", value: $urlLocation},
            {name: "rdProject", value: $rdProject},
            {name: "qualitypage", value: $qualitypage},
            {name: "searchqualityListPage", value: $searchqualityListPage},
            {name: "searchBatchProductListPage", value: $searchBatchProductListPage},
            );	// Used to direct search query to mixins.py

        $(this).clear	// Clear form to prevent double submit
        // console.log("GET URL Location --> " + $(this).attr("data-url"))
        // console.log($.param(data))

        // Perform ajax call to update entry 
        function searchInQuality(urlAjaxLocation, ajaxStatus, dataToPass, searchText, searchRequest){
            // console.log(dataToPass)
            $.ajax({
                method: "GET",
                url: urlAjaxLocation,
                beforeSend: function(xhr) {
                        // $("#customerIDResult").addClass("blur-all")
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        notification.makeNotification("Search in progress...", "standard")
                         },
                data:  $.param(dataToPass),
                success: function(data) {
                    // console.log("Ajax success")
                    if (data["errorMessage"]) {
                        notification.makeNotification(data["errorMessage"], "error")
                    } else {
                        if (data["message"]) {
                            notification.makeNotification(data["message"], "online")
                        } else {
                            handler.objectRefreshSuccess_quality("Refresh requested!", ajaxStatus, data)
                            // Pagination section must now be configured to continue search requests
                            if (ajaxStatus == "search_QualityPlans"){
                                $("#qualityPaginationNext, #qualityPaginationPrevious").attr({"ajaxStatus":"search_QualityPlans"})
                                $("#qualityPaginationNext, #qualityPaginationPrevious").attr({"searchObjectFieldText": searchText})
                                $("#qualityPaginationNext, #qualityPaginationPrevious").attr({"requestType": searchRequest})
                            } else if (ajaxStatus == "search_EDIT_QualityProject") {
                                $("#RDProjectsPaginationNext, #RDProjectsPaginationPrevious").attr({"ajaxStatus":"RDProjectPaginate"})
                                $("#RDProjectsPaginationNext, #RDProjectsPaginationPrevious").attr({"searchObjectFieldText": searchText})
                            } else {
                                $("#batchProjectsPaginationNext, #batchProjectsPaginationPrevious").attr({"ajaxStatus":"batchProductPaginate"})
                                $("#batchProjectsPaginationNext, #batchProjectsPaginationPrevious").attr({"searchObjectFieldText": searchText})
                            }
                        }
                        
                    }
                    
                },
                error: function(jqXHR){
                    handler.handleFormError_quality("Error in .searchSales-form", jqXHR)
                },   
            });
        }
        
        $(data).each(function(i, field){
            if (field.name === "searchObjectFieldText") {
                // console.log(field.name + ": " + field.value)
                val = field.value
            }
        });

        searchInQuality(
            $(this).attr("data-url"),
            $(this).attr("ajaxStatus"), 
            data, 
            val,
            $('input[name=radio]:checked').val(),
        )

        $('input[name=radio]:checked').removeAttr('checked')
    })
})