// Handle AJAX From Submit Success -> Update Object, handle jQuery Edit/Delete implementation
import * as notification from "/static/home/js/handleNotifications.js"

export function handleEditFormObject_sales(updateLocation, data, textStatus, jqXHR){
    // console.log("handleEditFormObject_production - Grab object form data Success")
    // console.log("Form Data: " + data)
    // console.log("updateLocation: " + updateLocation)
    
	// Update information div from template
	$('.'+ updateLocation).html(data)

	// Handle UI Interations
	$(".fa-sync").removeClass("fa-spin")
}	

// Handle AJAX From Submit Success -> Update object Object, handle jQuery Edit/Delete implementation
export function handlePaginationSuccess_sales(paginationType, data, jqXHR){
    // console.log("handlePaginationSuccess_sales - Pagination Success")

    // console.log("paginationType: " + paginationType)
    if (paginationType == "customerIDPagination") {
        // Handle UI Status
        $("#customerIDResults").removeClass("blur-all")
        // $("#errorLog").slideUp()

        // Update information div from template
        $('#customerIDResults').html(data)

    } else {

        // Handle UI Status
        $("#deliveryPlan").removeClass("blur-all")
        // $("#errorLog").slideUp()

        // Update information div from template
        $('#deliveryPlan').html(data)
    }
    
} 

// Handle AJAX From Submit Success -> Update object, handle jQuery Edit/Delete implementation
export function handleFormSuccess_sales(urlLocation, refreshObject, textStatus, data, jqXHR){
    // console.log(urlLocation)	// Error JSON

    if (refreshObject) {
        // console.log("handleFormSuccess_production - refreshObject-> True")

        // Perform ajax call to refresh template in objectList.html
        $.ajax({
            method: "GET",
            beforeSend: function(xhr) { 
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                $("#deliveryPlan").addClass("blur-all")
                 },
            url: urlLocation,
            success: objectRefreshSuccess_sales,
            error: handleFormError_sales,
        }) //Setup jQuery AJAX Call

        // Handle UI
        // alert("Form information submitted succesfully!")        
    } else {

        if (confirm(textStatus)) {
            location.reload()
        } else {
            notification.makeNotification("Refresh to view changes!", "standard")
            // Handle UI Status
            $("#deliveryPlan").removeClass("blur-all")

            // Handle UI responses
            // $("#errorLog").slideUp().empty()
            $(".fa-sync").removeClass("fa-spin")
            // $("#updateItem").append("Form submitted.")

        }
    }

}

// Handle AJAX From Submit Success -> Update objects in objectList.html
export function objectRefreshSuccess_sales(textStatus, ajaxStatus, data, jqXHR){
	// console.log("objectRefreshSuccess - Form Success")
    // console.log(data)
    // alert("Action complete!")
    if (ajaxStatus == "refreshDeliveryPlanList") {
        // console.log("refresh ajaxStatus: " + ajaxStatus)
        notification.makeNotification("Refresh complete!", "standard")
        $("#deliveryPlan").removeClass("blur-all")
        $('#deliveryPlan').html(data).slideDown() 
    } else if (ajaxStatus == "search_DeliveryPlans") {
        // console.log("refresh ajaxStatus: " + ajaxStatus)
        notification.makeNotification("Search complete!", "standard")
        // console.log("search results: " + data)
        $("#deliveryPlan").removeClass("blur-all")
        $('#deliveryPlan').html(data).slideDown() 
    } else {
        // console.log("refresh ajaxStatus: " + ajaxStatus)
        notification.makeNotification("Search complete!", "standard")
        $("#customerIDResults").removeClass("blur-all")
        $('#customerIDResults').html(data).slideDown()
    }

	// Handle UI responses
    // $("#errorLog").slideUp().empty()
    $(".fa-sync").removeClass("fa-spin")
}

// Handle AJAX From Submit Failure
export function handleFormError_sales(errorLocation, jqXHR){
	// console.log("General Form Error")
    // console.log(jqXHR)
    
    // Handle UI
    $("#deliveryPlan").removeClass("blur-all")

    $(jqXHR.responseJSON["error"]).each(function(i, field){
        // console.log(field)
        notification.makeNotification(field.message, "standard")
    });
}

export function handleDeleteSuccess_sales(textStatus, jqXHR){
    // Handle UI responces
    notification.makeNotification(textStatus, "standard")
    $("#refreshDeliveryPlanList").trigger("click")
    $(".fa-sync").removeClass("fa-spin")
}