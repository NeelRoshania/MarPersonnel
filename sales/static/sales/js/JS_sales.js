// C:\Users\nrosh\Anaconda2\Scripts\PROJECTS\PYTHON\DJANGO\acpersonnel\ajaxified\home\js
// Ctrl D to find all of same and type to replace

// about:config -> dom.moduleScripts.enabled;true

// console.log("JS_sales.js found.")
import * as handler from "./handlerFunctions_sales.js"
import * as notification from "/static/home/js/handleNotifications.js"

// import * from "./handlerFunctions.js"

$(document).ready(function(){

    var $myForm = $('.sales-form')
    var headers = new Headers();
    var $salesPage = 1;
    var $customerIDPage = 1;
    var $searchDeliveryPlanPage = 1
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
    $(".objectHeader").on("click", "#searchDeliveryRoutes", function(){
        $("#searchDeliveryRoutesForm").slideToggle("fast", function(){
            $(this).on("click", ".form-check-input", function(){
                if ($(this).attr("value") == 'date to be delivered') {
                    // console.log("Add datepicker...")
                    $("#search_DeliveryPlan_Field").attr("readonly", true).val('').prop('disabled', false)
                    $("#search_DeliveryPlan_Field").datepicker({
                      changeMonth: true,
                      changeYear: true,
                      yearRange: "2017:2022",
                      dateFormat: "yy-mm-dd",
                        onSelect: function(date) {
                            // $("#search_DeliveryPlan_Field").attr("readonly", true).prop('disabled', false)
                        },
                      // You can put more options here.
                    }) 
                }

                else {
                    // console.log("Remove datepicker...")
                    $("#search_DeliveryPlan_Field").datepicker("destroy").attr("readonly", false).prop('disabled', false)
                }
            })
        })
	})

    // Setup search bar date picker for fields to be edited
    $(".objectHeader").on("click", ".date", function(){
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
    $(".objectHeader").on("click", "#addDeliveryRoute", function(){
    	$("#addDeliveryRouteForm").slideToggle("fast")
    })

    // Setup slideToggle for object form -> This will be a unique function
    $("#userToDo").on("click", function(){
        // alert("UserToDO clicked...")
        // $("#updateItem").append("UserToDo clicked.")
    })

    // Setup slideToggle for object form -> This will be a unique function
    $(".objectHeader").on("click", "#refreshDeliveryPlanList", function(){
        // console.log("ajaxStatus: " + $(this).attr("ajaxStatus"))
    	$urlLocation = $(this).attr("data-url")
        $salesPage = 1
        $customerIDPage = 1
        $searchDeliveryPlanPage = 1

        // Perform ajax call to refresh template in authorList.html
        function ajaxRefreshDeliveryPlan(ajaxStatus) {
            $.ajax({
                method: "GET",
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    $("#deliveryPlan").addClass("blur-all")
                    $(".fa-sync").addClass("fa-spin")
                    notification.makeNotification("Refresh in progress...", "standard") 
                     },
                data: {'status': 'GET -> Request card info.'},
                url: $urlLocation,
                success: function(data) {
                    handler.objectRefreshSuccess_sales("Refresh requested!", ajaxStatus, data)
                    // Reset ajaxStatus for salesPaginationNext and salesPaginationPrevious
                    $("#salesPaginationNext, #salesPaginationPrevious").attr("ajaxStatus", "refreshDeliveryPlanList")
                },
                error: function(jqXHR){
                    handler.handleFormError_sales("Error in .searchSales-form", jqXHR)
                },   
            })
        }
        
        ajaxRefreshDeliveryPlan($(this).attr("ajaxStatus"))
    })

	$("#deliveryPlan, #addDeliveryRouteForm").on("click", "#edit", function(event){
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
                    handler.handleEditFormObject_sales(ajaxState, data)
                },
                error: function(jqXHR){
                    handler.handleFormError_sales("Error in #edit", jqXHR)
                },
            })            
        }
   });

	$("#deliveryPlan, #addDeliveryRouteForm").on("click", "#deleteYes", function(event){
        // alert("deleteYes clicked.")
		// Handle urlLocation
        event.preventDefault()
        if ($(this).attr('ajaxStatus') == "deliveredDeliveryPlanForm") {
            // $(this).closest("#DeliveryPlanList").slideUp("fast")
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
                    success: function(jqXHR) {
                        handler.handleDeleteSuccess_sales("Delivery route updated!", jqXHR)
                    },
                    error: function(jqXHR){
                        handler.handleFormError_sales("Error in #deleteYes", jqXHR)
                    },
                })
        } else if ($(this).attr('ajaxStatus') == "deleteCustomerIDForm") {
            if (confirm("Warning! If there are delivery plans for this customer, they will be deleted too! \n\n Continue?")) {
                
                $(this).closest("#customerIDResult").slideUp("fast") 

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
                    success: function(jqXHR) {
                        // console.log(jqXHR)
                        handler.handleDeleteSuccess_sales("Customer deleted!", jqXHR)
                        location.reload()
                    },
                    error: function(jqXHR){
                        handler.handleFormError_sales("Error in #deleteYes", jqXHR)
                    },
                })
                // Page must reload to update M2M
                // location.reload()
            }
        }
	});

	// Handle Pagination Previous
	$("#deliveryPlan, #addDeliveryRouteForm").on("click", "#salesPaginationPrevious", function(event) {
		event.preventDefault()
		
        if (($(this).attr("ajaxStatus") == "refreshDeliveryPlanList")) {
            $urlLocation = $("#refreshDeliveryPlanList").attr("data-url")
            $salesPage -= 1
            // console.log("ajaxStatus: refreshDeliveryPlanList")
            // console.log("Search for DeliveryPlan - customerIDPaginationPrevious " + "$salesPage: " + $salesPage + " urlLocation: " + $urlLocation)

            $.ajax({
                method: "GET",
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    $("#deliveryPlan").addClass("blur-all")
                    $(".loaderStatus").empty().show()
                     },
                data: {
                        "salesPage" : $salesPage,
                        "ajaxStatus": $(this).attr("ajaxStatus")
                    },
                url: $urlLocation,
                success: function(data) {
                    if (data["errorMessage"]) {
                        notification.makeNotification(data["errorMessage"], "standard")
                    } else {
                        handler.handlePaginationSuccess_sales("DeliveryPlanPagination", data)
                        $("#salesPaginationNext, #salesPaginationPrevious").attr("ajaxStatus", "refreshDeliveryPlanList")
                    }
                },
                error: handler.handleFormError,
                

            }) //Setup jQuery AJAX Call     

        } else if (($(this).attr("ajaxStatus") == "search_DeliveryPlans")){
            // Has the user made a request to search for Delivery Plans?
            $urlLocation = $(this).attr("data-url")
            $searchDeliveryPlanPage -= 1
            // console.log("ajaxStatus: search_DeliveryPlans")
            // console.log("Search for DeliveryPlan - search_DeliveryPlans " + "$searchDeliveryPlanPage: " + $searchDeliveryPlanPage + " urlLocation: " + $urlLocation)

            function searchPaginationNext(searchTextResult, searchRequest, urlLocation, dataToSend) {
                $.ajax({
                    method: "GET",
                    beforeSend: function(xhr) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        $("#deliveryPlan").addClass("blur-all")
                        $(".loaderStatus").empty().show()
                         },
                    data: dataToSend,
                    url: urlLocation,
                    success: function(data) {
                        if (data["errorMessage"]) {
                            notification.makeNotification(data["errorMessage"], "standard")
                        } else {
                            handler.handlePaginationSuccess_sales("searchDeliveryPlan", data)
                            $("#salesPaginationNext, #salesPaginationPrevious").attr("ajaxStatus", "search_DeliveryPlans")
                            $("#salesPaginationNext, #salesPaginationPrevious").attr("searchObjectFieldText", searchTextResult)
                            $("#salesPaginationNext, #salesPaginationPrevious").attr({"requestType": searchRequest})
                        }
                    },
                    error: function(jqXHR){
                        handler.handleFormError_sales("Error in searchPaginationNext", jqXHR)
                    }, 

                }) //Setup jQuery AJAX Call  
            }
            searchPaginationNext(
                $(this).attr("searchObjectFieldText"), 
                $(this).attr("requestType"),
                $(this).attr("data-url"), 
                {
                    "searchDeliveryPlanPage" : $searchDeliveryPlanPage, 
                    "searchObjectFieldText": $(this).attr("searchObjectFieldText"),
                    "ajaxStatus": $(this).attr("ajaxStatus"),
                    "requestType": $(this).attr("requestType"),
                }
            )
        }	
   });		

	// Handle Pagination Next - This needs to account for search CustomerID and general deliveryPLan andsearched ones
	$("#deliveryPlan, #addDeliveryRouteForm").on("click", "#salesPaginationNext", function(event){
		event.preventDefault()

        if (($(this).attr("ajaxStatus") == "refreshDeliveryPlanList")) {
            // Is the user making a general pagination request for the delivery plans?
            $urlLocation = $("#refreshDeliveryPlanList").attr("data-url")
            $salesPage += 1
            // console.log("ajaxStatus: refreshDeliveryPlanList")
            // console.log("Search for DeliveryPlan - customerIDPaginationNext " + "$salesPage: " + $salesPage + " urlLocation: " + $urlLocation)

            $.ajax({
                method: "GET",
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    $("#deliveryPlan").addClass("blur-all")
                    $(".loaderStatus").empty().show()
                     },
                data: {
                        "salesPage" : $salesPage,
                        "ajaxStatus": $(this).attr("ajaxStatus")
                    },
                url: $urlLocation,
                success: function(data) {
                    if (data["errorMessage"]) {
                        notification.makeNotification(data["errorMessage"], "standard")
                    } else {
                        handler.handlePaginationSuccess_sales("DeliveryPlanPagination", data)
                        $("#salesPaginationNext, #salesPaginationPrevious").attr("ajaxStatus", "refreshDeliveryPlanList")
                    }
                },
                error: function(jqXHR){
                        handler.handleFormError_sales("Error in searchPaginationNext", jqXHR)
                    }, 
            }) //Setup jQuery AJAX Call     
        } else if (($(this).attr("ajaxStatus") == "search_DeliveryPlans")) {
            // Has the user made a request to search for Delivery Plans?
            $urlLocation = $(this).attr("data-url")
            $searchDeliveryPlanPage += 1
            // console.log("ajaxStatus: search_DeliveryPlans")
            // console.log("Search for DeliveryPlan - customerIDPaginationNext " + "$searchDeliveryPlanPage: " + $searchDeliveryPlanPage + " urlLocation: " + $urlLocation)

            function searchPaginationNext(searchTextResult, searchRequestType, urlLocation, dataToSend) {
                $.ajax({
                    method: "GET",
                    beforeSend: function(xhr) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        $("#deliveryPlan").addClass("blur-all")
                        $(".loaderStatus").empty().show()
                         },
                    data: dataToSend,
                    url: urlLocation,
                    success: function(data) {
                        if (data["errorMessage"]) {
                            notification.makeNotification(data["errorMessage"], "standard")
                        } else {
                            handler.handlePaginationSuccess_sales("searchDeliveryPlan", data)
                            $("#salesPaginationNext, #salesPaginationPrevious").attr("ajaxStatus", "search_DeliveryPlans")
                            $("#salesPaginationNext, #salesPaginationPrevious").attr("searchObjectFieldText", searchTextResult)
                            $("#salesPaginationNext, #salesPaginationPrevious").attr({"requestType": searchRequestType})
                        }
                    },
                    error: function(jqXHR){
                        handler.handleFormError_sales("Error in searchPaginationNext", jqXHR)
                    },   
                }) //Setup jQuery AJAX Call  
            }
            searchPaginationNext(
                $(this).attr("searchObjectFieldText"), 
                $(this).attr("requestType"),
                $(this).attr("data-url"), 
                {
                    "searchDeliveryPlanPage" : $searchDeliveryPlanPage, 
                    "searchObjectFieldText": $(this).attr("searchObjectFieldText"),
                    "ajaxStatus": $(this).attr("ajaxStatus"),
                    "requestType": $(this).attr("requestType"),
                })
            }
        });	

    // Handle Pagination Next - This needs to account for search CustomerID and general deliveryPLan andsearched ones
    $("#addDeliveryRouteForm").on("click", "#customerIDPaginationNext", function(event){
        event.preventDefault()
        $urlLocation = $(this).attr("data-url")
        $customerIDPage += 1
        // console.log("Search for customerID - customerIDPaginationPrevious " + "$customerIDPage: " + $customerIDPage)

        function searchPaginationNext(searchTextResult, urlLocation, dataToSend) {
            $.ajax({
                method: "GET",
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    $("#customerIDResult").addClass("blur-all")
                    $(".loaderStatus").empty().show()
                     },
                data: dataToSend,
                url: $urlLocation,
                success: function(data) {
                    if (data["errorMessage"]) {
                        notification.makeNotification(data["errorMessage"], "standard")
                    } else {
                        handler.handlePaginationSuccess_sales("customerIDPagination", data)
                        $("#customerIDPaginationNext, #customerIDPaginationPrevious").attr("searchObjectFieldText", searchTextResult)
                    }
                    
                },
                error: function(jqXHR){
                    handler.handleFormError_sales("Error in searchPaginationNext", jqXHR)
                },
            }) //Setup jQuery AJAX Call
        }

        searchPaginationNext(
                $(this).attr("searchObjectFieldText"),
                $(this).attr("data-url"),
                {
                    "searchObjectFieldText": $(this).attr("searchObjectFieldText"),
                    "customerIDPage": $customerIDPage,
                    "customerIDPaginate": true,
                },
                $(this).attr("ajaxStatus"),
            )
        }
    )

    $("#addDeliveryRouteForm").on("click", "#customerIDPaginationPrevious", function(event){
        event.preventDefault()
        $urlLocation = $(this).attr("data-url")
        $customerIDPage -= 1
        // console.log("Search for customerID - customerIDPaginationPrevious " + "$customerIDPage: " + $customerIDPage)

        function searchPaginationNext(searchTextResult, urlLocation, dataToSend) {
            $.ajax({
                method: "GET",
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    $("#customerIDResult").addClass("blur-all")
                    $(".loaderStatus").empty().show()
                     },
                data: dataToSend,
                url: $urlLocation,
                success: function(data) {
                    if (data["errorMessage"]) {
                        notification.makeNotification(data["errorMessage"], "standard")
                    } else {
                        handler.handlePaginationSuccess_sales("customerIDPagination", data)
                        $("#customerIDPaginationNext, #customerIDPaginationPrevious").attr("searchObjectFieldText", searchTextResult)
                    }
                    
                },
                error: function(jqXHR){
                    handler.handleFormError_sales("Error in searchPaginationNext", jqXHR)
                },
            }) //Setup jQuery AJAX Call
        }

        searchPaginationNext(
                $(this).attr("searchObjectFieldText"),
                $(this).attr("data-url"),
                {
                    "searchObjectFieldText": $(this).attr("searchObjectFieldText"),
                    "customerIDPage": $customerIDPage,
                    "customerIDPaginate": true,
                },
                $(this).attr("ajaxStatus"),
            )
        }
    )

    // Handle add object form submission
    $(document).on('submit', '.sales-form', function(event){
       // code
        event.preventDefault()  // Prevent the form from submitting straight away
        // alert(".my-ajax-form' clicked.")
        var $urlLocation = $(this).attr("data-url") // URL location specified in form to send data to
        var data = $(this).serializeArray() // Grab the form information effeciently
        $(this).clear   // Clear form to prevent double submit
        data.push(
            {name: "ajaxStatus", value: $(this).attr("ajaxStatus")},
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
                        $("#deliveryPlan").addClass("blur-all")
                        xhr.setRequestHeader("X-CSRFToken", csrftoken)
                        $myForm[0].reset(); // reset form data 
                       notification.makeNotification("Update in progress...", "standard")
                         },
                data: $.param(data),
                success: function(data){
                    notification.makeNotification(data["message"], "standard")
                    handler.handleFormSuccess_sales($("#refreshDeliveryPlanList").attr("data-url"), false, "Information updated. Ok to refresh?", data)
                    // console.log("Data: " + data)
                },
                error: function(jqXHR){
                    handler.handleFormError_sales("Error in .sales-form", jqXHR)
                },    
            });
        }
        
    })

	// Handle editObjectForm - Need to think of a way to identify each edit from uniquely from a js perspective
	$(document).on('submit', '.editSalesForm', function(event){
	   // code
        event.preventDefault()	// Prevent the form from submitting straight away
        // console.log("object Edit Form submitted...")
        var $urlLocation = $(this).attr("data-url") // URL location specified in form to send data to
        var data = $(this).serializeArray() // Grab the form information effeciently
        data.push(
        	{name: "ajaxStatus", value: $(this).attr("ajaxStatus")},
        	{name: "editObjectSubmit", value: true} );	// Accumulate ajax data fields
        $(this).clear	// Clear form to prevent double submit
        // console.log("POST URL Location --> " + $urlLocation + '\nSerialized AJAX Data --> ' + $.param(data) )

        if (confirm("Is this information correct?")) {
            // Perform ajax call to update entry
            $.ajax({
                method: "POST",
                url: $urlLocation,
                beforeSend: function(xhr) {
                        $("#deliveryPlan").addClass("blur-all")
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        // $("#updateItem").append("Form submitted.")
                        notification.makeNotification("Update in progress...", "standard")
                         },
                data:  $.param(data),
                success: function(data){
                    notification.makeNotification(data["message"], "standard")
                    handler.handleFormSuccess_sales($("#refreshDeliveryPlanList").attr("data-url"), false, "Information updated. Ok to refresh?", data)
                },
                error: function(jqXHR){
                    handler.handleFormError_sales("Error in .editProductionForm", jqXHR)
                },     
                });
        }  
    })	

    // Handle searchObjectForm - Need to think of a way to identify each edit from uniquely from a js perspective
	$(document).on('submit', '.searchSales-form', function(event){
        event.preventDefault()	// Prevent the form from submitting straight away
        // alert("Search for object...")
        var data = $(this).serializeArray() // Grab the form information effeciently
        var val = ""
        $searchDeliveryPlanPage = 1
        $customerIDPage = 1
        data.push(
        	{name: "ajaxStatus", value: $(this).attr("ajaxStatus")},
        	{name: "searchObjectSubmit", value: true},
            {name: "urlLocation", value: $urlLocation},
            {name: "customerIDPage", value: $customerIDPage},
            {name: "searchDeliveryPlanPage", value: $searchDeliveryPlanPage},
            );	// Used to direct search query to mixins.py
        $(this).clear	// Clear form to prevent double submit
        // console.log("GET URL Location --> " + $(this).attr("data-url"))
        // console.log($.param(data))

        // Perform ajax call to update entry 
        function searchInSales(urlAjaxLocation, ajaxStatus, dataToPass, searchText, searchRequest){

            $.ajax({
                method: "GET",
                url: urlAjaxLocation,
                beforeSend: function(xhr) {
                    notification.makeNotification("Search in progress...", "standard")
                    if (ajaxStatus == "search_DeliveryPlans") {
                        $("#deliveryPlan").addClass("blur-all")
                    } else {
                        $("#customerIDResult").addClass("blur-all")
                    }
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                 },
                data:  $.param(dataToPass),
                success: function(data) {
                    if (data["errorMessage"]) {
                        notification.makeNotification(data["errorMessage"], "error")
                    } else {
                        if (data["message"]) {
                            notification.makeNotification(data["message"], "error")
                        } else {
                            handler.objectRefreshSuccess_sales("Refresh requested!", ajaxStatus, data)
                            // Pagination section must now be configured to continue search requests
                            if (ajaxStatus == "search_DeliveryPlans"){
                                $("#salesPaginationNext, #salesPaginationPrevious").attr({"ajaxStatus":"search_DeliveryPlans"})
                                $("#salesPaginationNext, #salesPaginationPrevious").attr({"searchObjectFieldText": searchText})
                                $("#salesPaginationNext, #salesPaginationPrevious").attr({"requestType": searchRequest})
                            } else {
                                $("#customerIDPaginationNext, #customerIDPaginationPrevious").attr({"ajaxStatus":"customerIDPaginate"})
                                $("#customerIDPaginationNext, #customerIDPaginationPrevious").attr({"searchObjectFieldText": searchText})
                                // $("#customerIDPaginationNext, #customerIDPaginationPrevious").attr({"requestType": searchRequest})
                            }
                        }
                        
                    }
                },
                error: function(jqXHR){
                    handler.handleFormError_sales("Error in .searchSales-form", jqXHR)
                },   
            });

        }

        $(data).each(function(i, field){
            if (field.name === "searchObjectFieldText") {
                // console.log(field.name + ": " + field.value)
                val = field.value
            }
        });

        searchInSales(
            $(this).attr("data-url"),
            $(this).attr("ajaxStatus"), 
            data, 
            val,
            $('input[name=radio]:checked').val(), // This is too vague, only works if doing single search requests
        )

        $('input[name=radio]:checked').removeAttr('checked')
})
})