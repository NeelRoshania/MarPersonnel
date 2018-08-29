// Handle AJAX From Submit Success -> Update Object, handle jQuery Edit/Delete implementation
import * as notification from "/static/home/js/handleNotifications.js"
export function handleEditFormObject_quality(updateLocation, data, textStatus, jqXHR){
    // console.log("handleEditFormObject_quality - Grab object form data Success")
    // console.log("Form Data: " + data)
    // console.log("updateLocation: " + updateLocation)
    
	// Update information div from template
	$('.'+ updateLocation).html(data)

	// Handle UI Interations
	$(".fa-sync").removeClass("fa-spin")
}	

// Handle AJAX From Submit Success -> Update object Object, handle jQuery Edit/Delete implementation
export function handlePaginationSuccess_quality(paginationType, data, jqXHR){
    // console.log("handlePaginationSuccess_quality - Pagination Success")
    // console.log("paginationType: " + paginationType)
    
    if (paginationType == "RDProjectPagination") {
        // console.log(data) 
        // Handle UI Status
        $("#RDProjectResults").removeClass("blur-all")
        // $("#errorLog").slideUp()

        // Update information div from template
        $('#RDProjectResults').html(data)

    } else if (paginationType == "batchProductPaginate") {
        // console.log(data) 
        // Handle UI Status
        $("#batchProductResults").removeClass("blur-all")
        // $("#errorLog").slideUp()
        // Update information div from template
        $('#batchProductResults').html(data)
    } else {
        // console.log(data) 
        // Handle UI Status
        $("#qualityList").removeClass("blur-all")
        // $("#errorLog").slideUp()

        // Update information div from template
        $('#qualityList').html(data)
    }
    
} 

// Handle AJAX From Submit Success -> Update object, handle jQuery Edit/Delete implementation
export function handleFormSuccess_quality(urlLocation, refreshObject, textStatus, data, jqXHR){
    // console.log(urlLocation)	// Error JSON

    if (refreshObject) {
        // console.log("handleFormSuccess_quality - refreshObject-> True")

        // Perform ajax call to refresh template in objectList.html
        $.ajax({
            method: "GET",
            beforeSend: function(xhr) { 
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                $("#qualityList").addClass("blur-all")
                 },
            url: urlLocation,
            success: function(){
                objectRefreshSuccess_quality("Refresh requested!")
            },
            error: function() {
                handleFormError_quality("Error on refreshObject")
            },
        }) //Setup jQuery AJAX Call

        // Handle UI
        // alert("Form information submitted succesfully!")        
    } else {

        if (confirm(textStatus)) {
            location.reload()
            // console.log("handleFormSuccess_quality - refreshObject-> True")
        } else {
            // Handle UI Status
            $("#qualityList").removeClass("blur-all")

            // Handle UI responses
            // $("#errorLog").slideUp().empty()
            $(".fa-sync").removeClass("fa-spin")
            // $("#updateItem").append("Form submitted.")
        }

        
    }

}

// Handle AJAX From Submit Success -> Update objects in objectList.html
export function objectRefreshSuccess_quality(textStatus, ajaxStatus, data, jqXHR){
	// console.log("objectRefreshSuccess_quality - Form Success")
    // console.log(data)

    if (ajaxStatus == "refreshQualityPlanList") {
        // console.log("refresh ajaxStatus: " + ajaxStatus)
        notification.makeNotification("Refresh complete!", "standard")
        $("#qualityList").removeClass("blur-all")
        $('#qualityList').html(data).slideDown() 
    } else if (ajaxStatus == "search_QualityPlans") {
        // console.log("refresh ajaxStatus: " + ajaxStatus)
        notification.makeNotification("Search complete!", "standard")
        // console.log("search results: " + data)
        $("#qualityList").removeClass("blur-all")
        $('#qualityList').html(data).slideDown() 
    } else if ((ajaxStatus == "search_EDIT_QualityProject") || (ajaxStatus == "RDProjectsPaginationNext") || (ajaxStatus == "RDProjectsPaginationPrevious")) {
        // console.log("refresh ajaxStatus: " + ajaxStatus)
        notification.makeNotification("Search complete!", "standard")
        $("#RDProjectResults").removeClass("blur-all")
        $('#RDProjectResults').html(data).slideDown()
    } else {
        notification.makeNotification("Search complete!", "standard")
        $("#batchProductResults").removeClass("blur-all")
        $('#batchProductResults').html(data).slideDown()
    }

	// Handle UI responses
    // $("#errorLog").slideUp().empty()
    $(".fa-sync").removeClass("fa-spin")
}

// Handle AJAX From Submit Failure
export function handleFormError_quality(errorLocation, jqXHR){
	// console.log("General Form Error")
    // console.log(jqXHR)
    
    // Handle UI
    $("#qualityList").removeClass("blur-all")

    $(jqXHR.responseJSON["error"]).each(function(i, field){
        // console.log(field)
        notification.makeNotification(field.message, "error")
    });
}

export function handleDeleteSuccess_quality(textStatus, jqXHR){
    // Handle UI responces
    notification.makeNotification(textStatus, "online")
    $("#refreshQualityPlanList").trigger("click")
    $(".fa-sync").removeClass("fa-spin")
}